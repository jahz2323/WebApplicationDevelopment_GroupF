from django.urls import path
from . import views

urlpatterns = [
    # Static pages
    path("", views.App, name="App"),
    path("Dashboard/", views.Dashboard, name="Dashboard"),
    path("About/", views.About, name="About"),
    path("Services/", views.Services, name="Services"),
    path("Contact/", views.Contact, name="Contact"),
    path("ProductCatalogue", views.ProductCatalogue, name="ProductCatalogue"),
    path("Login/", views.Login, name="Login"),
    path("Logout/", views.Logout, name="Logout"),
    path("Dashboard/PerformanceChart/", views.PerformanceChart, name="PerformanceChart"),
    path("Dashboard/Add_Machinery/", views.Add_Machinery, name="Add_Machinery"),
    path("Dashboard/delete_Machinery/", views.delete_Machinery, name="delete_Machinery"),
    path("Dashboard/update_Machinery/", views.update_Machinery, name="update_Machinery"),
    path("MachineryList/", views.MachineryList, name="MachineryList"),
    # User registration
    path("register/", views.user_registration, name="user_registration"),
    path("submit-registration/", views.register_user, name="register_user"),
    path("register/success/", views.registration_success, name="registration_success"),
    path("FaultCaseDetails <int:machinery_id>/", views.FaultCaseDetails, name="FaultCaseDetails"),
]
