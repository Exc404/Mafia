from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .models import Profile
from .forms import EditProfileForm


# Create your views here.


def profile(request):
    if request.user.is_authenticated:
        #return HttpResponse('Профиль!')

        return render(request, 'profile/profile.html', {'request': request})
    else:
        return HttpResponse('ЭЭЭЭЭ, залогинся!')


# def edit_profile(request):
#     if request.user.is_authenticated:
#
#         data = {'error': "Ошибка редактирования профиля! Проверьте правильность заполнения полей формы!"}
#         if request.method == 'GET':
#
#             render(request, 'html успешного редактирования')
#
#         form = EditProfileForm()
#         form.nickname = request.user.profile.nickname
#         form.profile_img = request.user.profile.profile_img
#
#         if request.method == 'POST':
#             var = form
#             form = EditProfileForm(request.POST, request.FILES)
#             if not form.is_valid():
#                 data['form'] = var
#                 return render(request, 'html профиля', data)
#
#         data['form'] = form
#         form_obj = form.instance
#         data['form'] = form
#         data['form_obj'] = form_obj
#         form.save(commit=False)
#         return render(request, 'html профиля', data)
#
#     else:
#         return render_to_string('<h1>ЭЭЭЭЭ, залогинся!</h1>')


def edit_profile(request):
    if request.user.is_authenticated:
        data = {}
        get_profile = Profile.objects.get(related_user=request.user)

        if request.method == 'POST':
            form = EditProfileForm(request.POST, request.FILES, instance=get_profile)
            if form.is_valid():
                form.save()
                return HttpResponse('Нормально отредачил')

        form = EditProfileForm()
        data['form'] = form
        data['form_obj'] = get_profile
        return render(request, 'edit_profile.html', data)

    else:
        return HttpResponse('ЭЭЭЭЭ, залогинся!')

