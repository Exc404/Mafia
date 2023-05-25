from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from user_profile.models import Profile
from .forms import RegistrForm
from django.contrib.auth.forms import PasswordChangeForm
from .token import account_activation_token


# регистрация без подтверждения почты
# def regist(request):
#     # Массив для передачи данных шаблонны
#     data = {}
#     # Проверка что есть запрос POST
#     if request.method == 'POST':
#         # Создаём форму
#         form = RegistrForm(request.POST)
#         # Валидация данных из формы
#         if form.is_valid():
#             # Сохраняем пользователя
#             form.save()
#             # Передача формы к рендару
#             data['form'] = form
#             # Передача надписи, если прошло всё успешно
#             data['res'] = "Всё прошло успешно"
#             # Рендаринг страницы
#             return redirect('/')
#         else:
#             data['form'] = form
#             data['res'] = "Форма заполнена неверно"
#             return render(request, 'registration/registr.html', data)
#     else:  # Иначе
#         # Создаём форму
#         form = RegistrForm()
#         # Передаём форму для рендеринга
#         data['form'] = form
#         # Рендаринг страницы
#         return render(request, 'registration/registr.html', data)


def regist(request):
    # Массив для передачи данных шаблонны
    data = {}
    # Проверка что есть запрос POST
    if request.method == 'POST':
        # Создаём форму
        form = RegistrForm(request.POST)
        # Валидация данных из формы
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Подтвердите свой электронный адрес'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, "<MafiaOnlineByG4m3dev@yandex.ru>", to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            data['form'] = form
            data['res'] = "Форма заполнена неверно"
            return render(request, 'registration/registr.html', data)
    else:  # Иначе
        # Создаём форму
        form = RegistrForm()
        # Передаём форму для рендеринга
        data['form'] = form
        # Рендаринг страницы
        return render(request, 'registration/registr.html', data)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user_profile = Profile()
        user_profile.nickname = user.username
        user_profile.related_user = user
        user.save()
        user_profile.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
