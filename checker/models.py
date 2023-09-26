from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile_database(models.Model):
    steam_link_id = models.TextField()
    nickname = models.TextField()
    steam_customlink = models.TextField(blank=True, null=True)
    avatar_s = models.URLField(blank=True)
    player_lvl = models.TextField(blank=True, null=True)
    time_created = models.TextField(blank=True, null=True)
    economyBan = models.TextField()
    vacbanned = models.TextField()
    communityBanned = models.TextField()
    avatar_url = models.URLField()

    def __str__(self):
        return f'Profile of: {self.steam_link_id}'




