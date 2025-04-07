from django.urls import path
from . import views

urlpatterns = [
    path("", views.App, name="App"),
    path("Dashboard/", views.Dashboard, name="Dashboard"),
    path("About/", views.About, name="About"),
    path("Services/", views.Services, name="Services"),
    path("Dashboard/PerformanceChart/", views.PerformanceChart, name="PerformanceChart"),
]
