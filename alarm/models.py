from django.db import models
from django.core.exceptions import ValidationError
from enum import Enum

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
    status = models.CharField(max_length=3,
                                 choices=ALARM_STATUS.choices,
                                 default=ALARM_STATUS.OFF)
    # Alarm Type?
    type = models.CharField(max_length=3,
                            choices=ALARM_TYPES.choices,
                            default=ALARM_TYPES.AUDIBLE)
    
    # Current Alarm
    current_type = models.CharField(max_length=3,
                                    choices=ALARM_TYPES.choices,
                                    default=ALARM_TYPES.OFF)

    def __str__(self):
        return f"Alarm: { self.get_status_display() } Type: { self.get_type_display()}"

    def save(self, *args, **kwargs):
        # Enforce singleton behaviour by checking if any instance exist
        existing_instance = AlarmConfig.objects.first()
        if existing_instance and existing_instance.pk != self.pk:
            raise ValidationError("Only once instance allowed!")
        
        super(AlarmConfig, self).save(*args, **kwargs)