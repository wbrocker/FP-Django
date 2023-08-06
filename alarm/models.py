from django.db import models
from django.core.exceptions import ValidationError
from enum import Enum


# This table will keep a list of all objects
# that have been detected.
class DetectionObjects(models.Model):
    name = models.CharField(max_length=100)
    name_cleaned = models.CharField(max_length=100, blank=True)
    alarm_on_object = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    # Create the name_cleaned with a default value
    def save(self, *args, **kwargs):
        if not self.name_cleaned:
            self.name_cleaned = self.name
        super(DetectionObjects, self).save(*args, **kwargs)


class AlarmConfig(models.Model):

    class ALARM_STATUS(models.TextChoices):
        ON = 'ON', 'On'
        OFF = 'OFF', 'Off'

    class ALARM_TYPES(models.TextChoices):
        AUDIBLE = 'AUD', 'Audible'
        VISUAL = 'VIS', 'Visual'
        BOTH = 'BOT', 'Audible and Visual'
        OFF = 'OFF', 'Off'

    # On or Off
    status = models.CharField('Current Alarm Status',
                              max_length=3,
                                 choices=ALARM_STATUS.choices,
                                 default=ALARM_STATUS.OFF)
    # Alarm Type?
    type = models.CharField('Alarm Type',
                            max_length=3,
                            choices=ALARM_TYPES.choices,
                            default=ALARM_TYPES.AUDIBLE)
    
    # Current Alarm
    current_type = models.CharField(max_length=3,
                                    choices=ALARM_TYPES.choices,
                                    default=ALARM_TYPES.OFF)
    
    # Objects that should be alarmed on
    # alarm_objects = models.ManyToManyField(DetectionObjects, default='all')
    alarm_objects = models.BooleanField('Alarm on Object Recognition', default=False)      # Alarm on Objects

    # Score for items to alert on
    score = models.DecimalField(max_digits=4, decimal_places=3, default=0.5)

    def __str__(self):
        return f"Alarm: { self.get_status_display() } Type: { self.get_type_display()}"

    def save(self, *args, **kwargs):
        # Enforce singleton behaviour by checking if any instance exist
        existing_instance = AlarmConfig.objects.first()
        if existing_instance and existing_instance.pk != self.pk:
            raise ValidationError("Only once instance allowed!")
        
        super(AlarmConfig, self).save(*args, **kwargs)