from django.urls import path, include

from .views import *

urlpatterns = [
    path('', profile, name="profile"),
    path('edit/', edit_profile, name="edit_profile")
]