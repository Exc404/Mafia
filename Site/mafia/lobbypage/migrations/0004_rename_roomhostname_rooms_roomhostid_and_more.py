# Generated by Django 4.1.7 on 2023-05-31 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobbypage', '0003_rooms_players_alter_rooms_usersamount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rooms',
            old_name='roomHostName',
            new_name='roomHostId',
        ),
        migrations.AlterField(
            model_name='rooms',
            name='players',
            field=models.CharField(blank=True, default='', max_length=84),
        ),
    ]
