from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class Rooms(models.Model):

    def __int__(self):
        super(self).__init__()

    PlayerList = []
    roomname = models.CharField(blank=False, max_length=40)
    roomHostName = models.CharField(max_length=20)
    roomID = models.CharField(max_length=8, default="STOCKID")
    UsersAmount = models.IntegerField(validators=[MinValueValidator(-1), MaxValueValidator(12)], default = 0)
    IsGame = models.BooleanField(default=0)

    def AddPlayer(self, Username):
        self.PlayerList.append(Username)
        self.UsersAmount+=1

    def DelPlayer(self, Username):
        print("WANNA DELETE:", Username)
        print("FROM:", self.PlayerList)
        self.PlayerList.remove(Username)
        self.UsersAmount-=1
        if len(self.PlayerList)==0 and self.UsersAmount==0:
            self.delete()

    def CheckPlayers(self):  #debug thing
        print("CHECKING!!!", self.PlayerList)

    def __str__(self):
        return self.roomname
