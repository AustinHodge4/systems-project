# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

@login_required(login_url='/deq/login/')
@ensure_csrf_cookie
def home(request):
    context_dict = {}
    context_dict['isAdmin'] = request.user.is_superuser
    print(context_dict)
    return render(request, 'index.html', context_dict)