from django.test import TestCase, Client
from django.urls import reverse, resolve
from unittest.mock import patch, Mock
import json

from django.test import SimpleTestCase
from . import views

class URLTests(SimpleTestCase):
    def test_openai_plate_recognition_url(self):
        url = reverse('openai_plate_recognition')
        self.assertEqual(resolve(url).func, views.openai_plate_recognition)

class ALPRTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('openai_plate_recognition')

    @patch('alpr.views.client')
    def test_valid_request(self, MockClient):
        mock_response = Mock()
        mock_response.choices = [
            Mock(message=Mock(content='Number Plate: ABC123.\nExpired Time: 2024-12-31'))
        ]
        mock_response.usage = Mock(prompt_tokens=10, completion_tokens=10, total_tokens=20)
        MockClient.chat.completions.create.return_value = mock_response

        data = {
            "url": "http://example.com/image.jpg"
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "url": "http://example.com/image.jpg",
            "answer": "Number Plate: ABC123.\nExpired Time: 2024-12-31",
            "number_plate": "ABC123",
            "expired_time": "2024-12-31",
            "message_tokens": 10,
            "response_tokens": 10,
            "total_tokens": 20
        })

    def test_invalid_request_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Invalid request method'})

    def test_invalid_json(self):
        response = self.client.post(self.url, 'invalid json', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Invalid JSON data'})

    def test_missing_url(self):
        data = {}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'URL to image is required'})

    @patch('alpr.views.client')
    def test_unexpected_error(self, MockClient):
        MockClient.chat.completions.create.side_effect = Exception("Mocked exception")
        
        data = {
            "url": "http://example.com/image.jpg"
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json())
        self.assertIn('An unexpected error occurred', response.json()['error'])
