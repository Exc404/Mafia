from django.urls import path, include

from .views import *

urlpatterns = [
    path('create/', lobby, name="lobby"),
    path('Room_<str:room_name>/', TheLobby, name='TheLobby'),
]