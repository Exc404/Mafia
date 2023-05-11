from django.urls import path, include

from .views import *

urlpatterns = [
    path('registration/', regist, name='regist'),
    path('', include('django.contrib.auth.urls'), name='login'),
   # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate')
]