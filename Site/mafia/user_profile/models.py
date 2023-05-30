from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.

class Profile(models.Model):
    profile_img = models.ImageField(upload_to='profileImg/', default='profileImg/AnonIcon.png', blank=False)
    nickname = models.CharField(max_length=20, blank=False)
    micro_value_lvl = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)], default=50)
    micro_index = models.IntegerField(validators=[MinValueValidator(-1)], default=0)
    webcam_index = models.IntegerField(validators=[MinValueValidator(-1)], default=0)
    related_user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.nickname + ' @' + self.related_user.username
