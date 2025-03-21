from django.urls import path
from . import views

urlpatterns = [
    path("", views.Homepage_view, name="Homepage_view"),
]