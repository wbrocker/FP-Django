from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import AlarmConfig


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
                                                  