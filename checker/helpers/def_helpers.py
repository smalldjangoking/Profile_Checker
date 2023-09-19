from json import JSONDecodeError
import requests
from ..models import Profile_database
import json

steam_API = '1B14188AD762CC570112DE0C9C4CDE60'
api_requests = {
    'IsteamUser': f'https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/',
    'GetPlayerSummaries': f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',
    'GetBadges': f'https://api.steampowered.com/IPlayerService/GetBadges/v1/',
}


def check_for_id(first, second, steam_API):
    if first:
        valuepost = first
        resolve_url = f'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={steam_API}&vanityurl={valuepost}'
        custom_and_id = requests.get(resolve_url).json()
        try:
            # проверка не прошла успешна на customid (под видом обычного айди)
            if custom_and_id['response'].get('message') == 'No match':
                api_url_ban = f'http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={steam_API}&steamids={valuepost}'
                api_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steam_API}&steamids={valuepost}"
                api_lvl = f"https://api.steampowered.com/IPlayerService/GetBadges/v1/?key={steam_API}&steamid={valuepost}"
                data_profile = requests.get(api_url).json()
                data_bans = requests.get(api_url_ban).json()
                data_lvls = requests.get(api_lvl).json()
                player_level = data_lvls.get('response', {}).get('player_level', 0)
                player_level_json = json.dumps({"player_level": player_level})
                # Объединение двух JSON-объектов
                merged_data = data_profile.copy()
                merged_data.update(data_bans)
                merged_data.update(json.loads(player_level_json))
                return merged_data
            # проверка прошла успешна, берем customid под видом айди.
            elif custom_and_id['response']['steamid']:
                valuepost_real_id = custom_and_id['response']['steamid']
                api_url_ban = f'http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={steam_API}&steamids={valuepost_real_id}'
                api_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steam_API}&steamids={valuepost_real_id}"
                api_lvl = f"https://api.steampowered.com/IPlayerService/GetBadges/v1/?key={steam_API}&steamid={valuepost_real_id}"
                data_profile = requests.get(api_url).json()
                data_bans = requests.get(api_url_ban).json()
                data_lvls = requests.get(api_lvl).json()
                player_level = data_lvls.get('response', {}).get('player_level', 0)
                player_level_json = json.dumps({"player_level": player_level})
                # Объединение двух JSON-объектов
                merged_data = data_profile.copy()
                merged_data.update(data_bans)
                merged_data.update(json.loads(player_level_json))
                return merged_data
        except JSONDecodeError:
            message = 'Такого пользователя не существует'
            return message

    # точно кастомайди
    elif second:
        valuepost = second
        resolve_url = f'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={steam_API}&vanityurl={valuepost}'
        custom_and_id = requests.get(resolve_url).json()
        try:
            valuepost_real_id = custom_and_id['response']['steamid']
            api_url_ban = f'http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={steam_API}&steamids={valuepost_real_id}'
            api_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steam_API}&steamids={valuepost_real_id}"
            api_lvl = f"https://api.steampowered.com/IPlayerService/GetBadges/v1/?key={steam_API}&steamid={valuepost_real_id}"
            data_profile = requests.get(api_url).json()
            data_bans = requests.get(api_url_ban).json()
            data_lvls = requests.get(api_lvl).json()
            player_level = data_lvls.get('response', {}).get('player_level', 0)
            player_level_json = json.dumps({"player_level": player_level})
            # Объединение двух JSON-объектов
            merged_data = data_profile.copy()
            merged_data.update(data_bans)
            merged_data.update(json.loads(player_level_json))
            return merged_data

        except KeyError:
            message = 'Такого пользователя не существует'
            return message


def to_data_base(**kwargs):
    account_info = kwargs['valuedata']['response']['players'][0]
    ban_info = kwargs['valuedata']['players'][0]
    steam_link_id = account_info.get('steamid')
    steam_save = Profile_database(
        steam_link_id=account_info.get('steamid'),
        ban=ban_info,
        profile_data=account_info,
        steam_customlink=account_info.get('profileurl').split('/')[-2],
        player_lvl=kwargs['valuedata']['player_level'],
        nickname=account_info.get('personaname'),
        time_created=account_info.get('timecreated'),
        economyBan=ban_info.get('EconomyBan'),
        vacbanned=ban_info.get('VACBanned'),
        communityBanned=ban_info.get('CommunityBanned'),
        avatar_url=account_info.get('avatarfull')
    )

    steam_save.save()

    return steam_link_id


def json_load_data(id):
    if Profile_database.objects.filter(steam_link_id=id).exists():
        print('True')
        return None


    result_data = {}
    for key, link in api_requests.items():
        params = {
            'key': steam_API,
            'steamids': id
        }
        try:
            data = requests.get(link, params=params).json()
            result_data[key] = data
        except requests.exceptions.JSONDecodeError:
            params['steamid'] = params.pop('steamids', None)
            data = requests.get(link, params=params).json()
            result_data[key] = data
    to_database_saver(result_data)
    return None

def to_database_saver(data):
    steam_save = Profile_database(
        steam_link_id=data.get('IsteamUser', {}).get('players', {})[0].get('SteamId'),
        player_lvl=data.get('GetBadges', {}).get('response', {}).get('player_level'),
        nickname=data.get('GetPlayerSummaries', {}).get('response', {}).get('players', {})[0].get('personaname'),
        time_created=data.get('GetPlayerSummaries', {}).get('response', {}).get('players', {})[0].get('timecreated'),
        economyBan=data.get('IsteamUser', {}).get('players', {})[0].get('EconomyBan'),
        vacbanned=data.get('IsteamUser', {}).get('players', {})[0].get('VACBanned'),
        communityBanned=data.get('IsteamUser', {}).get('players', {})[0].get('CommunityBanned'),
        avatar_url=data.get('GetPlayerSummaries', {}).get('response', {}).get('players', {})[0].get('avatarfull'),
        avatar_s=data.get('GetPlayerSummaries', {}).get('response', {}).get('players', {})[0].get('avatar'),
    )

    steam_save.save()
    return None


