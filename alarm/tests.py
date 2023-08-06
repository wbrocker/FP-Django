from django.test import TestCase, RequestFactory
from django.urls import path
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import AlarmConfig
from .views import ChangeAlarmStatus


class AlarmConfigModelTestCase(TestCase):

    def test_create_alarm_config(self):
        # Test creating an AlarmConfig instance
        alarm_config = AlarmConfig.objects.create()
        self.assertEqual(alarm_config.status, AlarmConfig.ALARM_STATUS.OFF)
        self.assertEqual(alarm_config.type, AlarmConfig.ALARM_TYPES.AUDIBLE)
        self.assertEqual(alarm_config.current_type, AlarmConfig.ALARM_TYPES.OFF)

    def test_singleton(self):
        # Test enforcing singleton behaviour by preventing multiple entries
        alarm_config = AlarmConfig.objects.create()
        with self.assertRaises(ValidationError):
            # Attempt to create another AlarmConfig instance
            duplicate = AlarmConfig.objects.create()


    def test_update_alarm_config(self):
        # test updating an existing AlarmConfig instance
        alarm_config = AlarmConfig.objects.create(status=AlarmConfig.ALARM_STATUS.ON)
        # Change the status and type
        alarm_config.status = AlarmConfig.ALARM_STATUS.OFF
        alarm_config.type = AlarmConfig.ALARM_TYPES.VISUAL
        alarm_config.save()
        updated_alarm_config = AlarmConfig.objects.get(pk=alarm_config.pk)
        self.assertEqual(updated_alarm_config.status, AlarmConfig.ALARM_STATUS.OFF)
        self.assertEqual(updated_alarm_config.type, AlarmConfig.ALARM_TYPES.VISUAL)

    def test_string_representation(self):
        # Test the string representation of the AlarmConfig instance
        alarm_config = AlarmConfig.objects.create(status=AlarmConfig.ALARM_STATUS.ON,
                                                  type=AlarmConfig.ALARM_TYPES.BOTH)
        expected_string = f"Alarm: On Type: Audible and Visual"
        self.assertEqual(str(alarm_config), expected_string)
                                                  

# class ChangeAlarmStatusViewTestCase(TestCase):

#     def setUp(self):
#         # Set up a factory to create requests
#         self.factory = RequestFactory


#     def test_change_alarm_status_on_to_off(self):
#         # Test changing alarm status from ON to OFF
#         alarm = AlarmConfig.objects.create(status=AlarmConfig.ALARM_STATUS.ON)
#         url = reverse('alarm:alarm-status')
#         request = self.factory.get(url)
#         response = ChangeAlarmStatus(request)
#         # Check if the alarm status is changed to OFF 
#         self.assertEqual(AlarmConfig.objects.get(pk=alarm.pk).status, AlarmConfig.ALARM_STATUS.OFF)
#         # Check if the view redirects to the Dash page
#         self.assertRedirects(response, reverse('dashboard:dash'))

#     def test_change_alarm_status_off_to_on(self):
#         # Test changing alarm status from OFF to ON
#         alarm = AlarmConfig.objects.create(status=AlarmConfig.ALARM_STATUS.OFF)
#         url = reverse('alarm:alarm-status')
#         request = self.factory.get(url)
#         response = ChangeAlarmStatus(request)
#         # Check if the alarm status is changed to ON
#         self.assertEqual(AlarmConfig.objects.get(pk=alarm.pk).status, AlarmConfig.ALARM_STATUS.ON)
#         # Check if the view redirects to the dashboard page
#         self.assertRedirects(response, reverse('dashboard:dash'))