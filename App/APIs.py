import math
from operator import truediv

from django.urls import resolve
from rest_framework import serializers
from App.models import *
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now



# RESTFUL API provide performance for Machinery
# Uptime downtime
# Get object
# API Logic
# Response in json
# JsonResponse
# // Author Jahziel Belmonte
def get_machinery_status():
    # get all statuses of machines
    # and convert to list
    Machines = Machinery.objects.all()
    status_list = []

    for machine in Machines:
        status_list.append(machine.status, machine.name)
    return status_list

# // Author Jahziel Belmonte
def PerformanceChart(request):
    # Interested in machinery with FAULT status
    Machinery_fault_objects = Machinery.objects.filter(status="FAULT")
    items = []
    for machinery in Machinery_fault_objects:
        # print name, status and importance
        print(f"Name: {machinery.name}, Status: {machinery.status}, Importance: {machinery.importance}",
              f"Created at: {machinery.created_at}, Updated at: {machinery.updated_at}")
        current_time = timezone.now()
        downtime_hours = calculate_downtime(machinery.created_at, current_time)
        """
            return items object for each machinery that has 'fault' status
            - name
            - status
            - importance
            - created_at
            - updated_at
            - current_time
            - downtime_hours // calculate_downtime 
        """
        items.append({
            "name": machinery.name,
            "status": machinery.status,
            "importance": machinery.importance,
            "created_at": machinery.created_at,
            "updated_at": machinery.updated_at,
            'current_time': current_time,
            'downtime_hours': downtime_hours
        })

    response = [
        {
            'success': True,
            'message': 'Data retrieved successfully',
            'items': items,
        }
    ]

    return JsonResponse(response[0], safe=True)


#// Author Jahziel Belmonte
def calculate_downtime(created_at, now_time):
    """
    Calculate the downtime in hours between the created_at time and now_time.
    :param created_at: datetime object representing the creation time
    :param now_time: datetime object representing the current time
    :return: downtime in hours
    """
    return math.floor((now_time - created_at).total_seconds() / 3600)  # convert to hours



def Add_Machinery(request):
    return None
