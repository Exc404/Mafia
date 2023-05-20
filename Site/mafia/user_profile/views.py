from django.shortcuts import render
from django.template.loader import render_to_string

from .forms import ImageForm, NicknameForm


# Create your views here.


def profile(request):
    data = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            form_img = ImageForm(request.POST)
            form_nick = NicknameForm(request.POST)
            # Валидация данных из формы
            if form_img.is_valid():
                request.user.profile.profile_img = form_img.profileImg
                request.user.profile.save()
            else:
                if form_nick.is_valid():
                    request.user.profile.form_nick = form_nick.nickname
                    request.user.profile.save()

        return render(request, 'profile/profile.html', {'request': request})
    else:
        return render_to_string('ЭЭЭЭЭ, залогинся!')
