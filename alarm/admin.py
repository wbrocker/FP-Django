from django.contrib import admin
from .models import AlarmConfig, DetectionObjects

# Register your models here.
admin.site.register(AlarmConfig)
admin.site.register(DetectionObjects)