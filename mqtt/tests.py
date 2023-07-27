import paho.mqtt.client as mqtt
from django.test import TestCase
from django.conf import settings 
from unittest import mock
from devices.models import ActiveDevices
from mqtt.mqtt import on_connect, on_message


class MqttTestCases(TestCase):
    def setUp(self):
        # Setting the mock MQTT Client
        self.mqtt_client = mqtt.Client()

    # @mock.patch('mqtt.ActiveDevices.objects.get')
    # def test_on_connect_success(self, mock_get):
    #     # Mock the subscribe method
    #     with mock.patch.object(self.mqtt_client, 'subscribe') as mock_subscribe:
    #         on_connect(self.mqtt_client, None, None, 0)

    #     # Confirm subscription
    #     expected_topics = ['alarms', 'esp/#']
    #     mock_subscribe.assert_called_with(expected_topics)

    # @mock.patch('mqtt.ActiveDevices.objects.get')
    # def test_on_message_device_status_update(self, mock_get):
    #     # Mock the ActiveDevices object returned by objects.get
    #     mock_device = mock.Mock()
    #     mock_device.status = ActiveDevices.Status.ACTIVE
    #     mock_get.return_value = mock_device

    #     # Mock the MQTT message
    #     mock_msg = mock.Mock()
    #     mock_msg.topic = 'esp/lwt/40'
    #     mock_msg.payload = b'hello'

    #     # Call the on_message function
    #     on_message(self.mqtt_client, None, mock_msg)

    #     # Assert that the device's status is updated
    #     self.assertEqual(mock_device.status, ActiveDevices.Status.ACTIVE)