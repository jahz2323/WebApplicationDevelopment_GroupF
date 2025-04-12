from django.urls import path
from .views import UserListView, UserCreateView, UserUpdateView, UserDeleteView

app_name = 'user_manager'

urlpatterns = [
    path('', UserListView.as_view(), name='list'),
    path('create/', UserCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', UserUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete'),
]