from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_list, name="user_list"),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
]
