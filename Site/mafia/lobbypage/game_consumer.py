from asgiref.sync import async_to_sync
from .models import Rooms

class ServerConsumer():
    #конструктор
    def __init__(self, channel_layer, group_name, id):
        self.channel_layer = channel_layer
        self.group_name = 'lobby_' + group_name
        self.id = id
        print("00000000000000000000000000000000000000")
    
    #функция обновления
    def Update(self):
        print("1111111111111111111111111111111111111111111111111111111111111111111000000000000000000000000000000000000000000")
        while(True):
            try: 
                thisroom = Rooms.objects.get(id = self.id)
                if(thisroom.is_game):
                    async_to_sync(self.channel_layer.group_send)(
                        self.group_name,
                        {
                            'type' : 'message_sending',
                            'message' : 'АХАХАХАХ, Я ЕБАНУТЫЙ'
                        }
                    )
            except Rooms.DoesNotExist:
                break
