from django.urls import path, include

from .views import *

urlpatterns = [
    path('', index, name="mainpage"),
    path('faqpage/', faqpage, name="faqpage"),
    path('get_notices_count_view/', get_notices_count_view),
    path('faqpage/get_notices_count_view/', get_notices_count_view),
]
