from urllib.request import Request, urlopen
import json

api_url = 'https://politicsandwar.com/api/'
header = {'User-Agent': 'Mozilla/5.0'}


def get_webpage(url):
    req = Request(url, headers=header)
    webpage = urlopen(req).read()
    data = json.loads(webpage)
    return data


# function to call the various APIs. Optional parameters for ids that some APIs require.
# different API urls have different formats, hence the extra logic.
# due to arcane API design, some results may need to be keyed into to get the actual data
def pw_api(api=None, object_id=None, filters=None, key=None):
    # alliance members API: https://politicsandwar.fandom.com/wiki/Alliance_Members_API
    if api == 'alliance members':
        data = get_webpage(f"{api_url}alliance-members/?allianceid={object_id}&key={key}")['nations']
    # nation API: https://politicsandwar.fandom.com/wiki/Nation_API
    elif api == 'nation':
        return get_webpage(f"{api_url}nation/id={object_id}&key={key}")
    # nations API: https://politicsandwar.fandom.com/wiki/Nations_API
    elif api == 'nations':
        if filters:
            data = get_webpage(f"{api_url}nations/?key={key}&{filters}")['nations']
        else:
            data = get_webpage(f"{api_url}nations/?key={key}")['nations']
    # alliance API: https://politicsandwar.fandom.com/wiki/Alliance_API
    elif api == 'alliance':
        data = get_webpage(f"{api_url}alliance/id={object_id}&key={key}")
    # alliances API: https://politicsandwar.fandom.com/wiki/Alliances_API
    elif api == 'alliances':
        data = get_webpage(f"{api_url}alliances/?key={key}")['alliances']
    # wars API: https://politicsandwar.fandom.com/wiki/Wars_API
    elif api == 'wars':
        data = get_webpage(f"{api_url}wars/?alliance_id={object_id},500/&key={key}")['wars']
    # war API: https://politicsandwar.fandom.com/wiki/War_API
    elif api == 'war':
        data = get_webpage(f"{api_url}war/{object_id}/&key={key}")['war'][0]
    # war attacks API: https://politicsandwar.fandom.com/wiki/War_Attacks_API
    elif api == 'war attacks':
        data = get_webpage(f"{api_url}war-attacks/key={key}&war_id={object_id}")['war_attacks']
    # trade price API: https://politicsandwar.fandom.com/wiki/Tradeprice_API
    elif api == 'trade price':
        data = get_webpage(f"{api_url}tradeprice/resource={object_id}&key={key}")
    else:
        data = None
    return data


