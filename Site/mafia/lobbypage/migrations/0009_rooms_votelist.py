# Generated by Django 4.1.7 on 2023-06-10 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobbypage', '0008_delete_roommember'),
    ]

    operations = [
        migrations.AddField(
            model_name='rooms',
            name='votelist',
            field=models.JSONField(null=True),
        ),
    ]
