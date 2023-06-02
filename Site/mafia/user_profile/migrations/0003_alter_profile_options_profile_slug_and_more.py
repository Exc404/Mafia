# Generated by Django 4.1.7 on 2023-06-01 12:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile', '0002_profile_delete_userprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Профиль', 'verbose_name_plural': 'Профили'},
        ),
        migrations.AddField(
            model_name='profile',
            name='slug',
            field=models.SlugField(default='profile', unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='micro_index',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(-1)], verbose_name='Выбранный микрофон'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='micro_value_lvl',
            field=models.IntegerField(default=50, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Громкость микрофона'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(max_length=20, verbose_name='Никнейм'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(default='profileImg/AnonIcon.jpg', upload_to='profileImg/', verbose_name='Фото профиля'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='related_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Аккаунт профиля'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='webcam_index',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(-1)], verbose_name='Выбранная камера'),
        ),
    ]