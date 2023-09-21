from checker.models import Profile_database
def authenticated_user(request):
    current_user = request.user if request.user.is_authenticated else None
    if current_user:
        steam_id = current_user.social_auth.get(provider='steam').uid
        user_data_info = Profile_database.objects.get(steam_link_id=steam_id)

        return {'user_avatar_s': user_data_info.avatar_s}


    return {'user_avatar_s': 'None'}