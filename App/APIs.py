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

def get_machinery_status():
    # get all statuses of machines
    # and convert to list
    Machines = Machinery.objects.all()
    status_list = []

    for machine in Machines:
        status_list.append(machine.status, machine.name)
    return status_list


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



def calculate_downtime(created_at, now_time):
    return math.floor((now_time - created_at).total_seconds() / 3600)  # convert to hours