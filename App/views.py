from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Context
from App.models import *
from .APIs import PerformanceChart,Add_Machinery,delete_Machinery,update_Machinery
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import Group


# Create your views here.

def App(request):
    context = {}

    return render(request, "../templates/StaticPages/Homepage.html", context)


def About(request):
    context = {}

    return render(request, "../templates/StaticPages/About.html", context)


# Authors  Jahziel
"""
For all users, display navigation (left-menu) which provides links to different pages, 
On mouse enter page.X < 170 display the left-menu where the user can navigate to the different pages 

Visualisation : Chartjs 
Idea: Display the downtime for FAULT machinery 
The downtime is calculated by subtracting the current time from the created_at time of the machinery
This is the data loaded into dataset attrib 
The chart used is a barchart with x being the name of the machinery and y being the downtime in days 
DYNAMIC VIEWs
Manager view: 
Add machinery, Delete machinery 
Assign Technician to machinery and Repair 

Export file, txt for groups of machinery or for individual 
"""

# Authors Jahziel Belmonte
def Dashboard(request):
    print("all groups that are present in the system", request.user.groups.all())
    print("user is authenticated", request.user.is_authenticated)
    # Get current user group

    user = request.user
    print("user group:", user.groups.get())
    print("all groups the user is in:", user.groups.all())
    is_manager = user.groups.filter(name="Managers").exists()
    is_technician = user.groups.filter(name="Technicians").exists()
    is_repair = user.groups.filter(name="Repair").exists()
    importance_levels = Machinery.objects.values_list('importance', flat=True).distinct().order_by('importance')

    print("is_manager:", is_manager)
    print("is_technician:", is_technician)
    print("is_repair:", is_repair)

    if is_manager:
        print("User is a manager:", user.username)
        # Add logic for manager dashboard
        # give context for labels - dynamically updated importance, technicians, repairs, and collections
        context = {
            "user": user,
            "is_manager": is_manager, # True if user is manager
            "technicians": User.objects.filter(groups__name="Technicians"),
            "repairs": User.objects.filter(groups__name="Repair"),
            "importance" : importance_levels,
            "machinery": Machinery.objects.all(),
            "machinery_faults": MachineryFault.objects.all(),
            "machinery_warnings": MachineryWarning.objects.all(),
            "collections": Collection.objects.all(),
        }
        return render(request, "../templates/DynamicPages/Dashboard.html", context)

    elif is_technician:
        print("User is a technician:", user.username)
        # Add logic for technician dashboard
        context = {}
        return render(request, "../templates/DynamicPages/Dashboard.html", context)
    elif is_repair:
        print("User is a repair:", user.username)
        # Add logic for repair dashboard
    else:
        # User is employee
        print("User has no group assigned")

    context = {}

    return render(request, "../templates/DynamicPages/Dashboard.html", context)


# Authors  Jahziel
def Login(request):
    print("Login view accessed")
    if request.method == "POST":
        print("Received POST data:", request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("User authenticated successfully:", user)
            return render(request, "../templates/DynamicPages/Login.html", {
                'success_message': 'Login successful',
                'user': user.username,
            })
        else:
            print("Authentication failed")
            return render(request, "../templates/DynamicPages/Login.html", {
                'error_message': 'Invalid username or password'
            })
    # If the request method is GET, render the login page

    context = {

    }
    return render(request, "../templates/DynamicPages/Login.html", context)


# Authors  Jahziel
def Logout(request):
    logout(request)
    return render(request, "../templates/StaticPages/Homepage.html", {
        'success_message': 'Logout successful',
    })


def Services(request):
    context = {}

    return render(request, "../templates/StaticPages/Services.html", context)


def ProductCatalogue(request):
    context = {}
    return render(request, "../templates/StaticPages/ProductCatalogue.html", context)


def Contact(request):
    context = {}
    return render(request, "../templates/StaticPages/Contact.html", context)

# def FaultCase(request):
#     if request.method == "POST":
#     context = {}
#     machinery = Machinery.objects.get(id=machinery_id)
#     if user_technician:
#       function: Able to create new fault case

#     faults = MachineryFault.objects.filter(machinery=machinery)
#     context['machinery'] = machinery
#     context['faults'] = faults
#     return render(request, "../templates/DynamicPages/FaultCase.html", context)