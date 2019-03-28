from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from deq.models import Checklist, Facility, Letters
from datetime import datetime

@login_required(login_url='/deq/login/')
@ensure_csrf_cookie
def checklist(request):
    context_dict = {}
    context_dict['isAdmin'] = request.user.is_superuser
    context_dict['checklists'] = Checklist.objects.all()
    return render(request, 'check-list.html', context_dict)

@login_required(login_url='/deq/login/')
@ensure_csrf_cookie
def createEditChecklist(request):
    context_dict = {}
    context_dict['isAdmin'] = request.user.is_superuser
    if request.method == "POST":
        checklist = None
        if 'id' in request.POST and not request.POST['id'] == '':
            # Find and edit checklist
            checklist = Checklist.objects.get(pk=int(request.POST['id']))
        else:
            # Create new checklist 
            checklist = Checklist()
        checklist.checklist_name = request.POST['name']
        checklist.facility = Facility.objects.get(pk=int(request.POST['facility']))
        checklist.date_modified = datetime.now()
        checklist.released_to_environment = 'released' in request.POST
        checklist.residue = 'residue' in request.POST
        checklist.burned = 'burned' in request.POST
        checklist.records_of_volume = 'volume' in request.POST
        checklist.disposal = 'disposal' in request.POST
        checklist.recyclable_materials = 'recycled_m' in request.POST
        checklist.recycled_on_site = 'recycled_s' in request.POST

        # Dont set latest inspection because the checklist needs to be
        # created then the inspection date can be set
        checklist.save()
        # Create letters here and ser checklist foreign key to created checklist up above
        # Content on letter should be a string with details of these questions

        '''
        CHECKLIST QUESTIONS + DB model field
        -------------------------------------------------------------------------------------
        Are the HSM being released into the environment? (released_to_environment)

        Are any residuals generated from the recycling process? (residue)

        Does the generator maintain records on the volume of recyclable materials generated per
        month and the volume recycled per month? (records_of_volume)

        Are these materials burned for energy recovery or used to produce a fuel? (burned)

        Are these materials used in a manner constituting disposal or, once reclaimed, used in a
        manner constituting disposal? (disposal)

        Are these materials recyclable materials from which precious metals are reclaimed or spent
        lead-acid batteries being reclaimed? (recyclable_materials)

        Are the hazardous secondary materials being recycled on-site? (recycled_on_site) 
        '''
        letter = Letters()
        letter.checklist = Checklist.objects.get(pk=int(request.POST['checklist']))
        letter.subject_name = "Inspection Results for " + checklist.checklist_name()
        letter.date_modified = checklist.date_modified()

        content = ("Are the HSM being released into the environment? "+ str(checklist.release_to_enviornment) + "\n"

        "Are any residuals generated from the recycling process? "+ str(checklist.residue) +" \n "

        "Does the generator maintain records on the volume of recyclable materials generated per " 
       " month and the volume recycled per month? "+str(checklist.records_of_volume) +" \n "

        "Are these materials burned for energy recovery or used to produce a fuel? "+str(checklist.burned)+" \n"

        "Are these materials used in a manner constituting disposal or, once reclaimed, used in a"
        "manner constituting disposal? "+str(checklist.disposal)+"\n"

        "Are these materials recyclable materials from which precious metals are reclaimed or spent"
        "lead-acid batteries being reclaimed? "+str(checklist.recyclable_materials)+" \n"

        "Are the hazardous secondary materials being recycled on-site? "+str(checklist.recycled_on_site)+" \n")
        letter.content = content
        letter.save()

    elif request.method == "GET":
        print("Here")
        if "id" in request.GET:
            checklist = Checklist.objects.get(pk=int(request.GET['id']))
            if "delete" in request.GET:
                checklist.delete()
                return redirect('/deq/checklist/')
            context_dict['id'] = request.GET['id']

            context_dict['name'] = checklist.checklist_name
            context_dict['selected_facility'] = checklist.facility.pk
            context_dict['released'] =checklist.released_to_environment

            context_dict['residue'] = checklist.residue
            context_dict['burned'] = checklist.burned
            context_dict['volume'] = checklist.records_of_volume
            context_dict['disposal'] =checklist.disposal
            context_dict['recycled_m']=checklist.recyclable_materials
            context_dict['recycled_s']=checklist.recycled_on_site

        context_dict['facilities'] = Facility.objects.all()

        return render(request, 'createEditChecklist.html', context_dict)
    return redirect('/deq/checklist/')
