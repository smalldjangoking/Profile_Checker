from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('my_admin/', admin.site.urls),
    path('', views.main_page, name='main_url'),
    path('profile/<int:steam_id>', views.profile_page, name='profile_url'),
    path('about', views.about),
]