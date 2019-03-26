from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from deq.models import Facility

@login_required(login_url='/deq/login/')
@ensure_csrf_cookie
def facilityList(request):
    context_dict = {}
    context_dict['isAdmin'] = request.user.is_superuser
    context_dict['facilities'] = Facility.objects.all()
    return render(request, 'facilityList.html', context_dict)

@login_required(login_url='/deq/login/')
@ensure_csrf_cookie
def createEditFacility(request):
    context_dict = {}
    context_dict['isAdmin'] = request.user.is_superuser
    if request.method == "POST":
        facility = None
        if 'id' in request.POST and not request.POST['id'] == '':
            facility = Facility.objects.get(pk=int(request.POST['id']))
        else:
            facility = Facility()
        facility.facility_name = request.POST['name']
        facility.street_address = request.POST['street']
        facility.county = request.POST['county']
        facility.city = request.POST['city']
        facility.zipcode = request.POST['zipcode']
        facility.district = request.POST['district']
        facility.telephone = request.POST['telephone']
        # Dont set latest inspection because the checklist needs to be
        # created then the inspection date can be set
        facility.save()
    elif request.method == "GET":
        if "id" in request.GET:
            facility = Facility.objects.get(pk=int(request.GET['id']))
            if "delete" in request.GET:
                facility.delete()
                return redirect('/deq/facilityList/')

            context_dict['id'] = request.GET['id']

            context_dict['name'] = facility.facility_name
            context_dict['street'] = facility.street_address
            context_dict['county'] = facility.county
            context_dict['city'] = facility.city
            context_dict['zipcode'] = facility.zipcode
            context_dict['district'] = facility.district
            context_dict['telephone'] = facility.telephone
        return render(request, 'createEditFacility.html', context_dict)

    return redirect('/deq/facilityList/')