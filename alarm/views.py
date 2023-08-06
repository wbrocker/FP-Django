from django.shortcuts import render, redirect
from .models import AlarmConfig

def ChangeAlarmStatus(request):
    """
    Arm or Disarm the alarm
    """
    alarm = AlarmConfig.objects.get(pk=1)

    if alarm.status == AlarmConfig.ALARM_STATUS.ON:
        alarm.status = AlarmConfig.ALARM_STATUS.OFF
    else:
        alarm.status = AlarmConfig.ALARM_STATUS.ON

    alarm.save()

    return redirect('dashboard:dash')

