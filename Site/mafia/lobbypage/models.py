from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.
class Rooms(models.Model):

    def __init__(self, *args, **kwargs):
        self.PlayerList = []
        super().__init__(*args, **kwargs)

    roomname = models.CharField(blank=False, max_length=40)
    roomHostName = models.CharField(max_length=20)
    roomID = models.CharField(max_length=8, default="STOCKID")
    UsersAmount = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(10)], default = 0)
    IsGame = models.BooleanField(default=0)

    def AddPlayer(self, Username):
        self.PlayerList.append(Username)

    def DelPlayer(self, Username):
        self.PlayerList.remove(Username)
        if len(self.PlayerList)==0:
            self.delete()


    def __str__(self):
        return self.roomname
