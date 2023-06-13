from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from lobbypage.models import Rooms


class Profile(models.Model):

    profile_img = models.ImageField(upload_to='profileImg/', default='profileImg/AnonIcon.jpg', blank=False,
                                    verbose_name='Фото профиля')
    nickname = models.CharField(max_length=20, blank=False, verbose_name='Никнейм')
    slug = models.SlugField(max_length=50, blank=True, unique=True, db_index=True, verbose_name='URL')
    micro_value_lvl = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)], default=50,
                                          verbose_name='Громкость микрофона')
    micro_index = models.IntegerField(validators=[MinValueValidator(-1)], default=0, verbose_name='Выбранный микрофон')
    webcam_index = models.IntegerField(validators=[MinValueValidator(-1)], default=0, verbose_name='Выбранная камера')
    related_user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Аккаунт профиля')
    related_lobby = models.ForeignKey(Rooms, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Связанное лобби')

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


    def __str__(self):
        return self.nickname + ' @' + self.related_user.username

    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.nickname) + str(self.related_user.pk))
        super(Profile, self).save(*args, **kwargs)




class GameHistory(models.Model):

    roomname = models.CharField(blank=False, max_length=40)
    data =  models.DateField()
    win = models.IntegerField(default = -1)
    playerlist = models.JSONField(null = True, default = dict)
    players = models.ManyToManyField(Profile)
