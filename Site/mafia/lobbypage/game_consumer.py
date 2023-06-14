from asgiref.sync import async_to_sync
from .models import Rooms
from user_profile.models import Profile
from user_profile.models import GameHistory
from random import choice
from threading import Timer
from time import sleep
from copy import copy
import datetime

class ServerConsumer():
    #конструктор
    def __init__(self, channel_layer, group_name, id):
        self.channel_layer = channel_layer
        self.group_name = 'lobby_' + group_name
        self.id = id
        self.message = ""
        self.turn = -1
        self.loop = 0
        print("00000000000000000000000000000000000000")
        self.killtarget = ""
        self.healtarget = ""
        self.checktarget = ""
        self.votetarget = ""
        self.killedname = ""
        self.votename = ""
        self.firstroles = {}

    #функция обновления
    def Update(self):
        print("1111111111111111111111111111111111111111111111111111111111111111111000000000000000000000000000000000000000000")
        while(True):
            try: 
                thisroom = Rooms.objects.get(id = self.id)
                if(thisroom.is_game):
                    Gamepath = ["mafia", "doc", "com", "civilchat", "civilvote"]
                    players_amount = thisroom.profile_set.count()
                    if players_amount > 0:
                        votelist = {}
                        roles = {"mafia": players_amount//4, "com" : 1, "doc" : 1, "civil" : players_amount-1-1-(players_amount//4)}
                        players = thisroom.profile_set.all()
                        for guy in players:
                            votelist[guy.pk] = 0
                            thisroom.votelist = votelist
                            thisroom.save()
                        rolelist = {}
                        for pl in players:
                            temprole = choice(list(roles.keys()))
                            while roles[temprole]==0:
                                temprole = choice(list(roles.keys()))
                            rolelist[str(pl.pk)] = temprole
                            roles[temprole] -= 1
                        if(self.firstroles == {}):
                            self.firstroles = copy(rolelist)
                            print("-------------------------self.firstroles-----------------------------", self.firstroles)
                        async_to_sync(self.channel_layer.group_send)(
                            self.group_name,
                            {
                                'type' : 'game_starts',
                                'roleslist' : rolelist 
                            }
                        )
                        print(rolelist)
                        #Начало геймплея тут vvvvvv
                        while True:
                            if(self.turn!=-1):
                                thisroom = Rooms.objects.get(id = self.id)
                                tempvotelist = thisroom.votelist
                                print(tempvotelist)
                                tempmax=0
                                result = ""
                                result_name = ""
                                for player in list(tempvotelist.keys()):
                                    if tempvotelist[player]>tempmax:
                                        tempmax = tempvotelist[player]
                                        result = player
                                if list(tempvotelist.values()).count(tempmax)==1 and tempmax!=0:
                                    print(result)
                                    result_name = Profile.objects.get(pk=result).nickname
                                    match self.turn:
                                        case 0: 
                                            self.killtarget = result
                                            self.killedname = result_name
                                        case 1: self.healtarget = result
                                        case 2: self.checktarget = result
                                        case 4: 
                                            self.votetarget = result
                                            self.votename = result_name
                                    async_to_sync(self.channel_layer.group_send)(
                                        self.group_name,
                                        {
                                            'type' : 'vote_result',
                                            'resultpk' : result,
                                            'resultname' : result_name 
                                        }
                                    )
                                else:
                                    print("SABOTAGE")
                                for player in list(tempvotelist.keys()):
                                    tempvotelist[player] = 0
                                thisroom.votelist = tempvotelist
                                thisroom.save()
                            self.turn+=1

                            if self.turn == 5:
                                self.turn = 0
                                self.loop +=1
                            
                            #ПРОВЕРКА НА ЛИВНУВШИХ
                            thisroom = Rooms.objects.get(id = self.id)
                            players_now = [] 
                            for pl in thisroom.profile_set.all():
                                players_now.append(str(pl.pk))
                            print("ИГРОКИ СЕЙЧАС:", players_now)
                            print("ИГРОКИ В БАЗЕ",  rolelist)
                            for pl in list(rolelist.keys()):
                                if pl not in players_now:
                                    print("105ая строка пройдена!")
                                    if Gamepath[self.turn] == rolelist[pl]:
                                        rolelist[pl] = "spec"
                                        print("РОЛИ ИЗМЕНЕНЫ!", rolelist)
                            async_to_sync(self.channel_layer.group_send)(
                                self.group_name,
                                {
                                    'type' : 'update_roles',
                                    'rolelist' : rolelist  
                                }
                            )
                            #ПРОВЕРКА НА ЛИВНУВШИХ ЗАКОНЧИЛАСЬ

                            if self.turn == 3:
                                if self.killtarget == self.healtarget: healsuccsess = 1
                                else: 
                                    healsuccsess = 0
                                    rolelist[self.killtarget] = "spec"
                                checked_name=""
                                if self.checktarget!="":
                                    checked_name = rolelist[self.checktarget]
                                async_to_sync(self.channel_layer.group_send)(
                                    self.group_name,
                                    {
                                        'type' : 'morning',
                                        'killresult' : self.killtarget,
                                        'killedname' : self.killedname,
                                        'healsuccess' : healsuccsess,
                                        'checkresult' : checked_name
                                    }
                                )
                                self.killtarget = ""
                                self.healtarget = ""
                                self.checktarget = ""
                                self.killedname = ""
                            if self.turn == 0 and self.votename!="":
                                rolelist[self.votetarget] = "spec"
                                async_to_sync(self.channel_layer.group_send)(
                                    self.group_name,
                                    {
                                        'type' : 'night',
                                        'voteresult' : self.votetarget,
                                        'votedname' : self.votename,
                                    }
                                )
                                self.votetarget = ""
                                self.votename = ""

                            darkcount = list(rolelist.values()).count("mafia")
                            lightcount = list(rolelist.values()).count("civil") + list(rolelist.values()).count("doc") + list(rolelist.values()).count("com")
                            if (darkcount >= lightcount or darkcount == 0):
                                NewGameHistory = GameHistory()
                                NewGameHistory.roomname = Rooms.objects.get(id = self.id).roomname
                                if darkcount >= lightcount:
                                    NewGameHistory.win = "0"
                                elif darkcount == 0:
                                    NewGameHistory.win = "1"
                                NewGameHistory.data = datetime.date.today()
                                print("++++++++++++++++++++++++++++self.firstroles+++++++++++++++++++++++++++++++++++++", self.firstroles)
                                NewGameHistory.playerlist = self.firstroles
                                NewGameHistory.save()
                                for pl in players:
                                    NewGameHistory.players.add(pl)
                                NewGameHistory.save()
                                async_to_sync(self.channel_layer.group_send)(
                                    self.group_name,
                                    {
                                            'type' : 'end_game',
                                            'winner' : NewGameHistory.win,
                                    }
                                )
                                thisroom = Rooms.objects.get(id = self.id)
                                thisroom.votelist = {}
                                thisroom.save()
                                break

                            async_to_sync(self.channel_layer.group_send)(
                                self.group_name,
                                {
                                    'type' : 'new_turn',
                                    'new_turn' : Gamepath[self.turn],
                                    'turn_number' : self.turn,
                                    'loop_number' : self.loop 
                                }
                            )  
                            sleep(20)
                        thisroom.is_game = False
                        self.killtarget = ""
                        self.healtarget = ""
                        self.checktarget = ""
                        self.votetarget = ""
                        self.killedname = ""
                        self.votename = ""
                        self.message = ""
                        self.turn = -1
                        self.loop = 0
                        thisroom.save()
            except Rooms.DoesNotExist:
                break
