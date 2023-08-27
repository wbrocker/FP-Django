from django.test import TestCase
from django.urls import reverse
from django.shortcuts import redirect,render
from django.utils import timezone
import json

from .models import Locations, ActiveDevices
from alarm.models import AlarmConfig

from .forms import DeviceForm, LocationForm, PicIntervalForm


# Models Testcases
class ActiveDevicesModelTest(TestCase):

    def setUp(self):
        # Create test location for Foreign keys
        self.location = Locations.objects.create(name='Test Location')

        # Create a test ActiveDevices instance
        self.device = ActiveDevices.objects.create(
            type=ActiveDevices.Type.CAM,
            name='Test Camera',
            description='This is a test',
            location = self.location,
            status=ActiveDevices.Status.DISCOVERED,
            data={'key':'value'},
            ip='192.168.2.1',
            firmware='0.1'
        )

        def test_str_representation(self):
            # Test that the __str__ method return correctly.
            self.assertEqual(str(self.device), 'Discovered')

        
        def test_default_values(self):
            # Testing thed default values for fields
            device = ActiveDevices.objecs.create(type=ActiveDevices.Type.SENSOR)
            self.assertEqual(device.name, 'No Name')
            self.assertIsNone(device.description)
            self.assertIsNone(device.data)
            self.assertEqual(device.ip, '0.0.0.0')
            self.assertEqual(device.firmware, '')


        def test_type_choices(self):
            # Test the choices for the 'type' field
            self.assertEqual(self.device.type, ActiveDevices.Type.CAM)
            device = ActiveDevices.objects.create(type=ActiveDevices.Type.SENSOR)
            self.assertEqual(device.type, ActiveDevices.Type.SENSOR)


        def test_location_foreign_key(self):
            # Test the ForeignKey relationship with Locations
            self.assertEqual(self.device.location, self.location)


        def test_created_and_updated_fields(self):
            # Test the auto_now_add and auto_now fields
            now = timezone.now()
            device = ActiveDevices.objects.create(type=ActiveDevices.Type.CAM)
            self.assertIsNotNone(device.created)
            self.assertIsNotNone(device.updated)
            self.assertLessEqual(device.created, now)
            self.assertLessEqual(device.updated, now)

        def test_status_choices(self):
            # Test the choices for the 'status' field
            self.assertEqual(self.device.status, ActiveDevices.Status.DISCOVERED)
            device = ActiveDevices.objects.create(status=ActiveDevices.Status.ACTIVE)
            self.assertEqual(device.status, ActiveDevices.Status.ACTIVE)


        def test_model_methods(self):
            # Testing custom methods.
            self.assertTrue(self.device.is_active_device())
    
# Views testCases
class DevicesListViewsTests(TestCase):
    def setUp(self):
        # Setup Location
        self.location = Locations.objects.create(name='Location1')
        
        # Test creating an AlarmConfig instance
        alarm_config = AlarmConfig.objects.create()
        self.assertEqual(alarm_config.status, AlarmConfig.ALARM_STATUS.OFF)
        self.assertEqual(alarm_config.type, AlarmConfig.ALARM_TYPES.AUDIBLE)
        self.assertEqual(alarm_config.current_type, AlarmConfig.ALARM_TYPES.OFF)


        # Create instances of ActiveDevices
        ActiveDevices.objects.create(
            type=ActiveDevices.Type.CAM,
            name='Camera1',
            description='Test Camera',
            location=self.location,
            status=ActiveDevices.Status.ACTIVE,
            data={'key':'value'},
            ip='192.168.2.1',
            firmware='0.1'
        )


    def test_deviceList_view(self):
        # Test the 'deviceList' view
        url = reverse('devices:device-home')
        response = self.client.get(url)

        # Confirm a 200 status code is returned
        self.assertEqual(response.status_code, 200)
        
        # Confirm the response contains the expected variables
        self.assertQuerysetEqual(
            response.context['devices'],
            ActiveDevices.objects.all(),
            transform=lambda x: x
        )

        # Confirm that the correct template is used for redering.
        self.assertTemplateUsed(response, 'devices/devices.html')


class DeviceFormTestCase(TestCase):
    def test_location_form_valid(self):
        # Test the form with valid data
        form_data = {
            'name': 'Test Location',
            'description': 'Test Description'
        }

        form = LocationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_location_form_missing_data(self):
        # Test the form with missing required data
        form_data = {
            'name': '',
            'description':''
        }

        form = LocationForm(data=form_data)
        self.assertFalse(form.is_valid())



class RegisterDeviceViewTestCase(TestCase):
    def setUp(self):
        # Create a test Location instance for Foreignkey
        self.location = Locations.objects.create(name='Test Location')

    def test_existing_device_update(self):
        # Test updating of existing device
        device = ActiveDevices.objects.create(
            ip='192.168.1.100',
            name='Test Device',
            type=ActiveDevices.Type.CAM,
            location=self.location,
            status=ActiveDevices.Status.ACTIVE,
            data={'camStatus': False},
            firmware='0.1'
        )

        url = reverse('devices:register-device')
        params = {
            'ip': '192.168.1.100',
            'host': 'Test Device',
            'type': ActiveDevices.Type.CAM,
            'firmware': '0.2'
        }

        response = self.client.get(url, params)

        # Assert the view returns JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        # Assert the Firmware is updated
        device.refresh_from_db()
        self.assertEqual(device.firmware, '0.2')

        # Confirm the JSON response contains the updated data
        expected_data = {
            'camStatus': True,
            'cameraid': 1,
            # 'flash': False,
            # 'picInterval': 200,
            # 'firmware': '0.2',
            # 'sleep': False,
        }
        self.assertDictContainsSubset(response.json(), expected_data)

    
    def test_new_device_registration(self):
        # Test registering a new device
        url = reverse('devices:register-device')
        params = {
            'ip': '192.168.1.200',
            'host': 'New Device',
            'type': ActiveDevices.Type.SENSOR,
            'firmware': '1.5'
        }

        response = self.client.get(url, params)

        # Check if JSON response is returned.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        # Check that new device was created in the DB
        new_device = ActiveDevices.objects.get(ip='192.168.1.200')
        self.assertEqual(new_device.name, 'New Device')
        self.assertEqual(new_device.type, ActiveDevices.Type.SENSOR)
        self.assertEqual(new_device.firmware, '1.5')

        # Confirm the JSON response contains expected data
        expected_data = {
            'sensorid': 1,
            'alarm': '0',
            'temperature': 0,
            'humidity': 0,
            'alarmtrigger': 0
        }
        self.assertDictContainsSubset(response.json(), expected_data)
        

class EditPicItnervalViewTestCase(TestCase):
    def setUp(self):
        # Test creating an AlarmConfig instance
        self.alarm = AlarmConfig.objects.create()

        # Create test location for Foreign keys
        self.location = Locations.objects.create(name='Test Location')

        # Create a test ActiveDevices instance
        self.device = ActiveDevices.objects.create(
            type=ActiveDevices.Type.CAM,
            name='Test Camera',
            description='This is a test',
            location = self.location,
            status=ActiveDevices.Status.DISCOVERED,
            data={'key':'value'},
            ip='192.168.2.1',
            firmware='0.1'
        )

        self.url = reverse('devices:editpicint', kwargs={'pk': self.device.pk})

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'devices/picint.html')
        self.assertIsInstance(response.context['form'], PicIntervalForm)
        self.assertEqual(response.context['alarm'], self.alarm)
        self.assertEqual(response.context['cam'], self.device)


    def test_valid_post_request(self):
        data = {'picInterval': 5}  # Change this value as needed
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertEqual(response.url, reverse('devices:device-home'))

        # Refresh the cam instance
        self.device.refresh_from_db()
        self.assertEqual(self.device.data['picInterval'], 5)  # Assert the new value is saved

    def test_invalid_post_request(self):
        data = {'picInterval': 'invalid'}  # Invalid value
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'devices/picint.html')
        self.assertIsInstance(response.context['form'], PicIntervalForm)
        self.assertIn('form', response.context)
        self.assertIn('alarm', response.context)
        self.assertIn('cam', response.context)

    def tearDown(self):
        self.alarm.delete()
        self.device.delete()