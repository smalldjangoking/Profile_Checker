# Generated by Django 4.2.2 on 2023-06-15 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0008_alter_profile_database_communitybanned_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile_database',
            name='Trade_Ban',
            field=models.BooleanField(null=True),
        ),
    ]
