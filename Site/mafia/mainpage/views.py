from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from user_profile.models import Notice
from django.views.decorators.csrf import csrf_exempt


def index(request):
    data = {}
    data['request'] = request
    return render(request, 'mainpage/mainpage.html', data)


def faqpage(request):
    return render(request, 'mainpage/faqpage.html', {'request': request})


@csrf_exempt
def get_notices_count_view(request):
    if request.user.is_authenticated and request.method == "POST":
        notice_count = Notice.objects.filter(addressee=request.user.profile).count()
        response = {"notice_count": notice_count}
        return JsonResponse(response)


def pageNotFound(request, exception):
    return HttpResponseNotFound(render_to_string('mainpage/pageNotFound.html'))
