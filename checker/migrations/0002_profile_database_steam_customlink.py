# Generated by Django 4.2.2 on 2023-06-13 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile_database',
            name='steam_customlink',
            field=models.TextField(blank=True),
        ),
    ]
