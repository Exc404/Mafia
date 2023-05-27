from django.shortcuts import render
import json
from user_profile.models import Profile
# Create your views here.

Names = [0,0]
def lobby(request):
    Names[1] = Profile.objects.get(related_user=request.user)
    return render(request, 'lobbypage/lobbyindex.html', {})

def TheLobby(request, room_name):
    Names[0] = room_name
    return render(request, 'lobbypage/lobbypage.html',
                  {'request': request,
                   'room_name_json': json.dumps(room_name)
                   })

def GetNames():
    global Names
    tempNames = Names
    return tempNames