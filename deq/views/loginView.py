# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def loginuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # login user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/deq/home/')
        else:
            return redirect('/deq/')
    else:
        return render(request, 'login.html')

def logoutuser(request):
    logout(request)
    return redirect('/deq/')
