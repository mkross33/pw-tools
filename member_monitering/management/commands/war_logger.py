# war_logger.py
# usage: python manage.py war_logs
# purpose: updates the data in the wars tab, and adds new war_attacks to the attacks table
# Runs via CRON every day after the member logger (set to run at 8:30 with member logger running at 8:10 PM)

from pwapi.utils import pw_api
from modules.helpers import rss_cost, unit_cost
from django.core.management.base import BaseCommand
from public.models import WarAttacks, Wars, Member
from dateutil import parser


class Command(BaseCommand):
    help = 'Updates the member table and makes new member logs'

    def handle(self, *args, **kwargs):
        # get the ID's of all recorded SK wars in the API (Only saves from last 30 days)
        wars = pw_api(api='wars', object_id=615)
        # create new War objects for any new wars
        create_war_records(wars)
        # Get all the war objects which are marked as active
        active_wars = Wars.objects.filter(active=True)
        # make new attack records for them, as needed
        create_attack_records(active_wars)
        # Once all the latest records have been added. We can update all finished wars to be marked as such in DB
        update_war_status(wars)


# Add new records to the wars table
# Input: wars, a list of dicts representing each SK war logged on the game server. Returns nothing, just updates the DB
def create_war_records(wars):
    # loop through the active wars making War objects for new wars
    for war in wars:
        # if this war's ID doesn't have a War object for it, make a new one
        if not Wars.objects.filter(war_id=war['warID']).exists():
            # Convert date from ISO String to datetime object
            date = parser.parse(war['date'])
            # Get the corresponding member object for the war
            try:
                member = Member.objects.get(nation_id=war['member_id'])
            # if we don't have a member for this yet, forget it and move on. We'll pick it up and add it with the next
            # log cycle
            except:
                continue
            # get the member object to reference in the War object
            cities = member.logs.latest('timestamp').cities
            # make and save the new War object
            new_war = Wars(war_id=war['warID'], date=date, member_id=member, member_cities=cities,
                           enemy_id=war['enemy_id'], enemy_ruler=war['enemy_ruler'], enemy_nation=war['enemy_nation'],
                           enemy_alliance=war['enemy_alliance'], enemy_cities=war['enemy_cities'])
            new_war.save()


# adds new attack records for active wars in our database
# input: wars, a list of war objects
def create_attack_records(wars):
    # loop through the passed in wars
    for war in wars:
        # Get the attack_ids of every logged attack associated with this war ID.
        logged_attacks = war.attacks.values('attack_id')
        # get all the attacks launched in this war from the API
        attacks = pw_api(api='war attacks', object_id=war.war_id)
        # loop through each attack and make new records for new ones. We loop in reverse order because the game stores
        # the latest attacks first, whereas I want to go through them and add them in chronological order from the first
        # attack on.
        for attack in attacks[::-1]:
            # if we already have a record for this attack, or it is a fortify (no actual attack, but logged as such
            # in the games API), skip it. Attack ID must be typed back to int first.
            if (int(attack['war_attack_id']) in logged_attacks) or (attack['attack_type'] == 'fortify'):
                continue
            # otherwise make a new record.
            else:
                # Counters to store the unit casualties. Innitialize to 0. API doesn't give us these, just casualty 1,
                # casualty 2, with what it represents differing based on attack type. We will figure that out later as
                # needed, though for victory message attacks all casualties stay 0
                attcas_soldiers = 0
                attcas_tanks = 0
                attcas_aircraft = 0
                attcas_ships = 0
                defcas_soldiers = 0
                defcas_tanks = 0
                defcas_aircraft = 0
                defcas_ships = 0

                # type the loot to a float (everything in this API is a string, for whatever reason)
                money_looted = float(attack['money_looted'])
                # counters for total damage dealt and taken. Damage, at the very least, is equal to money loot. These
                # will be updated as necessary
                damage_dealt = money_looted
                damage_taken = 0.0

                # victory type attacks are unique attacks at the end of a war that just loot the enemy. There are no
                # casualties to track or infra destroyed, and only one possible result.
                if attack['attack_type'] == 'victory':
                    # infra destroyed isn't even listed in this response, so we manually set it to 0 (naturally 0 value)
                    infra_destroyed = 0.0
                    infra_value = 0.0
                    # call the result victory
                    result = 'victory'
                # if it was a regular attack, we have some real calculations to do to get the total damages, casualties
                # and result. Unfortunately the API does not make this easy.
                else:
                    # type destroyed infra and value back to floats from strings
                    infra_destroyed = float(attack['infra_destroyed'])
                    try:
                        infra_value = float(attack['infra_destroyed_value'])
                    except TypeError:
                        infra_value = 0.0

                    # type the casualties back to ints
                    attack['attcas1'] = int(attack['attcas1'])
                    attack['attcas2'] = int(attack['attcas2'])
                    attack['defcas1'] = int(attack['defcas1'])
                    attack['defcas2'] = int(attack['defcas2'])

                    # Use the attack type to figure out what units these casualties represent.
                    # See logic guide here: http://politicsandwar.wikia.com/wiki/War_Attacks_API

                    # All airstrike types have att/def cas1 as aircraft. There is never an attcas2, sometimes a defcas2.
                    if 'airstrike' in attack['attack_type']:
                        # change the type to just airstrike. We don't want to use the games airstrike1, airstrike2, etc
                        attack['attack_type'] = 'airstrike'
                        # add the cas1 casualties to aircraft casualties for both sides
                        attcas_aircraft += attack['attcas1']
                        defcas_aircraft += attack['defcas1']
                        # add their monetary values to damages. defender casualties = damage dealt, attcas damage taken
                        damage_dealt += unit_cost('aircraft', defcas_aircraft)
                        damage_taken += unit_cost('aircraft', attcas_aircraft)

                        # The following airstrikes have a defcas2, which varies by the type.
                        # update the casualties and the damages (based on cost of lost units) accordingly
                        # airstrike money
                        if attack['attack_type'] == 'airstrike4':
                            # Since this casualty is actually lost money, it can be added directly to damages. No
                            # casualties get updated
                            damage_dealt += attack['defcas2']
                        # airstrike soldiers
                        elif attack['attack_type'] == 'airstrike2':
                            defcas_soldiers = attack['defcas2']
                            damage_dealt += unit_cost('soldiers', defcas_soldiers)
                        # airstrike tanks
                        elif attack['attack_type'] == 'airstrike3':
                            defcas_tanks = attack['defcas2']
                            damage_dealt += unit_cost('tanks', defcas_tanks)
                        # airstrike ships
                        elif attack['attack_type'] == 'airstrike5':
                            defcas_ships = attack['defcas2']
                            damage_dealt += unit_cost('ships', defcas_ships)
                    # if its a ground battle, 1 is soldiers and 2 is tanks
                    elif attack['attack_type'] == 'ground':
                        attcas_soldiers += attack['attcas1']
                        damage_taken += unit_cost('soldiers', attcas_soldiers)
                        attcas_tanks += attack['attcas2']
                        damage_taken += unit_cost('tanks', attcas_tanks)
                        defcas_soldiers = attack['defcas1']
                        damage_taken += unit_cost('soldiers', defcas_soldiers)
                        defcas_tanks += attack['defcas2']
                        damage_taken += unit_cost('tanks', defcas_tanks)
                    # if it's a naval battle, cas1 is ships, no cas2.
                    elif attack['attack_type'] == 'naval':
                        attcas_ships += attack['attcas1']
                        damage_taken += unit_cost('ships', attcas_ships)
                        defcas_ships += attack['defcas1']
                        damage_taken += unit_cost('ships', defcas_ships)

                    # missiles and nuclear attacks have no casualties, only infra destroyed.
                    # type is either missile/nuke or missilef/nukef for failed launches, so we test for substrings
                    # cost of the missile/nuke is treated as damage_taken, since the attacker is set back that cost
                    elif 'missile' in attack['attack_type']:
                        damage_taken += unit_cost('missile', 1)
                        # just call it missile, dont want to keep a missilef if it is one
                        attack['attack_type'] = 'missile'
                    elif attack['attack_type'] == 'nuke' or attack['attack_type'] == 'nukef':
                        damage_taken += unit_cost('nuke', 1)
                        attack['attack_type'] = 'nuke'

                    # calculate the cost of gas and munitions used by each side, and add to the damages. Some attack
                    # types don't have any values for these, and attacks where none are used sometimes hae 0, sometimes
                    # have no value, raising a NoneType error. Since the API is not always consistant, I just throw
                    # these in a try except. If a TypeError gets raised, it means no resources were used and we just
                    # move on
                    try:
                        attgas = float(attack['att_gas_used'])
                        attmun = float(attack['att_mun_used'])
                        defgas = float(attack['def_gas_used'])
                        defmun = float(attack['def_mun_used'])
                        # add them to the totals
                        damage_dealt += rss_cost('gasoline', defgas) + rss_cost('munitions', defmun)
                        damage_taken += rss_cost('gasoline', attgas) + rss_cost('munitions', attmun)
                    except TypeError:
                        pass

                    # Set the result. API uses numbers to represent this, whereas I want to store the actual name
                    if attack['success'] == '3':
                        result = 'Immense Triumph'
                    elif attack['success'] == '2':
                        result = 'Moderate Success'
                    elif attack['success'] == '1':
                        result = 'Pyrrhic Victory'
                    else:
                        result = 'Utter Failure'

                # like everything else, the winners ID is stored as a string. Cast it back to int before adding
                victor = int(attack['victor'])
                new_record = WarAttacks(attack_id=attack['war_attack_id'], war_id=war,
                                        attacker_id=attack['attacker_nation_id'], victor=victor,
                                        defender_id=attack['defender_nation_id'], type=attack['attack_type'],
                                        result=result, infra_destroyed=infra_destroyed, infra_value=infra_value,
                                        money_looted=money_looted, attcas_soldiers=attcas_soldiers,
                                        attcas_tanks=attcas_tanks, attcas_aircraft=attcas_aircraft,
                                        attcas_ships=attcas_ships, defcas_soldiers=defcas_soldiers,
                                        defcas_tanks=defcas_tanks, defcas_ships=defcas_ships,
                                        defcas_aircraft=defcas_aircraft, damage_dealt=damage_dealt,
                                        damage_taken=damage_taken)
                new_record.save()


# Update the status of any finished wars that are still marked as active in the DB
# takes as argument wars, a list of dicts for each in-game war. For each one marked as finished, we update the DB
def update_war_status(wars):
    # loop through the in-game wars
    for war in wars:
        # if the active value is False, update the Wars object to be the same
        if not war['active']:
            finished_war = Wars.objects.get(war_id=war['warID'])
            finished_war.active = False
            finished_war.save()
