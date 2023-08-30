import paho.mqtt.client as mqtt
from django.test import TestCase, Client
from django.conf import settings 
from unittest.mock import Mock, patch
from devices.models import ActiveDevices
from mqtt.mqtt import on_connect, on_message
from mqtt.views import publish_message
import json


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

class PublishMessageViewTest(TestCase):

    @patch('mqtt.views.publish_message')
    def test_publish_message_success(self, mock_publish):
        # Arrange
        mock_request = Mock()
        mock_request.body = json.dumps({'topic': 'test/topic',
                                        'msg': 'Hello'})
        mock_publish.return_value = (0,1)

        response = publish_message(mock_request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'code': 0})

    @patch('mqtt.views.publish_message')
    def test_publish_message_failure(self, mock_publish):
        # Arrange
        mock_request = Mock()
        mock_request.body = json.dumps({'topic': 'test/topic', 'msg': 'Hello'})
        mock_publish.return_value = (1, 1)      # Mocking a publish failure

        response = publish_message(mock_request)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'code': 0})

    def test_publish_message_invalid_request(self):
        # Arrange
        client = Client()
        invalid_data = {'invalid_key': 'value'}

        # Act
        response = client.post('/mqtt/publish_message/', json.dumps(invalid_data), content_type='application/json')

        # Assert
        self.assertEqual(response.status_code, 404)