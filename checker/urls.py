from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('auth/', include('social_django.urls', namespace='social')),
    path('my_admin/', admin.site.urls),
    path('', views.main_page, name='main_url'),
    path('account', views.profile, name='account'),
    path('profile/<int:steam_id>', views.profile_page, name='profile_url'),
    path('about', views.about, name='about_admin'),
    path('logout', views.custom_logout, name='custom_logout'),
]