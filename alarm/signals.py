from django.db.models.signals import post_save
from django.dispatch import receiver
from alarm.models import AlarmConfig

from devices.utils import ChangeCamStatus, ActivateOrDeactivateAlarm
from mqtt.mqtt import client as mqtt_client

@receiver(post_save, sender=AlarmConfig)
def active_and_log_alarm(sender, instance, created, **kwargs):
    event_type = "Alarm Created" if created else "Alarm Updated"
    print("Signal Invoked!")

    # Activate Cameras as well as ESP8266
    alarm_trig_msg = 0

    if instance.status == AlarmConfig.ALARM_STATUS.OFF:
        print("Deactivating Alarm!")
        alarm_msg = 0
        ActivateOrDeactivateAlarm(False)                # Deactivate Camera
        # ChangeCamStatus(0)
    elif instance.status == AlarmConfig.ALARM_STATUS.ON:
        print("Activating Alarm!")
        alarm_msg = 1
        ActivateOrDeactivateAlarm(True)                 # Activate Camera
        # ChangeCamStatus(1)

    if instance.current_type == AlarmConfig.ALARM_TYPES.AUDIBLE:
        alarm_trig_msg = 1
    elif instance.current_type == AlarmConfig.ALARM_TYPES.VISUAL:
        alarm_trig_msg = 2
    elif instance.current_type == AlarmConfig.ALARM_TYPES.BOTH:
        alarm_trig_msg = 3

    print("Alarm Status: " + str(alarm_trig_msg))
    rc, mid = mqtt_client.publish('alarmtrigger', alarm_trig_msg)
    rc, mid = mqtt_client.publish('alarm', alarm_msg)