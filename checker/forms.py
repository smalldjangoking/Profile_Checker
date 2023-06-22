from django import forms
import re
from django.utils.safestring import mark_safe

error_message = mark_safe('<span style="color: red;">Неправильный формат ввода данных!</span><br>'
                          '<span style="color: red;">Символы !@#$%^&* не допускаются.</span><br><br>'
                          'Введите пожалуйста следующие форматы:<br>'
                          'steamID => 76561198358527542<br>'
                          'customID => 123s<br>'
                          'steamID_link => https://steamcommunity.com/profiles/76561198080756014<br>'
                          'steam_Custom_link => https://steamcommunity.com/id/123SSS')

class SearchProfileForm(forms.Form):
    search_form = forms.CharField(label='', max_length=200, widget=forms.TextInput(
        attrs={'class': "form-control text-center", 'id': "floatingInputValue",
               'placeholder': "ProfileLink/SteamID/CustomID"}))

    def clean_search_form(self):
        search_value = self.cleaned_data['search_form']

        # Проверка на steamID or link or CustormURL
        if re.search(r'[!@#$%^&*()+=-]', search_value):
            raise forms.ValidationError(error_message)

        #проверка на существующий аккаунт
        if re.search(r'[!@#$%^&*()+=-]', search_value):
            raise forms.ValidationError(error_message)

        if search_value.isnumeric():
            steamID = search_value
            customURL = None

        elif search_value.endswith('/'):
            if search_value.split('/')[-2].isnumeric():
                steamID = str(search_value.split('/')[-2])
                customURL = None
            elif '.com' in search_value:
                steamID = None
                customURL = str(search_value.split('/')[-2])

        elif 'com' in search_value:
            if search_value.split('/')[-1].isnumeric():
                steamID = str(search_value.split('/')[-1])
                customURL = None
            elif '.com' in search_value:
                steamID = None
                customURL = str(search_value.split('/')[-1])

        elif ']' not in search_value or 'STEAM_' not in search_value:
            steamID = None
            customURL = search_value

        return {'steam_id': steamID, 'custom_url': customURL}