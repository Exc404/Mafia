import json
from django.shortcuts import render
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from user_profile.models import Profile
from .models import Rooms
from random import choice

class TestConsumer(WebsocketConsumer):

    def connect(self):
        self.username = ""
        self.GameRole = "homo"
        self.uid = ""
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'lobby_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add) (
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        if 'message' in text_data_json:
            message = text_data_json['message']
            async_to_sync(self.channel_layer.group_send) (
                self.room_group_name,
                {
                    'type' : 'test_sending',
                    'message' : message,
                }
            )
        
        if 'username' in text_data_json and self.username=="":
            self.username = text_data_json['username']
            print(self.username + "$")
        
        if 'users' in text_data_json:
            self.usersid = text_data_json['users']
            self.uid = text_data_json['hostuid']
            thisuser = Profile.objects.get(nickname=self.username)
            thisroom = Rooms.objects.get(id=thisuser.related_lobby_id)
            thisroom.is_game = True
            thisroom.save()
            print(self.usersid)
            print("\n")
            print(self.uid)
            Roles = {"mafia" : 1, "doc": 1, "com":1, "civil": 1}
            playerroles = {}
            #self.GameRole = choice(list(Roles.keys()))
            self.GameRole = "mafia"
            print("HOST ROLE ", self.GameRole)
            Roles[self.GameRole]-=1
            playerroles[str(self.uid)] = self.GameRole
            for pluid in self.usersid:
                newrole = choice(list(Roles.keys()))
                while Roles[newrole]==0:
                    newrole = choice(list(Roles.keys()))
                playerroles[pluid] = newrole
                Roles[newrole]-=1
            async_to_sync(self.channel_layer.group_send) (
                self.room_group_name,
                {
                    'type' : 'roles_sending',
                    'players_roles' : playerroles
                }
            )

        if 'roleslist' in text_data_json:
            if self.uid == "":
                self.uid = text_data_json['socket_uid']
            temproles = text_data_json['roleslist']
            print("Принятые роли с юайди:\n", temproles, self.uid)
            if self.GameRole == "homo":
                self.GameRole = temproles[str(self.uid)]
            print(self.username, "Ваша роль - ", self.GameRole)


        if 'user_name' in text_data_json:
            async_to_sync(self.channel_layer.group_send) (
                self.room_group_name,
                {
                    'type' : 'user_info_sending',
                    'user_name' : text_data_json['user_name'],
                    'uid' : str(text_data_json['uid'])
                }
            )

        if 'vote_uid' in text_data_json:
            vote = text_data_json['vote_uid']
            vote = vote.replace("vote-", "")
            async_to_sync(self.channel_layer.group_send) (
                self.room_group_name,
                {
                    'type' : 'vote_sending',
                    'vote' : vote,
                }
            )
    def vote_sending(self, event):
        vote = event['vote']
        self.send(text_data = json.dumps({
            'type' : 'vote_sending',
            'vote' : vote
        }))


    def roles_sending(self, event):
        roleslist = event['players_roles']
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", roleslist)
        self.send(text_data = json.dumps({
            'type' : 'game_roles',
            'roleslist' : roleslist
        }))

    def user_info_sending(self, event):
        user_name = event['user_name']
        uid = event['uid']
        self.send(text_data = json.dumps({
            'type' : 'user_info',
            'user_name' : user_name,
            'uid' : uid
        }))

    def test_sending(self, event):
        message = event['message']
        self.send(text_data = json.dumps({
            'type' : 'chat',
            'message' :  message,
            'role' : self.GameRole
        }))

    def disconnect(self, code):
        print("!!!!!!!!!!!!!!КОНСУМЕР ВЫШЕЛ ПОТОМУШТА ", code)
        thisuser = Profile.objects.get(nickname=self.username)
        thisroom = Rooms.objects.get(id=thisuser.related_lobby_id)
        #thisroom.profile_set.remove(thisuser)
        thisuser.related_lobby_id = None
        thisuser.save()
        thisroom.DelPlayer(thisuser.pk)
        print("Disconnect!")
