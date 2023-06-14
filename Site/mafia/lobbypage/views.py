from django.shortcuts import render
import json
from user_profile.models import Profile
from .models import Rooms
from .forms import CreateTheRoom
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from agora_token_builder import RtcTokenBuilder
from user_profile.models import Friend


from asgiref.sync import sync_to_async
from .game_consumer import ServerConsumer
from channels.layers import get_channel_layer
import threading

import time
# Create your views here.

def lobby(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            NewRoom = CreateTheRoom(request.POST)
            if NewRoom.is_valid():
                NewRoom = NewRoom.save(commit=False)
                NewRoom.roomhostid = request.user.profile.pk
                NewRoom.save()
                GameMaster = ServerConsumer(get_channel_layer(), NewRoom.roomname+"_"+NewRoom.room_id, NewRoom.id)
                print("======================================================")
                thread = threading.Thread(target=GameMaster.Update)
                thread.start()
                print("======_________++++++++++++++++++++++++++")
                return redirect(TheLobby, NewRoom.roomname+"_"+NewRoom.room_id)
        data = {}

        form = CreateTheRoom()


        data['form'] = form
        return render(request, 'lobbypage/lobbyindex.html', data)

    else:
        return HttpResponse('ЭЭЭЭЭ, залогинся!')

def TheLobby(request, room_name):
    appId = '55fba11738094971a032a7ac307e10ed'
    appCertificate = 'b006d5596a3c4c1eaa51f546abfad7ad' #Брать из дискорда - странная херня в предпоследнем сообщении!! и УДАЛЯТЬ!!! 11111111111111111111111111111111111111111111111111111111111111111111111111
    player = request.user.profile
    uid = 0
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1
    if player.related_lobby_id == None:
        print("!!!!!!!!!!!!!!!!!!!!ПОЛЬЗОВАТЕЛЬ", player.nickname, " ЗАШЕЛ В ЗЭ ЛОББИ!!!!!!!!!!!!!!")
        for room in Rooms.objects.all():
            print(room.roomname+"_"+room.room_id)
            if room.roomname+"_"+room.room_id == room_name:
                if room.profile_set.count() < 12 and (room.is_game == False or str(player.pk) in list(room.votelist.keys())):
                    print("!!!!!!!!ВЫБРАНА КОМНАТА", room.roomname)
                    room.profile_set.add(player, bulk=False)
                    room.CheckPlayers()  #Cheking!!!!!
                    #room.save()
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    channelName = str(room_name)
                    return render(request, 'lobbypage/lobbypage.html',
                              {'request': request,
                               'room_name_json': mark_safe(json.dumps(room_name)),
                               'user_nickname_json': mark_safe(json.dumps(player.nickname)),
                               'user_pk_json': mark_safe(json.dumps(str(player.pk))),
                               'room_isgame_json' : mark_safe(json.dumps(room.is_game)),
                               'the_host_json': mark_safe(json.dumps(request.user.profile.pk == room.roomhostid)),
                               'friends': Friend.objects.get(related_user=request.user).friends.all(),
                               'agora_token' : mark_safe(json.dumps(RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)))
                               })
                else:
                    return HttpResponse('Народу многа....')
        return HttpResponse('Куда прёшь? Не видишь? Такой комнаты вообще нет.')
    else:
        return redirect(TheLobby, room_name)


def lobbylist(request):
    allTable = Rooms.objects.all()
    return render(request, 'lobbypage/lobbylist.html', {'rooms': allTable})

