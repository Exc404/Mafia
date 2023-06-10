from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from .models import *
from .forms import EditProfileForm, FriendsSearchForm


def profile(request):
    if request.user.is_authenticated:
        return redirect(show_profile, request.user.profile.slug)
    else:
        return redirect('login')


def show_profile(request, slug):
    showed_profile = get_object_or_404(Profile, slug=slug)
    data = {'user_profile': showed_profile}

    if request.user.is_authenticated and showed_profile == request.user.profile:
        data['login'] = request.user.username
        data['edit'] = True
        return render(request, 'profile/profile.html', data)
    else:
        data['login'] = ''
        data['edit'] = False
        friendship = request.user.friend.friends.all().filter(pk=showed_profile.pk).exists()
        if friendship:
            data['friend'] = True
        else:
            if request.user.profile.notice_set.all().filter(sender=showed_profile.related_user).filter(
                    notice_type=Notice.NoticeType.FRIENDSHIP).exists():
                data['friendship_notice_get'] = True
            elif showed_profile.notice_set.all().filter(sender=request.user).filter(
                    notice_type=Notice.NoticeType.FRIENDSHIP).exists():
                data['friendship_notice_send'] = True
            else:
                data['not_friend'] = True

    return render(request, 'profile/show_profile.html', data)


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
                return redirect(get_profile)

        form = EditProfileForm(instance=get_profile)
        data['form'] = form
        data['form_obj'] = get_profile
        return render(request, 'edit_profile.html', data)

    else:
        return redirect('login')


def settings_profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile/profile_settings.html', {'request': request})
    else:
        return redirect('login')


def friends_search(request):
    data = {}
    if request.user.is_authenticated:
        data['user_profile'] = request.user.profile
        data['form'] = FriendsSearchForm(initial={'nickname': 'введите никнейм'})
        if 'nickname' in request.GET:
            data['form'] = FriendsSearchForm(request.GET)
            if data['form'].is_valid():
                search_nickname = data['form'].cleaned_data['nickname']
                search_result = Profile.objects.filter(nickname__icontains=search_nickname)
                if search_result.count() > 0:
                    data['search_result'] = search_result
                else:
                    data['search_result'] = False
                    data['message'] = 'По вашему запросу ничего не найдено'
        else:
            data['message'] = 'Здесь будут перечислены найденные профили'

        return render(request, 'profile/friends_search.html', data)
    else:
        return redirect('login')


def notice(request):
    if request.user.is_authenticated:
        data = {}
        data['notices'] = reversed(Notice.objects.filter(addressee=request.user.profile))
        return render(request, 'profile/notice.html', data)
    else:
        return redirect('login')


def friends_list(request):
    if request.user.is_authenticated:
        data = {}
        data['friends'] = Friend.objects.get(related_user=request.user).friends.all()
        return render(request, 'profile/friends_list.html', data)
    else:
        return redirect('login')


@csrf_exempt
def delete_notice(request, record_id):
    response = {'notice_id': record_id}
    get_notice = Notice.objects.get(pk=record_id)

    if get_notice.notice_type == Notice.NoticeType.FRIENDSHIP:
        response_notice = Notice()
        response_notice.notice_type = Notice.NoticeType.INFO
        response_notice.text_message = "Ваша заявка в друзья была отклонена!"
        response_notice.addressee = get_notice.sender.profile
        response_notice.sender = get_notice.addressee.related_user
        response_notice.save()

    get_notice.delete()
    response['message'] = 'Запись успешно удалена.'
    return JsonResponse(response)


@csrf_exempt
def add_notice(request, record_id):
    response = {'notice_id': record_id}
    get_notice = Notice.objects.get(pk=record_id)

    user1 = get_notice.sender
    user2 = get_notice.addressee.related_user

    user1.friend.friends.add(user2.profile)
    user2.friend.friends.add(user1.profile)

    response_notice = Notice()
    response_notice.notice_type = Notice.NoticeType.INFO
    response_notice.text_message = "принял вашу заявку в друзья!"
    response_notice.sender = user2
    response_notice.addressee = user1.profile
    response_notice.save()

    get_notice.delete()
    response['message'] = 'Запись успешно удалена.'
    return JsonResponse(response)


@csrf_exempt
def add_friendship_notice(request, slug):
    sender = request.user
    addressee = Profile.objects.get(slug=slug)

    response_notice = Notice()
    response_notice.notice_type = Notice.NoticeType.FRIENDSHIP
    response_notice.text_message = "Заявка отправлена"
    response_notice.sender = sender
    response_notice.addressee = addressee
    response_notice.save()

    response = {'message': 'Уведомление отправлено'}
    return JsonResponse(response)


@csrf_exempt
def delete_friendship_notice(request, slug):

    profile1 = request.user.profile
    profile2 = Profile.objects.get(slug=slug)

    profile1.related_user.friend.friends.remove(profile2)
    profile2.related_user.friend.friends.remove(profile1)

    response_notice = Notice()
    response_notice.notice_type = Notice.NoticeType.INFO
    response_notice.text_message = "Вас удалил из друзей!"
    response_notice.sender = profile1.related_user
    response_notice.addressee = profile2
    response_notice.save()

    response = {'message': 'Уведомление отправлено'}
    return JsonResponse(response)
