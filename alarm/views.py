from django.shortcuts import render, redirect, get_object_or_404
from .models import AlarmConfig, DetectionObjects
from .forms import AlarmForm
from audit.utils import Audit

def ChangeAlarmStatus(request):
    """
    Arm or Disarm the alarm
    """
    alarm = AlarmConfig.objects.get(pk=1)

    if alarm.status == AlarmConfig.ALARM_STATUS.ON:
        alarm.status = AlarmConfig.ALARM_STATUS.OFF
        Audit("ALA", "Alarm Disarmed", "Alarm")
    else:
        alarm.status = AlarmConfig.ALARM_STATUS.ON
        Audit("ALA", "Alarm Armed", "Alarm")

    alarm.save()

    return redirect('dashboard:dash')


def AlarmConfigView(request):
    """
    Set or change the current Alarm
    Configuration
    """
    alarm_config = AlarmConfig.objects.first()

    if request.method == 'POST':
        form = AlarmForm(request.POST, instance=alarm_config)

        if form.is_valid():
            instance = form.save()

            return redirect('dashboard:dash')
    
        else:
            print(form.errors)

    else:
        form = AlarmForm(instance=alarm_config)

    return render(request, 'alarm/alarmconfig.html', 
                  {
                    "form": form,
                   "alarm": alarm_config
                   })


def AlarmDetectionObjects(request):
    """
    Edit or Update the objects that should activate
    the alarm if detected.
    """
    alarm_config = AlarmConfig.objects.first()
    det_objects = DetectionObjects.objects.all()

    return render(request,
                  'alarm/objects.html',
                  {
                      "detection": det_objects,
                      "alarm": alarm_config
                  })

def ToggleObject(request):
    """
    Toggle the detection status of the
    selected object
    """
    alarm_config = AlarmConfig.objects.first()
    obj_id = request.GET.get('obj')
    det_obj = get_object_or_404(DetectionObjects, id=obj_id)
    det_objects = DetectionObjects.objects.all()

    if det_obj.alarm_on_object:
        det_obj.alarm_on_object = False
    else:
        det_obj.alarm_on_object = True

    det_obj.save()

    return redirect('alarm:alarm-detection')

def AckAlarm(request):
    """
    Acknowledge Alarm from Dash
    """
    Audit("ALA", "Alarm Acknowledged from Dashboard", "Alarm")
    alarm = AlarmConfig.objects.first()
    alarm_status = alarm.current_type

    alarm.current_type = AlarmConfig.ALARM_TYPES.OFF
    alarm.save()
    
    return redirect('dashboard:dash')