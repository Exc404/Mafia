from django.urls import path, include

from .views import *

urlpatterns = [
    path('', profile, name="profile"),
    path('settings/', settings_profile, name="settings_profile"),
    path('edit/', edit_profile, name="edit_profile"),
    path('friends-search/', friends_search, name="friends_search"),
    path('friends/', friends_list, name="friends"),
    path('notice/', notice, name="notice"),
    path('notice/delete_record/<int:record_id>/', delete_notice, name='delete_record'),
    path('notice/add_record/<int:record_id>/', add_notice, name='add_record'),
    path('<slug>/', show_profile, name="show_profile"),
    path('<slug>/add_friendship_record/', add_friendship_notice, name="add_friendship_record"),
    path('<slug>/delete_friendship_record/', delete_friendship_notice, name="delete_friendship_record"),
]
