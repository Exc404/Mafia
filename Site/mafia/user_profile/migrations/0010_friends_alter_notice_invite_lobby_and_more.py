# Generated by Django 4.1.7 on 2023-06-07 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lobbypage', '0008_delete_roommember'),
        ('user_profile', '0009_alter_notice_invite_lobby_alter_notice_sender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend_1', models.IntegerField()),
                ('friend_2', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='notice',
            name='invite_lobby',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lobbypage.rooms', verbose_name='Лобби из приглашения'),
        ),
        migrations.AlterField(
            model_name='notice',
            name='text_message',
            field=models.CharField(blank=True, max_length=40, verbose_name='Сообщение'),
        ),
    ]
