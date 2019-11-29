from django.shortcuts import render
from .models import EnemyAlliance, EnemyNation
from pwapi.utils import pw_api


def enemy_slots(request):
    """ Show data for enemy nations with open defensive slots"""

    enemy_alliances = EnemyAlliance.objects.all()
    if not enemy_alliances.exists():
        return render(request, 'enemy_monitoring/slots.html', {'no_enemies': True})
    enemies = []
    for enemy in enemy_alliances:
        enemy_nations = pw_api(api='alliance', object_id=enemy.alliance_id)['member_id_list']
        for nation in enemy_nations:
            nation_data = pw_api(api='nation', object_id=nation)
            # ignore vacation mode players
            if nation_data['vmode'] != '0':
                continue
            defensive_wars = len(nation_data['defensivewar_ids'])
            open_slots = 3 - defensive_wars
            # Due to a game bug, it is sometimes possible for a nation to be in 4 defensive wars despite only having 3
            # slots, hence the need to account for negative open slots.
            if open_slots <= 0:
                continue

            enemy_data = {'name': nation_data['name'],
                          'leadername': nation_data['leadername'],
                          'alliance': nation_data['alliance'],
                          'slots': open_slots,
                          'beige_turns_left': nation_data['beige_turns_left'],
                          'score': nation_data['score'],
                          'soldiers': nation_data['soldiers'],
                          'tanks': nation_data['tanks'],
                          'aircraft': nation_data['aircraft'],
                          'ships': nation_data['ships'],
                          'nukes': nation_data['nukes'],
                          'link': 'https://politicsandwar.com/nation/id=' + str(nation)
                          }
            enemy_score = float(nation_data['score'])
            min_score_to_attack = enemy_score / 1.75
            max_score_to_attack = enemy_score / .75
            enemy_data['min_score'] = min_score_to_attack
            enemy_data['max_score'] = max_score_to_attack
            enemies.append(enemy_data)

    return render(request, 'enemy_monitoring/slots.html', {'enemies': enemies})


def enemy_spies(request):
    """ Display a list of spy counts and policies for enemy nations """
    enemies = EnemyNation.objects.all()
    if not enemies.exists():
        return render(request, 'enemy_monitoring/spies.html', {'no_enemies': True})
    return render(request, 'enemy_monitoring/spies.html', {'enemies': enemies})
