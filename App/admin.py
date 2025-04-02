from django.contrib import admin

# Register your models here.

from .models import User, Group, Machinery, MachineryFault

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Machinery)
admin.site.register(MachineryFault)
