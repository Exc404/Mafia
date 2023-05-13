from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.template.loader import render_to_string


def index(request):
<<<<<<< HEAD
    return render(request, 'mainpage/index.html', {'request': request})
=======
    return render(request, 'mainpage/mainpage.html')
>>>>>>> JinjaMainPage


def pageNotFound(request, exception):
    return HttpResponseNotFound(render_to_string('mainpage/pageNotFound.html'))
