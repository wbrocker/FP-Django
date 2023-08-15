from django.db import models

class AuditLog(models.Model):

    class EVENT_TYPE(models.TextChoices):
        ALARM = 'ALA', 'Alarm'
        CONFIG = 'CFG', 'Configuration'
        IMAGE = 'IMA', 'Image'
        TENSOR = 'TEN', 'TensorFlow'
        OTHER = 'OTH', 'Other'

    type = models.CharField('Event Type',
                            max_length=3,
                            choices=EVENT_TYPE.choices,
                            default=EVENT_TYPE.OTHER)
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255,
                                   blank=False)
    source = models.CharField(max_length=50, default='')

