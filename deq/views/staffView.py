from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User

@login_required(login_url='/deq/login/')
@ensure_csrf_cookie
def staffList(request):
    context_dict = {}
    context_dict['isAdmin'] = request.user.is_superuser
    context_dict['user'] = request.user
    context_dict['staffs'] = User.objects.all()
    return render(request, 'staff.html', context_dict)

@login_required(login_url='/deq/login/')
@ensure_csrf_cookie
def createEditStaff(request):
    context_dict = {}
    context_dict['isAdmin'] = request.user.is_superuser
    context_dict['user'] = request.user
    if request.method == "POST":
        user = None
        if 'id' in request.POST and not request.POST['id'] == '':
            user = User.objects.get(pk=int(request.POST['id']))
        else:
            user = User()

        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.username = request.POST['username']
        user.set_password(request.POST['password'])
        user.email = request.POST['email']
        user.is_staff = True
        user.is_superuser = 'is_admin' in request.POST
        user.save()
        
    elif request.method == "GET":
        if "id" in request.GET:
            user = User.objects.get(pk=int(request.GET['id']))
            if "delete" in request.GET:
                user.delete()
                return redirect('/deq/staff/')

            context_dict['id'] = request.GET['id']

            context_dict['first_name'] = user.first_name
            context_dict['last_name'] = user.last_name
            context_dict['username'] = user.username
            context_dict['password'] = user.password
            context_dict['email'] =  user.email
            context_dict['is_admin'] = user.is_superuser

        return render(request, 'createEditStaff.html', context_dict)

    return redirect('/deq/staff/')