import json
from django.shortcuts import render
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from user_profile.models import Profile
from .models import Rooms


class TestConsumer(WebsocketConsumer):

    def connect(self):
        self.username = ""
        self.room_group_name = 'lobby_'
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
            self.room_group_name += text_data_json['roomname']
            async_to_sync(self.channel_layer.group_add) (
                self.room_group_name,
                self.channel_name
            )
            print(self.username + "$")

    def test_sending(self, event):
        message = event['message']
        self.send(text_data = json.dumps({
            'type' : 'chat',
            'message' :  message,
        }))

    def disconnect(self, code):
        thisuser = Profile.objects.get(nickname=self.username)
        thisroom = Rooms.objects.get(id=thisuser.related_lobby_id)
        thisroom.profile_set.remove(thisuser)
        thisuser.related_lobby_id = None
        thisuser.save()
        thisroom.DelPlayer(thisuser.pk)
        print("Disconnect!")
