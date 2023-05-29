from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from user_profile.models import Profile
from .forms import RegistrForm
from django.contrib.auth.forms import PasswordChangeForm
from .token import account_activation_token
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
import random

nicknames_patterns = ['Мафиози', 'Аль Капоне', 'Гангстер', 'Дуче Дон', 'Вито Скалетта', 'Дон Корлеоне', 'Джо Барбаро',
                      'Злодей британец', 'Буч', 'Винсент Вега', 'Джек Даймонд', 'Фрэнк Синтара', 'Счастливчик Лучано',
                      'Коп', 'Шериф', 'Саша Белый', 'Кабан', 'Брат', 'Томас Шелби', 'Клайд', 'Пират', 'Бандит', 'Вор',
                      'Злодей', 'Робин Гуд', 'Плут', 'Авантюрист', 'Кидала', 'Аферист', 'Прохвост', 'Ловкач', 'Япончик',
                      'Япошка', 'Шельмец', 'Остап Бендер', 'Махинатор', 'Пабло Эскобар', 'Фрэнк Костелло', 'Джон Готти',
                      'Микки Коэн', 'Генри Хилл', 'Джеймс Балджер', 'Дмитрий Давыдов', 'Крыса', 'Лео Галанте']




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
        user_profile.nickname = random.choice(nicknames_patterns)
        user_profile.related_user = user
        user.save()
        user_profile.save()

        login(request, user)

        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def password_reset(request):
    data = {"form": PasswordResetForm()}
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except Exception:
                user = False
            if user:
                subject = 'Запрошен сброс пароля'
                current_site = get_current_site(request)
                email_template_name = "acc_password_reset.html"
                cont = {
                    'email': user.email,
                    'domain': current_site.domain,
                    'site_name': 'Mafia Online',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'htpp',
                }
                msg_html = render_to_string(email_template_name, cont)
                try:
                    send_mail(subject, 'ссылка', 'admin@django-protect-site', [user.email], fail_silently=True,
                              html_message=msg_html)
                except BadHeaderError:
                    return HttpResponse('Ошибка отправки ссылки для активации! Обратитесь по почте MafiaOnlineByG4m3dev@yandex.ru для ручной активации аккаунта!')
                return redirect("password_reset_success")

    return render(request, 'registration/password_reset.html', data)
