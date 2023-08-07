from django.db import models
from enum import Enum
from django.utils.translation import gettext_lazy as _
from django.db.models import Count


class Locations(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name
        # Count the devices per room.
        # devices_count = self.devices.aggregate(total_devices=Count('id'))['total_devices']
        # return str(devices_count)

class ActiveDevices(models.Model):
    
    class Type(models.TextChoices):
        CAM = 'CAM', 'Camera'
        SENSOR = 'SEN', 'Sensor'

    class Status(models.TextChoices):
        ACTIVE = 'ACT', 'Active'
        INACTIVE = 'INA', 'Inactive'
        DISCOVERED = 'DIS', 'Discovered'
        UNKNOWN = 'UNK', 'Unknown'
        ERROR = "ERR", "Error"

    type = models.CharField(max_length=3,
                            choices=Type.choices,
                            default=Type.CAM)
    name = models.CharField(max_length=100, default='No Name', null=True, blank=True)
    description = models.CharField(max_length=255, default='', null=True, blank=True)
    location = models.ForeignKey(Locations,
                                 on_delete=models.RESTRICT,
                                 related_name='devices')
    status = models.CharField(max_length=3,
                              choices=Status.choices,
                              default=Status.DISCOVERED)
    data = models.JSONField(null=True)
    ip = models.CharField(max_length=20, default='0.0.0.0')
    firmware = models.CharField(max_length=20, default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


