from django.shortcuts import render

# Create your views here.

def lobbylist(request):
    return render(request, 'lobbylistpage/lobbylistpage.html', {'request': request})