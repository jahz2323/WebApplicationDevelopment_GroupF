# user_manager/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from App.models import Machinery
from .forms import UserForm

User = get_user_model()

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'user_manager/list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('profile')
        
        # Filters
        if self.request.GET.get('role'):
            queryset = queryset.filter(profile__role=self.request.GET['role'])
        if self.request.GET.get('search'):
            queryset = queryset.filter(
                Q(username__icontains=self.request.GET['search']) |
                Q(email__icontains=self.request.GET['search'])
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machinery'] = Machinery.objects.all()
        return context

class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'user_manager/form.html'
    success_url = reverse_lazy('user_manager:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Handle profile and assignments
        self.object.profile.role = self.request.POST.get('role')
        self.object.profile.save()
        self.object.assigned_machinery_tech.set(form.cleaned_data['tech_machines'])
        self.object.assigned_machinery_repair.set(form.cleaned_data['repair_machines'])
        messages.success(self.request, "User created successfully!")
        return response

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user_manager/form.html'
    success_url = reverse_lazy('user_manager:list')

    def get_initial(self):
        initial = super().get_initial()
        initial['role'] = self.object.profile.role
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        # Handle profile and assignments
        self.object.profile.role = self.request.POST.get('role')
        self.object.profile.save()
        self.object.assigned_machinery_tech.set(form.cleaned_data['tech_machines'])
        self.object.assigned_machinery_repair.set(form.cleaned_data['repair_machines'])
        messages.success(self.request, "User updated successfully!")
        return response

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('user_manager:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "User deleted successfully!")
        return super().delete(request, *args, **kwargs)