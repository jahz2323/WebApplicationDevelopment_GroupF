import math
from operator import truediv
import os # for file path writing new reports
from django.conf import settings
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
        # print(f"Name: {machinery.name}, Status: {machinery.status}, Importance: {machinery.importance}",
        #       f"Created at: {machinery.created_at}, Updated at: {machinery.updated_at}")
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


# // Author Jahziel Belmonte
def calculate_downtime(created_at, now_time):
    """
    Calculate the downtime in hours between the created_at time and now_time.
    :param created_at: datetime object representing the creation time
    :param now_time: datetime object representing the current time
    :return: downtime in hours
    """
    return math.floor((now_time - created_at).total_seconds() / 3600)  # convert to hours


def Add_Machinery(request):
    print("Add_Machinery view accessed")
    # Check if the name of object is already in the database
    if request.method == "POST":
        print("Received POST data:", request.POST)
        """
            Data from POST request
            - name
            - status
            - importance
            - assigned_technician
            - assigned_repair
            - assigned_collection
            Defined attributes , created at and updated_at will be time now 
            - created_at
            - updated_at
        """
        name = request.POST.get("machine_name")
        status = request.POST.get("status")
        importance = request.POST.get("Importance")
        description = request.POST.get("description")
        # getlist() is used to get multiple values from the form
        assigned_technician = request.POST.getlist("assigned-technicians")
        assigned_repair = request.POST.getlist("assigned-repair")
        assigned_collection = request.POST.getlist("collections")
        created_at = datetime.now()
        updated_at = datetime.now()
        # Check if the machinery already exists
        if Machinery.objects.filter(name=name).exists():
            print("Machinery already exists")
            return JsonResponse({'error': 'Machinery already exists'}, status=400)
        else:
            # Create new machinery object
            machinery = Machinery(
                name=name,
                status=status,
                description=description,
                importance=importance,
                created_at=created_at,
                updated_at=updated_at
            )

            machinery.save()
            # Assign the technician, repair, and collection
            machinery.assigned_technicians.set(
                assigned_technician)  # Needed for many to many field to update relationship
            machinery.assigned_repair.set(assigned_repair)
            machinery.collections.set(assigned_collection)

            print("Machinery added successfully")
            return JsonResponse({'success': 'Machinery added successfully'}, status=200)


def delete_Machinery(request):
    print("delete_Machinery view accessed")

    if request.method == "POST":
        # Get the machinery ID from the request get list to delete multiple objects
        machinery_id = request.POST.getlist("machinery_id")
        print("Received machinery ID:", machinery_id)
        try:
            # Get the machinery object to match the ID
            for id in machinery_id:
                # Get the machinery object
                machinery = Machinery.objects.get(id=id)
                # Delete the machinery object
                machinery.delete()
                print(f"Machinery with ID {id} deleted successfully")
            return JsonResponse({'success': 'Machinery deleted successfully'}, status=200)
        except Machinery.DoesNotExist:
            return JsonResponse({'error': 'Machinery not found'}, status=404)


def update_Machinery(request):
    print("update_Machinery view accessed")
    machinery_id = request.POST.getlist("machinery_id")
    print("Received machinery ID:", machinery_id)

    if request.method == "POST":
        # List literal for report data
        report = []
        # Get the machinery ID from the request
        now = datetime.now()
        report_text = request.POST.get("Report")
        for id in machinery_id:
            try:
                # Get the machinery object
                machinery = Machinery.objects.get(id=id)
                # Update the machinery object set updated.now attib to current time
                print("Time now:", now)
                machinery.updated_at = now
                print("Machinery updated at :", machinery.updated_at)

                report.append(f"Name: {machinery.name}, Status: {machinery.status}, Importance: {machinery.importance}, "
                              f"Created at: {machinery.created_at}, Updated at: {machinery.updated_at}"
                              f", Current time: {now}, "
                              f"Report details: {report_text}")

                # Export a new file containing the report data, save in static folder

            except Machinery.DoesNotExist:
                # If the machinery object does not exist, return an error response
                print(f"Machinery with ID {id} not found")

            #export file to static folder, store as a txt
            report_content = "\n".join(report)

            #Join to the media folder
            media_dir = os.path.join(settings.BASE_DIR, 'App', 'static', 'media')
            os.makedirs(media_dir, exist_ok=True) #check if the directory exists, if not create it
            # Create a file name and path to save the report
            file_name = f"machinery_report_{now.strftime('%Y%m%d_%H%M%S')}.txt"
            file_path = os.path.join(media_dir, file_name)

            with open(file_path, 'w') as file:
                file.write(report_content)
            print(f"Report exported to {file_path}")
            # Return the response
            return JsonResponse({'success': 'Machinery updated successfully', 'report_path': f'/static/media/{file_name}'}, status=200)

        return JsonResponse({'error': 'Machinery not found'}, status=404)
