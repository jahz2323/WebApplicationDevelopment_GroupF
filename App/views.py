from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Context
from App.models import *
from .APIs import PerformanceChart, Add_Machinery
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate, login, logout

# Create your views here.

def App(request):
    context = {}

    return render(request, "../templates/StaticPages/Homepage.html", context)

def About(request):
    context = {}

    return render(request, "../templates/StaticPages/About.html", context)

def Dashboard(request):
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