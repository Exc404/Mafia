# Generated by Django 4.1.7 on 2023-05-31 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobbypage', '0005_remove_rooms_players'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rooms',
            old_name='IsGame',
            new_name='is_game',
        ),
        migrations.RenameField(
            model_name='rooms',
            old_name='roomID',
            new_name='room_id',
        ),
        migrations.RemoveField(
            model_name='rooms',
            name='UsersAmount',
        ),
        migrations.RemoveField(
            model_name='rooms',
            name='roomHostId',
        ),
        migrations.AddField(
            model_name='rooms',
            name='roomhostid',
            field=models.IntegerField(default=0),
        ),
    ]