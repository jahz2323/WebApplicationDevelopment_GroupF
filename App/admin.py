from django.contrib import admin

# Register your models here.

from .models import Collection, Machinery, MachineryWarning, MachineryFault, FaultImage, FaultComment

admin.site.register(Collection)
admin.site.register(Machinery)
admin.site.register(MachineryWarning)
admin.site.register(MachineryFault)
admin.site.register(FaultImage)
admin.site.register(FaultComment)
