from json import JSONDecodeError
import requests
from ..models import Profile_database
from requests.exceptions import JSONDecodeError
import json
steam_API = '1B14188AD762CC570112DE0C9C4CDE60'

api_requests = {
    'IsteamUser': f'https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/',
    'GetPlayerSummaries': f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',
    'GetBadges': f'https://api.steampowered.com/IPlayerService/GetBadges/v1/',
}
api_requests2 = f'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'


def check_for_id(id):
    asnwered_paramID = requests.get(api_requests2, {'key': steam_API, 'vanityurl': id}).json()

    if asnwered_paramID.get('response').get('success') == 1:
        customURL = id
        steamID = asnwered_paramID.get('response').get('steamid')
        if steamid_account_check(steamID):
            json_load_data(id=steamID, customid=customURL)
            return steamID

    else:
        steamID = id
        if steamid_account_check(steamID):
            json_load_data(id=id)
            return steamID

    #Небыл передан steamID, означает что пользователя несуществует.
    return True


def json_load_data(id, customid=None):
    if Profile_database.objects.filter(steam_link_id=id).exists():
        cumstomID_update(user=id, customID=customid)
        return None

    result_data = {}
    for key, link in api_requests.items():
        params = {
            'key': steam_API,
            'steamids': id
        }
        try:
            response = requests.get(link, params=params)
            result_data[key] = response.json()
        except JSONDecodeError:
            params['steamid'] = params.pop('steamids', None)
            data = requests.get(link, params=params).json()
            result_data[key] = data

    to_database_saver(result_data, customid)
    return None


def to_database_saver(data, customid=None):
    steam_save = Profile_database(
        steam_link_id=data.get('IsteamUser', {}).get('players', {})[0].get('SteamId'),
        player_lvl=data.get('GetBadges', {}).get('response', {}).get('player_level', 'Account-Hidden'),
        nickname=data.get('GetPlayerSummaries', {}).get('response', {}).get('players', {})[0].get('personaname'),
        time_created=data.get('GetPlayerSummaries', {}).get('response', {}).get('players', {})[0].get('timecreated'),
        economyBan=data.get('IsteamUser', {}).get('players', {})[0].get('EconomyBan'),
        vacbanned=data.get('IsteamUser', {}).get('players', {})[0].get('VACBanned'),
        communityBanned=data.get('IsteamUser', {}).get('players', {})[0].get('CommunityBanned'),
        avatar_url=data.get('GetPlayerSummaries', {}).get('response', {}).get('players', {})[0].get('avatarfull'),
        avatar_s=data.get('GetPlayerSummaries', {}).get('response', {}).get('players', {})[0].get('avatar'),
    )

    steam_save.save()
    if customid:
        (Profile_database.objects.filter(steam_link_id=data.get('IsteamUser', {}).get('players', {})[0].get('SteamId'))
         .update(steam_customlink=customid))


    return None


def steamid_account_check(steamid):
    user_test = requests.get(api_requests['IsteamUser'], {
            'key': steam_API,
            'steamids': steamid
        }).json()
    if not user_test.get('players'):
        return False
    return True

def cumstomID_update(user, customID):
    data = Profile_database.objects.get(steam_link_id=user)
    data.steam_customlink = customID
    data.save()

