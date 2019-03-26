# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from deq.models import Letters

@login_required(login_url="/deq/login/")
@ensure_csrf_cookie
def letterList(request):
    context_dict = {}
    context_dict['isAdmin'] = request.user.is_superuser
    context_dict['letters'] = Letters.objects.all()
    return render(request, 'letters.html', context_dict)

@login_required(login_url='/deq/login/')
@ensure_csrf_cookie
def editDeleteLetter(request):

    return 0
