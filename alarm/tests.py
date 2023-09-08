from django.test import TestCase, RequestFactory
from django.shortcuts import get_object_or_404
from unittest.mock import patch
from django.urls import path
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import AlarmConfig, DetectionObjects
from imgcapture.models import ImageDetection
from .views import ChangeAlarmStatus
from alarm.utils import checkAlarm


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


class DetectionObjectsTestCase(TestCase):
    def setUp(self):
        # Create sample detection objects for testing
        DetectionObjects.objects.create(name='Object1', name_cleaned='ObjectCleaned', alarm_on_object=True)
        DetectionObjects.objects.create(name='Object2', alarm_on_object=False)
        DetectionObjects.objects.create(name='Object3', name_cleaned='', alarm_on_object=True)

    def test_str_method(self):
        # Test the __str__ method.
        obj1 = DetectionObjects.objects.get(name='Object1')
        obj2 = DetectionObjects.objects.get(name='Object2')
        obj3 = DetectionObjects.objects.get(name='Object3')
        self.assertEqual(str(obj1), 'Object1')
        self.assertEqual(str(obj2), 'Object2')
        self.assertEqual(str(obj3), 'Object3')

    def test_default_name_cleaned(self):
        # Test that the name_cleaned field is set to the name by default
        obj1 = DetectionObjects.objects.get(name='Object1')
        obj2 = DetectionObjects.objects.get(name='Object2')
        self.assertEqual(obj1.name_cleaned, 'ObjectCleaned')
        self.assertEqual(obj2.name, 'Object2')           

    def test_alarm_on_object_default(self):
        # Test the default value for alarm_on
        obj1 = DetectionObjects.objects.get(name='Object1')
        obj2 = DetectionObjects.objects.get(name='Object2')
        self.assertTrue(obj1.alarm_on_object)
        self.assertFalse(obj2.alarm_on_object)


class CheckAlarmTestCase(TestCase):
    def setUp(self):
        self.alarm = AlarmConfig.objects.create(status='ON', score=0.5)
        self.detect_object1 = DetectionObjects.objects.create(name='Person', alarm_on_object=True)
        self.detect_object2 = DetectionObjects.objects.create(name='Car', alarm_on_object=True)
        self.detect_object3 = DetectionObjects.objects.create(name='Animal', alarm_on_object=False)

    def test_raise_alarm_all_condition_met(self):
        image = ImageDetection.objects.create(detection_data='{"detections": [{"category_name": "Person", "score": 0.6}]}')
        with patch('alarm.utils.json.loads', return_value={'detections': [{'categories': [{'category_name': 'Person', 'score': 0.6}]}]}):
            with patch('builtins.print') as mock_print:
                checkAlarm(image.id)
                mock_print.assert_called_with('Alarm Status: 1')
                
    def test_raise_alarm_specific_object_detected(self):
        image = ImageDetection.objects.create(detection_data='{"detections": [{"categories": [{"category_name": "Car", "score": 0.7}]}]}')
        with patch('alarm.utils.json.loads', return_value={'detections': [{'categories': [{'category_name': 'Car', 'score': 0.7}]}]}):
            with patch('builtins.print') as mock_print:
                checkAlarm(image.id)
                mock_print.assert_called_with('Alarm Status: 1')
        

class AlarmViewsTestCase(TestCase):
    def setUp(self):
        # Create Alarmconfig and DetectionObjects instances for testing
        self.alarm_config = AlarmConfig.objects.create(status='ON')
        self.det_object = DetectionObjects.objects.create(name='Object1', alarm_on_object=True)

    def test_alarm_detection_objects_view(self):
        url = reverse('alarm:alarm-detection')  
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'alarm/objects.html')
        self.assertContains(response, 'Object1')  
        # Add more assertions as needed

    def test_toggle_object_view(self):
        url = reverse('alarm:alarm-obj-toggle')  
        response = self.client.get(url, {'obj': self.det_object.id})

        self.assertEqual(response.status_code, 302)  # Redirect response
        self.det_object.refresh_from_db()
        self.assertEqual(self.det_object.alarm_on_object, False)  

        # Toggle again
        response = self.client.get(url, {'obj': self.det_object.id})
        self.det_object.refresh_from_db()
        self.assertEqual(self.det_object.alarm_on_object, True)
