import math
from operator import truediv

from django.urls import resolve
from rest_framework import serializers
from App.models import *
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse


#RESTFUL API provide performance for Machinery
# Uptime downtime

#Get object
#API Logic
#Response in json
#JsonResponse

def PerformanceChart(request):
    Machinery_id = Machinery.objects.all().values("id")
    print(Machinery_id)
    response = [
        {
            "id" : Machinery_id,
        }
    ]
    return JsonResponse(response[0], safe=True)

"""
    POST list of machines sorted by ID 
    AUTOFIELD - DEFAULT SORT
"""
def FaultyCheck(x):
    if x == "FAULT":
        return True
    else:
        return False

def FaultyMachines(request):
    Faulty_Machinery = Machinery.objects.all().filter(FaultyCheck, Machinery.status)
    ids = Faulty_Machinery.values_list('id', flat=True)

    #Link with MachineryFault - find Open Fault ticket machines
    Machinery_Fault = MachineryFault.objects.filter(id__in=ids)
    Machinery_Fault.objects.sortby(resolved == False)

    # Time created_at_ and compare to timezone.now() -
    now = timezone.now()

    downtime_collection = [] 
    for machinery in Machinery_Fault:
         downtime_collection.append(machinery.downtime)

    response = [
        {
            "id" : Machinery_Fault.id,
            "downtime" : downtime_collection,
        }
    ]
    return JsonResponse(response[0], safe=False)

def Downtime(now,created_at, FaultObj):
    downtime = (now - created_at).total_seconds()
    
