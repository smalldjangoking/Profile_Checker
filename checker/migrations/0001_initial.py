# Generated by Django 4.2.2 on 2023-06-13 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile_database',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('steam_link_id', models.TextField()),
                ('ban', models.TextField()),
                ('profile_data', models.TextField()),
            ],
        ),
    ]
