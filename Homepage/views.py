from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Context


# Create your views here.

def Homepage_view(request):
    context = {}

    return render(request, "../templates/StaticPages/Homepage.html", context)

