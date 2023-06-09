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
                    'type' : 'message_sending',
                    'message' : message,
                }
            )
        
        if 'username' in text_data_json and self.username=="":
            self.username = text_data_json['username']
            print(self.username + "$")

        if 'user_name' in text_data_json:
            async_to_sync(self.channel_layer.group_send) (
                self.room_group_name,
                {
                    'type' : 'user_info_sending',
                    'user_name' : text_data_json['user_name'],
                    'uid' : str(text_data_json['uid'])
                }
            )

    def user_info_sending(self, event):
        user_name = event['user_name']
        uid = event['uid']
        self.send(text_data = json.dumps({
            'type' : 'user_info',
            'user_name' : user_name,
            'uid' : uid
        }))

    def message_sending(self, event):
        message = event['message']
        self.send(text_data = json.dumps({
            'type' : 'chat',
            'message' :  message,
            'role' : self.GameRole,
            'nickname' : self.username
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
