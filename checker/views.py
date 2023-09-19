from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from checker.forms import SearchProfileForm
from .models import Profile_database
import json
from .helpers.def_helpers import check_for_id, to_data_base, json_load_data
import datetime
from social_core.backends.steam import SteamOpenId
from social_django.models import UserSocialAuth
from django.urls import reverse

steam_API = '1B14188AD762CC570112DE0C9C4CDE60'

@login_required
def profile(request):
    user = request.user
    steam_id = user.social_auth.get(provider='steam').uid
    json_load_data(steam_id)
    return render(request, 'checker/profile_template.html')


def main_page(request):
    if request.method == 'POST':
        searchprofileform = SearchProfileForm(request.POST)
        if searchprofileform.is_valid():
            cleaned_data = searchprofileform.cleaned_data['search_form']
            steam_id = cleaned_data['steam_id']
            custom_url = cleaned_data['custom_url']

            if Profile_database.objects.filter(steam_customlink=steam_id).exists():
                custom_url_ = Profile_database.objects.get(steam_customlink=steam_id)
                return redirect('profile_url', custom_url_.steam_link_id)

            if Profile_database.objects.filter(steam_link_id=steam_id).exists():
                return redirect('profile_url', steam_id)

            elif Profile_database.objects.filter(steam_customlink=custom_url).exists():
                custom_url_ = Profile_database.objects.get(steam_customlink=custom_url)
                tranform_to_id = custom_url_.steam_link_id
                return redirect('profile_url', tranform_to_id)


            valuedata = check_for_id(steam_id, custom_url, steam_API=steam_API)
            if type(valuedata) == str:
                searchprofileform = SearchProfileForm()
                return render(request, 'checker/main.html', {'searchprofileform': searchprofileform, 'valuedata': valuedata})

            else:
                complit = to_data_base(valuedata=valuedata)
                return redirect('profile_url', complit)


    else:
        searchprofileform = SearchProfileForm()

    return render(request, 'checker/main.html', {'searchprofileform': searchprofileform})


def profile_page(request, steam_id):
    get_obj = Profile_database.objects.get(steam_link_id=steam_id)
    time_calculator = datetime.datetime.fromtimestamp(int(get_obj.time_created))
    if 'none' in get_obj.economyBan:
        trade_ban = 'False'
    else:
        trade_ban = 'True'
    if trade_ban == 'True' or get_obj.communityBanned == 'True' or get_obj.vacbanned == 'True':
        check_mark_banned = 'True'
    else:
        check_mark_banned = 'False'

    context = {
        'nickname': get_obj.nickname,
        'account_level': get_obj.player_lvl,
        'time_created': time_calculator,
        'trade_ban': trade_ban,
        'avatar_full': get_obj.avatar_url,
        'communityban': get_obj.communityBanned,
        'vac_ban': get_obj.vacbanned,
        'check_mark_banned': check_mark_banned,
        'steam_id': steam_id,
    }
    return render(request, 'checker/profile.html', context)

def about(request):
    return render(request, 'checker/about.html')
