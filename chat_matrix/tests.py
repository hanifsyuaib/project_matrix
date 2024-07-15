from django.test import TestCase, Client
from django.urls import reverse
import json

class ChatMatrixTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')

    def test_home_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
