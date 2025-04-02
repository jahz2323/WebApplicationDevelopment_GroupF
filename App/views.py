from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Context


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

def Services(request):
    context = {}

    return render(request, "../templates/StaticPages/Services.html", context)