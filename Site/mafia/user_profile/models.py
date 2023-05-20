from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.

class Profile(models.Model):
    profile_img = models.ImageField(upload_to='profileImg/', default='profileImg/AnonIcon.png')
    nickname = models.CharField(max_length=100)
    micro_value_lvl = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)], default=50)
    micro_index = models.IntegerField(validators=[MinValueValidator(-1)], default=0)
    webcam_index = models.IntegerField(validators=[MinValueValidator(-1)], default=0)
    related_user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname
