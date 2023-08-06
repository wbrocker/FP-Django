from django.shortcuts import render, redirect, get_object_or_404
from .models import AlarmConfig
from .forms import AlarmForm

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
                  {'form': form})