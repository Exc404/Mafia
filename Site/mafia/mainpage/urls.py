from django.urls import path, include

from .views import *

urlpatterns = [
    path('', index, name="mainpage"),
    path('profile/', include('user_profile.urls'))
]
