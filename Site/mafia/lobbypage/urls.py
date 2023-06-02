from django.urls import path, include

from .views import *

urlpatterns = [
    path('create/', lobby, name="lobby"),
    path('enter/', lobbylist, name="lobbylist"),
    path('<str:room_name>/', TheLobby, name='TheLobby')
]