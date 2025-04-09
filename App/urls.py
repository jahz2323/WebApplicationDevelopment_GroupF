from django.urls import path
from . import views

urlpatterns = [
    path("", views.App, name="App"),
    path("Dashboard/", views.Dashboard, name="Dashboard"),
    path("About/", views.About, name="About"),
    path("Services/", views.Services, name="Services"),
    path("Contact/", views.Contact, name="Contact"),
    path("ProductCatalogue", views.ProductCatalogue, name="ProductCatalogue"),
    path("Dashboard/PerformanceChart/", views.PerformanceChart, name="PerformanceChart"),
]
