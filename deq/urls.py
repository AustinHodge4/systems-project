from django.urls import path
from django.shortcuts import redirect
from deq.views.homeView import home
from deq.views.loginView import loginuser, logoutuser
from deq.views.letterView import letterList

from deq.views.facilityView import facilityList, createEditFacility
from deq.views.checklistview import checklist, createEditChecklist
urlpatterns = [
    path('', lambda request: redirect('login/', permanent=False)),
    path('home/', home, name='home'),
    path('login/', loginuser),
    path('logout/',logoutuser),
    path('letters/', letterList),
    path('facilityList/', facilityList),
    path('createEditFacility/', createEditFacility),
    path('checklist/', checklist),
    path('createEditChecklist/', createEditChecklist),
]
