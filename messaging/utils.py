from messaging.models import MessageLog
from pwapi.utils import pw_api
from pwapi.models import PwKey


def get_noobs():
    """ Function to build out an dictionary of new players

    'Newness' is approximated via score and activity, ignoring players already in an alliance or
    in vacation mode."""

    api_key = PwKey.objects.filter(valid=True, limited=False)[0]
    nations = pw_api(api='nations', filters='alliance_id=0', key=api_key)
    noobs = []
    # API responses are ordered descending (smallest at the end)
    for nation in nations[::-1]:
        # threshold in minutes since last login, to consider the nation inactive
        inactive_threshold = 2880
        if (nation['vacmode'] == 0) and (nation['minutessinceactive'] < inactive_threshold):
            noobs.append(nation)
        if len(noobs) >= 200:
            break
    return noobs


# filter out already messaged nations
def filter_noobs(noobs):
    filtered_noobs = []
    for noob in noobs:
        if MessageLog.objects.filter(recipient=noob['nationid']).exists():
            continue
        filtered_noobs.append(noob)
    return filtered_noobs