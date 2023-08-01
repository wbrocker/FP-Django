# coding: utf-8
from alarm.models import AlarmConfig
alarm = AlarmConfig.objects.get(pk=1)
alarm
alarm.current_type = AlarmConfig.ALARM_TYPES.OFF
alarm.save()
alarm.current_type = AlarmConfig.ALARM_TYPES.ON
alarm.current_type = AlarmConfig.ALARM_TYPES.oFF
alarm.current_type = AlarmConfig.ALARM_TYPES.OFF
alarm.current_type = AlarmConfig.ALARM_TYPES.AUDIBLE
alarm.save()
alarm.current_type = AlarmConfig.ALARM_TYPES.OFF
alarm.save()
alarm
alarm.status = AlarmConfig.ALARM_STATUS.OFF
