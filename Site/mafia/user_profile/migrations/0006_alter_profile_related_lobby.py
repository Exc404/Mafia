# Generated by Django 4.1.7 on 2023-06-02 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lobbypage', '0006_rename_isgame_rooms_is_game_and_more'),
        ('user_profile', '0005_merge_20230602_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='related_lobby',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lobbypage.rooms', verbose_name='Связанное лобби'),
        ),
    ]