from django import forms
from django.contrib.auth.models import User, Group
from .models import UserProfile, Machinery

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    role = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)  # Select group as role
    assigned_machinery = forms.ModelMultipleChoiceField(queryset=Machinery.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)  # Select machinery for the user

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        # Save user profile and assign the user to the selected group
        role = self.cleaned_data.get('role')
        UserProfile.objects.create(user=user, role=role.name)  # Save role as group name
        user.groups.add(role)  # Add user to the selected group

        # Assign selected machinery to the user
        assigned_machinery = self.cleaned_data.get('assigned_machinery')
        user.assigned_machinery_tech.set(assigned_machinery)  # Assuming the machinery is for technicians
        user.save()

        return user
