from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.
class Rooms(models.Model):
    RoomName = models.CharField(max_length=40)
    RoomHostName = models.CharField(max_length=20)
    RoomID = models.CharField(max_length=8)
    UsersAmount = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(10)], default = 1)
    IsGame = models.BooleanField(default=0)

    def __str__(self):
        return self.RoomName