from django.urls import path, include

from .views import *

urlpatterns = [
    path('settings/', settings_profile, name="settings_profile"),
    path('edit/', edit_profile, name="edit_profile"),
    path('<slug>/', show_profile, name="show_profile"),
    path('friends-search', friends_search, name="friends_search")
]