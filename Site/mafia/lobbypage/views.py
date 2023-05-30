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
                NewRoom.profile_set.add(request.user.profile, bulk=False)
                NewRoom.save()
                return redirect(TheLobby, NewRoom.roomname+"_"+NewRoom.roomID)
        data = {}

        form = CreateTheRoom()


        data['form'] = form
        return render(request, 'lobbypage/lobbyindex.html', data)

    else:
        return HttpResponse('ЭЭЭЭЭ, залогинся!')


def lobbylist(request):
    return render(request, 'lobbypage/lobbylist.html', {'request': request})



def TheLobby(request, room_name):
    username = request.user.profile.nickname
    print(request.user.profile.nickname)
    text = "Rewrwwrw"
    return render(request, 'lobbypage/lobbypage.html',
                  {'request': request,
                   'room_name_json': mark_safe(json.dumps(room_name)),
                   'user_nickname_json': mark_safe(json.dumps(username))
                   })
