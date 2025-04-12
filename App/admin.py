from django.contrib import admin

# Register your models here.

from .models import Collection, Machinery, MachineryWarning, MachineryFault, FaultImage, FaultComment

# imports for user registration page
from django.contrib import admin
from .models import UserProfile

# to see the registered user in the django admin panel
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

admin.site.register(Collection)
admin.site.register(Machinery)
admin.site.register(MachineryWarning)
admin.site.register(MachineryFault)
admin.site.register(FaultImage)
admin.site.register(FaultComment)
