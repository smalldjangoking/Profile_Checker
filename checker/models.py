from django.db import models

# Create your models here.

from django.db import models

class Profile_database(models.Model):
    steam_link_id = models.TextField()
    nickname = models.TextField()
    steam_customlink = models.TextField(blank=True)
    ban = models.TextField()
    profile_data = models.TextField()
    player_lvl = models.TextField(blank=True)
    time_created = models.TextField()
    Trade_Ban = models.TextField()
    VAC_Ban = models.TextField()
    CommunityBanned = models.TextField()
    avatar_url = models.URLField()

    def __str__(self):
        return f'Profile of: {self.steam_link_id}'



