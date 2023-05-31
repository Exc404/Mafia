from django.shortcuts import render
import json
from user_profile.models import Profile
from .models import Rooms
from .forms import CreateTheRoom
from django.http import HttpResponse
from django.shortcuts import redirect
import mysql.connector
from django.utils.safestring import mark_safe
# Create your views here.

Names = ["","","null"]
def lobby(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            NewRoom = CreateTheRoom(request.POST)
            if NewRoom.is_valid():
                NewRoom = NewRoom.save(commit=False)
                NewRoom.roomHostName = request.user.profile.nickname
                NewRoom.save()
                return redirect(TheLobby, NewRoom.roomname+"_"+NewRoom.roomID)
        data = {}

        form = CreateTheRoom()


        data['form'] = form
        return render(request, 'lobbypage/lobbyindex.html', data)

    else:
        return HttpResponse('ЭЭЭЭЭ, залогинся!')

def TheLobby(request, room_name):
    player = request.user.profile
    for room in Rooms.objects.all():
        print(room.roomname+"_"+room.roomID)
        if room.roomname+"_"+room.roomID == room_name:
            if room.UsersAmount<12:
                print("!!!!!!!!ВЫБРАНА КОМНАТА", room.roomname)
                room.AddPlayer(player.nickname)
                room.CheckPlayers()
                room.profile_set.add(player, bulk=False)
                room.save()
                for R in Rooms.objects.all():
                    print(R.roomname, R.PlayerList)
                return render(request, 'lobbypage/lobbypage.html',
                              {'request': request,
                               'room_name_json': mark_safe(json.dumps(room_name)),
                               'user_nickname_json': mark_safe(json.dumps(player.nickname))
                               })
            else:
                return HttpResponse('Народу многа....')
    return HttpResponse('Куда прёшь? Не видишь? Такой комнаты вообще нет.')

def lobbylist(request):
    return render(request, 'lobbypage/lobbylist.html', {'request': request})