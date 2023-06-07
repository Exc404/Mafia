from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from lobbypage.models import Rooms
from django.utils.translation import gettext_lazy as _


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
    related_lobby = models.ForeignKey(Rooms, on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='Связанное лобби')

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.nickname + ' @' + self.related_user.username

    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.nickname) + '-id' + str(self.related_user.pk))
        super(Profile, self).save(*args, **kwargs)


class Notice(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Отправитель')
    addressee = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False, verbose_name='Адресат')
    datetime = models.DateTimeField(auto_now_add=True)
    invite_lobby = models.ForeignKey(Rooms, on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name='Лобби из приглашения')

    class NoticeType(models.TextChoices):
        FRIENDSHIP = "FR", _("Friendship")
        INVITE = "IV", _("Invite")
        INFO = "IF", _("Info")

    notice_type = models.CharField(max_length=2, choices=NoticeType.choices, default=NoticeType.INFO,
                                   verbose_name='Тип уведомления', blank=False)

    text_message = models.CharField(max_length=40, verbose_name='Сообщение', blank=True)

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        str_type = ''
        if self.notice_type == self.NoticeType.INFO:
            str_type = 'INFO для ' + self.addressee.nickname
        elif self.notice_type == self.NoticeType.FRIENDSHIP:
            str_type = 'FRIENDSHIP для ' + self.addressee.nickname
        elif self.notice_type == self.NoticeType.INVITE:
            str_type = 'INVITE для ' + self.addressee.nickname
        return str_type

    def save(self, *args, **kwargs):
        if (len(str(self.text_message)) - str(self.text_message).count(" ") == 0
            and self.notice_type == self.NoticeType.INFO) \
                or (self.sender == None and self.notice_type != self.NoticeType.INFO) \
                or (self.sender != None and self.sender.profile == self.addressee):
            return

        if self.notice_type == self.NoticeType.INFO:
            self.text_message = str(self.text_message).capitalize()
        elif self.notice_type == self.NoticeType.FRIENDSHIP:
            self.text_message = self.sender.profile.nickname + ' хочет добавить вас в друзья!'
        elif self.notice_type == self.NoticeType.INVITE:
            self.text_message = self.sender.profile.nickname + ' приглашает вас в игру!'

        super(Notice, self).save(*args, **kwargs)


class Friend(models.Model):
    related_user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Аккаунт профиля')
    friends = models.ManyToManyField(Profile)

    def __str__(self):
        return 'Друзья ' + self.related_user.profile.nickname

    def save(self, *args, **kwargs):
        super(Friend, self).save(*args, **kwargs)
