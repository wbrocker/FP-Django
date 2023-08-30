import paho.mqtt.client as mqtt
from django.test import TestCase, Client
from django.conf import settings 
from unittest.mock import Mock, patch
from devices.models import ActiveDevices
from mqtt.mqtt import on_connect, on_message
from mqtt.views import publish_message
import json


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