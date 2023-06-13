from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.template.loader import render_to_string
from user_profile.models import Notice

def index(request):
    data = {}
    if request.user.is_authenticated:
        data['NoticesCount'] = Notice.objects.filter(addressee=request.user.profile).count()
    data['request'] = request
    return render(request, 'mainpage/mainpage.html', data)

def faqpage(request):
    return render(request, 'mainpage/faqpage.html', {'request':request})


def pageNotFound(request, exception):
    return HttpResponseNotFound(render_to_string('mainpage/pageNotFound.html'))
