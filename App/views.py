from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader, Context
from App.models import *
from .models import UserProfile, Machinery, MachineryFault, MachineryWarning, Collection
from .APIs import PerformanceChart, Add_Machinery, delete_Machinery, update_Machinery, StatusChart
from .forms import CustomUserForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import Group, User


# Static Pages
def App(request):
    return render(request, "../templates/StaticPages/Homepage.html")


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


# Authors Jahziel Belmonte and Thomas
# Dashboard
# The dashboard is a dynamic page that displays different information based on the user's role
# Manager, Technician, Repair
# Managers can add, delete, and assign machinery to technicians, repair
# Technicians and repair can see the machinery assigned to them

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

    assigned_machinery = Machinery.objects.none()

    if is_technician:
        assigned_machinery = Machinery.objects.filter(assigned_technicians=user)
    elif is_repair:
        assigned_machinery = Machinery.objects.filter(assigned_repair=user)

    ok_count = assigned_machinery.filter(status='OK').count()
    total_count = assigned_machinery.count()

    print("is_manager:", is_manager)
    print("is_technician:", is_technician)
    print("is_repair:", is_repair)

    #Jahz
    if is_manager:
        print("User is a manager:", user.username)
        # Add logic for manager dashboard
        # give context for labels - dynamically updated importance, technicians, repairs, and collections
        context = {
            "user": user,
            "is_manager": is_manager,  # True if user is manager
            "technicians": User.objects.filter(groups__name="Technicians"),
            "repairs": User.objects.filter(groups__name="Repair"),
            "importance": importance_levels,
            "machinery": Machinery.objects.all(),
            "machinery_faults": MachineryFault.objects.all(),
            "machinery_warnings": MachineryWarning.objects.all(),
            "collections": Collection.objects.all(),
        }
        return render(request, "../templates/DynamicPages/Dashboard.html", context)

    #Thomas
    elif is_technician:
        print("User is a technician:", user.username)
        # Add logic for technician dashboard
        context = {
            'is_technician': is_technician,
            'assigned_machinery': assigned_machinery,
            "machinery": Machinery.objects.all(),
            'ok_count': ok_count,
            'total_count': total_count,
        }
        return render(request, "../templates/DynamicPages/Dashboard.html", context)
    #Thomas
    elif is_repair:
        print("User is a repair:", user.username)
        context = {
            'is_repair': is_repair,
            'assigned_machinery': assigned_machinery,
            "machinery": Machinery.objects.all(),
            'ok_count': ok_count,
            'total_count': total_count,
        }
        return render(request, "../templates/DynamicPages/Dashboard.html", context)
        # Add logic for repair dashboard
    else:
        # User is employee
        print("User has no group assigned")
    context = {}
    return render(request, "../templates/DynamicPages/Dashboard.html", context)


def Services(request):
    services_data = [
        {
            'image': 'media/ServicePage/Mchn.jpg',
            'title': 'Machine Status Monitoring',
            'description': 'Stay updated on machine health with real-time data and alerts.'
        },
        {
            'image': 'media/ServicePage/Mchn1.jpg',
            'title': 'Fault Reporting',
            'description': 'Technicians can report and log faults instantly for quicker resolution.'
        },
        {
            'image': 'media/ServicePage/Mchn2.jpg',
            'title': 'Repair Management',
            'description': 'Repair personnel can view, update, and resolve reported issues.'
        },
        {
            'image': 'media/ServicePage/Mchn3.jpg',
            'title': 'Manager Dashboard',
            'description': 'Managers can assign tasks, monitor operations, and view reports.'
        }
    ]
    return render(request, "../templates/StaticPages/Services.html", {'services': services_data})


def Contact(request):
    return render(request, "../templates/StaticPages/Contact.html")


def ProductCatalogue(request):
    return render(request, "../templates/StaticPages/ProductCatalogue.html")


# Login & Logout
# Authors Jahziel Belmonte
def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("Checking credentials for user:", username)
        user = authenticate(request, username=username, password=password)
        if user:
            print("User authenticated successfully:", username)
            login(request, user)
            return render(request, "../templates/DynamicPages/Login.html",
                          {'success_message': 'Login successful', 'user': user.username})
        else:
            print("Invalid credentials for user:", username)
            return render(request, "../templates/DynamicPages/Login.html",
                          {'error_message': 'Invalid username or password'})
    return render(request, "../templates/DynamicPages/Login.html")

# Authors Jahziel Belmonte
# Logout Function
def Logout(request):
    logout(request)
    return render(request, "../templates/StaticPages/Homepage.html", {'success_message': 'Logout successful'})


# Authors Omkar
def user_registration(request):
    form = CustomUserForm()
    roles = ["Manager", "Technician", "Repair", "View-only"]
    return render(request, '../templates/DynamicPages/userreg.html', {'form': form, 'roles': roles})


def register_user(request):
    if request.method == 'POST':
        print("🔄 POST request received")
        form = CustomUserForm(request.POST)
        if form.is_valid():
            print("✅ Form is valid")
            user = form.save()
            role = form.cleaned_data.get('role')
            print(f"👤 Created user: {user.username}, Role: {role}")
            UserProfile.objects.create(user=user, role=role)
            print("📦 UserProfile created successfully")
            return redirect('registration_success')
        else:
            print("❌ Form is invalid:")
            print(form.errors)
    else:
        print("🟢 GET request received for registration")

    form = CustomUserForm()
    roles = ["Manager", "Technician", "Repair", "View-only"]
    return render(request, '../templates/DynamicPages/userreg.html', {'form': form, 'roles': roles})


def registration_success(request):
    return HttpResponse("<h2>✅ Registration Successful!</h2><a href='/App/register/'>Go back to form</a>")


# Authors Jahziel Belmonte
def MachineryList(request):
    print("Machinery list view accessed")
    # Check if the user is authenticated
    user = request.user

    if user.is_authenticated:
        print("User is authenticated:", user.username)
        # Get selection from collection
        if request.method == "GET":
            # Collection id
            Collection_id = request.GET.get("collection_id")
            print("Requested Collection id :", Collection_id)
            # Get machinery objects from specific collection
            if Collection_id:
                # Get the collection object
                collection = Collection.objects.get(id=Collection_id)
                # Get all machinery objects in the collection
                machinery_list = Machinery.objects.filter(collections=collection)
                context = {
                    'machinery_list': machinery_list,
                    'user': user,
                    'collections': Collection.objects.all(),
                }
                return render(request, "../templates/DynamicPages/MachineryList.html", context)
            else:
                # Get all machinery objects from the database
                machinery_list = Machinery.objects.all()
                # Get all collection objects from the database
                collections = Collection.objects.all()
                context = {
                    'machinery_list': machinery_list,
                    'user': user,
                    'collections': collections,
                }
                return render(request, "../templates/DynamicPages/MachineryList.html", context)
        else:
            context = {}
            return render(request, "../templates/DynamicPages/MachineryList.html", context)
        # If the user is not authenticated, redirect to the login page
    return render(request, "../templates/DynamicPages/Login.html", {
        'error_message': 'You must be logged in to view this page'
    })


def FaultCaseDetails(request, machinery_id):
    print("Fault case details view accessed")
    # Check if the user is authenticated
    user = request.user

    if user.is_authenticated:
        print("User is authenticated:", user.username)
        # Get the machinery object from the database
        machinery = Machinery.objects.get(id=machinery_id)
        # Get all fault cases for the machinery
        fault_cases = MachineryFault.objects.filter(machinery=machinery)
        context = {
            'machinery': machinery,
            'fault_cases': fault_cases,
            'user': user,
        }
        return render(request, "../templates/DynamicPages/FaultCase.html", context)
    else:
        context = {}
        return render(request, "../templates/DynamicPages/Login.html", {
            'error_message': 'You must be logged in to view this page'
        })

# Fault page views ------------------------------------------------------------------

# View to list all fault cases related to a specific machinery
def machinery_fault_list(request, machinery_id):
    # Retrieve the machinery object or return 404 if not found
    machinery = get_object_or_404(Machinery, id=machinery_id)

    # Get all fault cases associated with this machinery
    faults = MachineryFault.objects.filter(machinery=machinery)

    # Pass the machinery and faults to the template
    context = {
        'machinery': machinery,
        'faults': faults,
    }

    # Render the machinery_fault_list template with the context
    return render(request, '../templates/DynamicPages/machinery_fault_list.html', context)


# View to show detailed information about a specific fault case
@login_required
def fault_detail(request, pk):
    fault = get_object_or_404(MachineryFault, pk=pk)

    if request.method == "POST" and request.user.has_perm("App.comment_fault"):
        text = request.POST.get("text")
        image = request.FILES.get("image")

        if text:
            FaultComment.objects.create(
                fault=fault,
                user=request.user,
                text=text
            )

        if image:
            FaultImage.objects.create(
                fault=fault,
                uploaded_by=request.user,
                image=image
            )

        if request.user.has_perm("App.resolve_fault") and 'resolve' in request.POST:
            fault.resolved = True
            fault.resolved_by = request.user
            fault.save()

        return redirect("fault_detail", pk=fault.pk)

    return render(request, "../templates/DynamicPages/fault_detail.html", {
        "fault": fault,
    })

@login_required
@permission_required("App.create_fault", raise_exception=True)
def create_fault(request, machinery_id):
    machinery = get_object_or_404(Machinery, pk=machinery_id)

    if request.method == "POST":
        title = request.POST.get("title")
        details = request.POST.get("details")
        image = request.FILES.get("image")

        if title and details:
            fault = MachineryFault.objects.create(
                title=title,
                details=details,
                created_by=request.user,
                machinery=machinery
            )

            if image:
                FaultImage.objects.create(
                    fault=fault,
                    uploaded_by=request.user,
                    image=image
                )

            return redirect("fault_detail", pk=fault.pk)

    return render(request, "../templates/DynamicPages/create_fault.html", {"machinery": machinery})