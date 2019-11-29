# member_logger.py
# usage: python manage.py member_logger
# add new member log records to the MemberLog class. By default, this should be set to run automatically every day at
# 8:10pm EST, which is ten minutes after game update every day. Right after update is the best time to collect new data,
# however waiting a bit is needed as the game servers slow down considerably immediately after update (8pm EST).

from pwapi.utils import pw_api
from public.models import Member, MemberLog
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Updates the member table and makes new member logs'

    def handle(self, *args, **kwargs):
        # get the in-game list of members and their data, represented as a list of dicts. Info about the keys used in this
        # dict can be found in modules/api.py, in the comments for this function (get_sk_members)
        members = pw_api(api='alliance members', object_id=615)
        # update the members table
        update_members(members)
        # add new member logs for each member
        make_logs(members)


# update the members table
#    parameters: members - a list of dictionaries representing each current member.
#    returns: nothing, just updates the DB to match the in-game data.
def update_members(members):

    # unfortunately our API data (members) is just a list of dicts for each nation. I want to cross-reference that list
    # against the returned Member objects from the DB. People in-game who aren't in the DB get a new record created,
    # while existing ones have their records updated. Rather than a convoluted double loop, where I loop through each
    # DB member, then loop through each API member to see if their natID is a match, I instead convert the API data to
    # a dict with each member as a value, keyed to their nation ID. That way I can loop through each Member object and
    # see if its .nation_id exists as a key in my new dict.

    # dict to store the in-game member data (as opposed to the returned list of dicts from the API)
    game_members = {}
    # Loop through each member in the returned list of API members, and add each one as a value to our dictionary, using
    # the nation id as the key
    for member in members:
        nation_id = member['nationid']
        # the game stores the vacation mode status of members as a 1 or a 0 (as strings), whereas we type them as
        # bools in the member class
        if member['vacmode'] == "0":
            vm = False
        else:
            vm = True
        game_members[nation_id] = {'ruler': member['leader'], 'nation': member['nation'], 'vm': vm}

    # Get all the existing Member objects
    db_members = Member.objects.all()
    # set to store their nation ids. This will fill as we loop through the objects. Any ids in game_members that aren't
    # in the set are completely new and need new Objects made for them.
    db_ids = set()
    # loop through our existing member objects and update as needed
    for member in db_members:
        # add their nation id to the db_ids set
        db_ids.add(member.nation_id)
        # if they are still with us (in the in-game list) we want to update everything to match in-game data.
        if member.nation_id in game_members:
            # I had two ways to do this. Previously in CS50 I used a series of if statements to check if the values
            # differed between the db and in-game, and only then run an update. Here I just update everything without
            # checking. The former is potenitally lighter on the DB (if nothing is different, no SQL is run), whereas
            # the latter, which I currently use, is less code. I'm not sure which is more important.
            member.ruler = game_members[member.nation_id]['ruler']
            member.nation = game_members[member.nation_id]['nation']
            member.vm = game_members[member.nation_id]['vm']
            # since this member is listed with us in-game, set the status to active
            member.status = 'active'
        # otherwise they are no longer members, and we just update their status accordingly.
        else:
            member.status = 'former'
        # save the changes
        member.save()

    # Make any new member objects.
    # loop through the keys (nation IDs) in the game_members dict
    for key in game_members:
        # if they aren't in the db_ids set, then this member needs a new Object created for them.
        if key not in db_ids:
            # dict for this member (easier than constantly writing game_member[key][key] to access its values
            member = game_members[key]
            # make and save the new object
            new_member = Member(nation_id=key, ruler=member['ruler'], nation=member['nation'], vm=member['vm'],
                                status='active')
            new_member.save()


# Create new logs for each in-game member not in VM. (update_members must be run before this, otherwise new members
# might not have objects to tie their logs to!)
# Parameters: members, a list of dicts representing each member, taken from the games API
def make_logs(members):
    # loop through each member and make a new log only if they aren't in VM
    for member in members:
        # Non-VM nations are given a value of '0' (as a string). Only make a new record if they have this value.
        if member['vacmode'] == '0':
            # calculate the total number of wars. API splits this into offensive and defensive, we just want total
            wars = member['offensivewars'] + member['defensivewars']
            # get the member object to insert as the foreign key reference in the MemberLog.nation_id field
            member_object = Member.objects.get(nation_id=member['nationid'])
            # make and save a new log
            new_log = MemberLog(nation_id=member_object, time_inactive=member['minutessinceactive'],
                                color=member['color'], soldiers=member['soldiers'], tanks=member['tanks'],
                                aircraft=member['aircraft'], ships=member['ships'], spies=member['spies'],
                                gasoline=member['gasoline'], munitions=member['munitions'], steel=member['steel'],
                                aluminum=member['aluminum'], uranium=member['uranium'], money=member['money'],
                                wars=wars, cities=member['cities'], score=member['score'])
            new_log.save()

