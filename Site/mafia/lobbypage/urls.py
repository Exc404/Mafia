from django.urls import path, include

from .views import *

urlpatterns = [
    path('create/', lobby, name="lobby"),
    path('<str:room_name>/', TheLobby, name='TheLobby'),
    path('enter/', lobbylist, name="lobbylist")
]