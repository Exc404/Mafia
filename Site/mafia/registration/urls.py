from django.contrib.auth.views import LoginView, \
    PasswordResetDoneView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView, LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path('registration/', regist, name='regist'),
    path('login/', LoginView.as_view(template_name = 'registration/login.html') , name = 'login'),
    path('logout/', LogoutView.as_view() , name = 'logout'),
    path('password-reset/', password_reset, name = 'password_reset'),
    path('password-reset/success/', PasswordResetDoneView.as_view(template_name = 'registration/password_reset_success.html') , name = 'password_reset_success'),
    path('reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name = 'registration/reset_confirm.html'), name = 'password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name = 'registration/reset_complete.html',) , name = 'password_reset_complete'),
    path('password-change/', PasswordChangeView.as_view(template_name = 'registration/password_change.html', success_url = 'success/') , name = 'password_change'),
    path('password-change/success/', PasswordChangeDoneView.as_view(template_name = 'registration/password_change_success.html') , name = 'password_change_success'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate')
]


