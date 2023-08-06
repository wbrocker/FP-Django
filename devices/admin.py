from django.contrib import admin
from .models import Locations, ActiveDevices

# Register your models here.
admin.site.register(Locations)
admin.site.register(ActiveDevices)