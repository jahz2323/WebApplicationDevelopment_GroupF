from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader, Context
from App.models import *
from .models import UserProfile, Machinery, MachineryFault, MachineryWarning, Collection
from .APIs import PerformanceChart, Add_Machinery, delete_Machinery, update_Machinery
from .forms import CustomUserForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import Group, User

# Static Pages
def App(request):
    return render(request, "../templates/StaticPages/Homepage.html")

def About(request):
    return render(request, "../templates/StaticPages/About.html")

def Services(request):
    return render(request, "../templates/StaticPages/Services.html")

def Contact(request):
    return render(request, "../templates/StaticPages/Contact.html")

def ProductCatalogue(request):
    return render(request, "../templates/StaticPages/ProductCatalogue.html")

# Login & Logout
def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return render(request, "../templates/DynamicPages/Login.html", {'success_message': 'Login successful', 'user': user.username})
        else:
            return render(request, "../templates/DynamicPages/Login.html", {'error_message': 'Invalid username or password'})
    return render(request, "../templates/DynamicPages/Login.html")

def Logout(request):
    logout(request)
    return render(request, "../templates/StaticPages/Homepage.html", {'success_message': 'Logout successful'})

# Dashboard logic
def Dashboard(request):
    user = request.user
    is_manager = user.groups.filter(name="Managers").exists()
    is_technician = user.groups.filter(name="Technicians").exists()
    is_repair = user.groups.filter(name="Repair").exists()
    importance_levels = Machinery.objects.values_list('importance', flat=True).distinct().order_by('importance')

    context = {
        "user": user,
        "is_manager": is_manager,
        "technicians": User.objects.filter(groups__name="Technicians"),
        "repairs": User.objects.filter(groups__name="Repair"),
        "importance": importance_levels,
        "machinery": Machinery.objects.all(),
        "machinery_faults": MachineryFault.objects.all(),
        "machinery_warnings": MachineryWarning.objects.all(),
        "collections": Collection.objects.all(),
    }

    return render(request, "../templates/DynamicPages/Dashboard.html", context)

# ✅ User registration page (GET view)
def user_registration(request):
    roles = ["Manager", "Technician", "Repair", "View-only"]
    form = CustomUserForm()
    return render(request, "userreg.html", {'form': form, 'roles': roles})

# ✅ Handles form POST submission
def register_user(request):
    roles = ["Manager", "Technician", "Repair", "View-only"]
    if request.method == 'POST':
        print("🔄 POST request received")
        form = CustomUserForm(request.POST)
        if form.is_valid():
            print("✅ Form is valid")
            user = form.save()
            role = form.cleaned_data.get('role')
            UserProfile.objects.create(user=user, role=role)
            print(f"👤 User created: {user.username}, Role: {role}")
            return redirect('registration_success')
        else:
            print("❌ Form is invalid")
            print(form.errors)
            return render(request, "userreg.html", {'form': form, 'roles': roles})
    else:
        print("🟢 GET request to /submit-registration/")
        form = CustomUserForm()
        return render(request, "userreg.html", {'form': form, 'roles': roles})

# ✅ Registration success message
def registration_success(request):
    return HttpResponse("<h2>✅ Registration Successful!</h2><a href='/App/register/'>Back to form</a>")

# ✅ Machinery list view
def MachineryList(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "GET":
            Collection_id = request.GET.get("collection_id")
            if Collection_id:
                collection = Collection.objects.get(id=Collection_id)
                machinery_list = Machinery.objects.filter(collections=collection)
            else:
                machinery_list = Machinery.objects.all()
            context = {
                'machinery_list': machinery_list,
                'user': user,
                'collections': Collection.objects.all(),
            }
            return render(request, "../templates/DynamicPages/MachineryList.html", context)
    return render(request, "../templates/DynamicPages/Login.html", {
        'error_message': 'You must be logged in to view this page'
    })
