from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from random import choice
# Create your models here.
class Rooms(models.Model):

    roomname = models.CharField(blank=False, max_length=40)
    roomhostid = models.IntegerField(default = 0)
    room_id = models.CharField(max_length=8, default="STOCKID")
    is_game = models.BooleanField(default=0)

    def DelPlayer(self, userid):
        if self.roomhostid == userid and self.profile_set.count()>0:
            players = self.profile_set.all()
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(players[0].pk)
            #print(self.profile_set.count())
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
            self.roomhostid = players[0].pk
            self.save()
        if self.profile_set.count() == 0:
            self.delete()
        print("WANNA DELETE:")

    
    def GetLink(self):
        link = self.roomname + '_' + self.room_id
        return link

    def CheckPlayers(self):  #debug thing
        print("CHECKING!!!", self.profile_set.count())

    def __str__(self):
        return self.roomname + ' ' + str(self.profile_set.count()) + '/12 '

