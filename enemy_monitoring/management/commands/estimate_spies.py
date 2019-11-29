from django.core.management.base import BaseCommand
from modules.spy_funcs import guess_spies
from public.models import Enemy, EnemyNation
from pwapi.utils import pw_api

# guesses number of spies for an enemy alliance


class Command(BaseCommand):
    help = 'Guesses the spy counts of enemy alliances'

    def handle(self, *args, **kwargs):
        # get the enemy alliances
        enemies = Enemy.objects.all()
        # loop through each and call the nations API filtering on their ID
        for enemy in enemies:
            # nations API filter to show only this alliances members
            aa_filter = f'alliance_id={enemy.alliance_id}'
            # get the nations API data for that AA. Key into nations to access the nations list in the returned dict
            nations = pw_api(api='nations', filters=aa_filter)
            # loop through each nation and create/update nation objects with spy info
            for nation in nations:
                # calculate their current spy count
                spies = guess_spies(nation['nationid'])
                # set their current war policy
                policy = nation['war_policy']
                # if they already have an EnemyNation object, update it
                if EnemyNation.objects.filter(nation_id=nation['nationid']).exists():
                    obj = EnemyNation.objects.get(nation_id=nation['nationid'])
                    obj.spies = spies
                    obj.policy = policy
                    obj.save()
                # otherwise make a new object for them
                else:
                    new_enemy_nation = EnemyNation(alliance=enemy, nation_id=nation['nationid'], ruler=nation['leader'],
                                                   nation=nation['nation'], score=nation['score'], spies=spies,
                                                   policy=nation['war_policy'])
                    new_enemy_nation.save()

