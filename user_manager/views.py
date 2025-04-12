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


# View to handle editing a user
@login_required
def edit_user(request, user_id):
    # Fetch the user object from the database
    user = get_object_or_404(User, id=user_id)
    
    # Pre-fill the form with the current user's data
    if request.method == "POST":
        form = UserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Redirect after saving the user
    else:
        form = UserCreationForm(instance=user)

    return render(request, 'user_manager/edit_user.html', {'form': form, 'user': user})


# Already implemented in the registration section
# Function to add user
# @login_required
# def add_user(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # Redirect to user list after successful registration
#             return redirect('user_list')
#     else:
#         form = UserCreationForm()

#     return render(request, 'user_manager/add_user.html', {'form': form})





# Temporary functions



# View to handle deleting a user
@login_required
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')  # Redirect to the user list page after deletion
    return render(request, 'user_manager/confirm_delete.html', {'user': user})