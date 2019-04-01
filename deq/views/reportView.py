# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from deq.models import Reports
from django.utils import timezone
from django.contrib.auth.models import User


@login_required(login_url="/deq/login/")
@ensure_csrf_cookie
def reportList(request):
    context_dict = {}
    context_dict['isAdmin'] = request.user.is_superuser
    context_dict['user'] = request.user
    context_dict['reports'] = Reports.objects.all()
    return render(request, 'reports.html', context_dict)

@login_required(login_url='/deq/login/')
@ensure_csrf_cookie
def createEditReport(request):
    context_dict = {}
    context_dict['isAdmin'] = request.user.is_superuser
    context_dict['user'] = request.user
    if request.method == "POST":
        report = None
        if 'id' in request.POST and not request.POST['id'] == '':
            report = Reports.objects.get(pk=int(request.POST['id']))
        else:
            report = Reports()

        report.report_name = request.POST['name']
        report.content = request.POST['content']
        report.employee = User.objects.get(pk=int(request.POST['employee']))
        report.date_modified = timezone.now()

        report.save()
    elif request.method == 'GET':
        if "id" in request.GET:
            report = Reports.objects.get(pk=int(request.GET['id']))
            if "delete" in request.GET:
                report.delete()
                return redirect('/deq/reports/')
            if 'view' in request.GET:
                context_dict['view'] = True

            context_dict['id'] = request.GET['id']
            context_dict['name'] = report.report_name
            context_dict['content'] = report.content
            context_dict['selected_employee'] = report.employee.pk
            context_dict['date_modified'] = report.date_modified

        context_dict['employees'] = User.objects.filter(is_superuser=False)

    return render(request, 'createEditReport.html', context_dict)