from django.urls import path

from .views import *

urlpatterns = [
    path('registration/', regist, name = "regist")
]