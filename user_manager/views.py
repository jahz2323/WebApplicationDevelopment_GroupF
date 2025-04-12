from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from App.models import UserProfile
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


# Function to render users list for user management page
@login_required
def user_list(request):
    # get all users objects
    users = User.objects.all()
    user_data = []

    # loop through each user for details
    for user in users:
        try:
            role = user.groups.first()
        except UserProfile.DoesNotExist:
            role = "N/A"
        tech_machines = user.assigned_machinery_tech.all()
        repair_machines = user.assigned_machinery_repair.all()
        
        user_data.append({
            "user": user,
            "role": role,
            "machines": list(tech_machines) + list(repair_machines)
        })
    return render(request, "user_manager/user_list.html", {"user_data": user_data})


# View to handle deleting a user
@login_required
def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User, pk=user_id)

    # Prevent users from deleting themselves
    if user_to_delete == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('user_list')

    user_to_delete.delete()
    messages.success(request, f"User '{user_to_delete.username}' has been deleted.")
    return redirect('user_list')