# Generated by Django 4.2.2 on 2023-06-14 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0003_profile_database_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile_database',
            name='player_lvl',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]