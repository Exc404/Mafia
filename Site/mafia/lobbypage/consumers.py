import json
from django.shortcuts import render
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from user_profile.models import Profile
from .models import Rooms

class TestConsumer(WebsocketConsumer):

    def connect(self):
        self.username = ""
        self.pk = ""
        self.role = ""
        self.chatlock = False
        self.votelock = True
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
            self.pk = text_data_json['pk']
            print(self.username + "$")
            print(self.pk + "$")

        if 'user_name' in text_data_json:
            async_to_sync(self.channel_layer.group_send) (
                self.room_group_name,
                {
                    'type' : 'user_info_sending',
                    'user_name' : text_data_json['user_name'],
                    'uid' : str(text_data_json['uid']),
                    'pk' : str(text_data_json['pk'])
                }
            )
        
        if 'start' in text_data_json:
            thisuser = Profile.objects.get(nickname=self.username)
            thisroom = Rooms.objects.get(id=thisuser.related_lobby_id)
            thisroom.is_game = True
            thisroom.save()
            
        if 'vote_pk' in text_data_json:
            votepk = text_data_json['vote_pk']
            thisuser = Profile.objects.get(nickname=self.username)
            thisroom = Rooms.objects.get(id=thisuser.related_lobby_id)
            thisroom.votelist[votepk]+=1
            thisroom.save()

    def night(self,event):
        killed = event["voteresult"]
        if killed == self.pk:
            print("YOU'VE BEEN KILLED!!!!")
            self.role = "spec"
        self.send(text_data = json.dumps({
            'type' : 'night_results',
            'votetarget' : killed,
            'targetname' : event['votedname'],
        }))

    def morning(self,event):
        killed = event["killresult"]
        saved = event["healsuccess"]
        if killed == self.pk and saved==0:
            print("YOU'VE BEEN KILLED!!!!")
            self.role = "spec"
        self.send(text_data = json.dumps({
            'type' : 'morning_results',
            'killtarget' : killed,
            'targetname' : event['killedname'],
            'healresult' : saved,
            'checked' : event['checkresult']
        }))

    def update_roles(self,event):
        self.role = event['rolelist'][self.pk]
        self.send(text_data = json.dumps({
            'type' : 'update_roles',
            'rolelist' : event['rolelist']
        }))

    def new_turn(self,event):
        turn = event['new_turn']
        if (self.role == turn or turn=="civilchat" or turn=="civilvote") and self.role!="spec":
            self.chatlock = False
            if turn=="civilchat" : self.votelock=True
            else: self.votelock = False
        else:
            self.chatlock = True
            self.votelock = True
        print(self.chatlock)
        self.send(text_data = json.dumps({
            'type' : 'turn_info',
            'chatlock' : self.chatlock,
            'votelock' : self.votelock,
            'turnnumber' : event['turn_number']
        }))

    def vote_result(self,event):
        self.send(text_data = json.dumps({
            'type' : 'vote_result',
            'resultpk' : event['resultpk'],
            'resultname' : event['resultname']
        }))

    def game_starts(self, event):
        rolelist = event['roleslist']
        self.role = rolelist[str(self.pk)]
        print("Моя роль - ", self.role)
        self.send(text_data = json.dumps({
            'type' : 'start_info',
            'rolelist' : rolelist
        }))

    def user_info_sending(self, event):
        user_name = event['user_name']
        uid = event['uid']
        pk = event['pk']
        # print("SELF PK", self.pk, self.username)
        self.send(text_data = json.dumps({
            'type' : 'user_info',
            'user_name' : user_name,
            'pk' : pk,
            'uid' : uid
        }))

    def message_sending(self, event):
        message = event['message']
        self.send(text_data = json.dumps({
            'type' : 'chat',
            'message' :  message,
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
