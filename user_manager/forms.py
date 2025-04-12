from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from App.models import Machinery

User = get_user_model()

class UserForm(UserCreationForm):
    tech_machines = forms.ModelMultipleChoiceField(
        queryset=Machinery.objects.all(),
        widget=forms.SelectMultiple(attrs={'size': '5'}),
        required=False
    )
    repair_machines = forms.ModelMultipleChoiceField(
        queryset=Machinery.objects.all(),
        widget=forms.SelectMultiple(attrs={'size': '5'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tech_machines'].initial = self.instance.assigned_machinery_tech.all()
            self.fields['repair_machines'].initial = self.instance.assigned_machinery_repair.all()
            self.fields['password1'].required = False
            self.fields['password2'].required = False
            self.fields['password1'].widget.attrs['placeholder'] = 'Leave blank to keep current password'
            self.fields['password2'].widget.attrs['placeholder'] = 'Leave blank to keep current password'