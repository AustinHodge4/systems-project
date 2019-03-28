# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from deq.models import Letters

@login_required(login_url="/deq/login/")
@ensure_csrf_cookie
def letter(request):
    context_dict = {}
    context_dict['isAdmin'] = request.user.is_superuser
    context_dict['user'] = request.user
    context_dict['letters'] = Letters.objects.all()
    return render(request, 'letters.html', context_dict)

@login_required(login_url='/deq/login/')
@ensure_csrf_cookie
def viewEditLetter(request):
        context_dict = {}
        context_dict['isAdmin'] = request.user.is_superuser
        context_dict['user'] = request.user
        if "id" in request.GET:
                letter = Letters.objects.get(pk=int(request.GET['id']))
                if "delete" in request.GET:
                        letter.delete()
                        return redirect('/deq/letters/')
                context_dict['id'] = request.GET['id']
                context_dict['name'] = letter.letter_subject
                context_dict['date_modified'] = letter.date_modified
                context_dict['content'] = letter.content
        return render(request, 'viewEditLetter.html', context_dict)