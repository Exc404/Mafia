import json
from django.shortcuts import render
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1", self.room_group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'test_sending',
                'message': message
            }
        )

    def test_sending(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))

    def disconnect(self, code):
        print("Disconnect")
