from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from chat_matrix.models import ChatSentimentAnalysis, ChatSummary
import json
from unittest.mock import patch

class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_success(self):
        response = self.client.post(self.register_url, json.dumps({
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'password123',
            'password2': 'password123'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(response.content, {'success': True})

    def test_register_password_mismatch(self):
        response = self.client.post(self.register_url, json.dumps({
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'password123',
            'password2': 'password456'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'success': False, 'error_message': 'Passwords do not match'})

    def test_register_invalid_method(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(response.content, {'success': False, 'error_message': 'Invalid request method'})


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login_success(self):
        response = self.client.post(self.login_url, json.dumps({
            'username': 'testuser',
            'password': 'password123'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})

    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, json.dumps({
            'username': 'testuser',
            'password': 'wrongpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'success': False, 'error_message': 'Invalid username or password'})

    def test_login_invalid_method(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(response.content, {'success': False, 'error_message': 'Invalid request method'})


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('logout')
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_logout_success(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})

    def test_logout_invalid_method(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(response.content, {'success': False, 'error_message': 'Invalid request method'})

class SummaryViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.summary_url = reverse('summary')
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    @patch('chat_matrix.views.openai_summary')
    def test_summary_post_success(self, mock_openai_summary):
        mock_openai_summary.return_value = {
            'answer': 'Summary:\nIni adalah pesan uji untuk disummary.\n\nKeywords:\n[uji, pesan, summarization]',
            'message_tokens': 10,
            'response_tokens': 20,
            'total_tokens': 30
        }
        response = self.client.post(self.summary_url, json.dumps({
            'message': 'This is a test message for summarization.'
        }), content_type='application/json')

        expected_response = {
            'message': 'This is a test message for summarization.',
            'response': 'Summary:\nIni adalah pesan uji untuk disummary.\n\nKeywords:\n[uji, pesan, summarization]'
        }
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_response)

    def test_summary_get(self):
        ChatSummary.objects.create(user=self.user, message='Test message', response='Summary response here')
        response = self.client.get(self.summary_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('chats', response.json())
        self.assertIn('username', response.json())

    def test_summary_unauthorized(self):
        self.client.logout()
        response = self.client.post(self.summary_url, json.dumps({
            'message': 'This should fail due to unauthorized user.'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {'error_message': 'Unauthorized'})


class SentimentAnalysisViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.sentiment_analysis_url = reverse('sentiment_analysis')
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    @patch('chat_matrix.views.openai_sentiment_analysis')
    def test_sentiment_analysis_post_success(self, mock_openai_sentiment_analysis):
        mock_openai_sentiment_analysis.return_value = {
            'answer': 'Sentiment: Neutral\nReason: The review does not express any strong positive or negative emotions, indicating a neutral sentiment.',
            'message_tokens': 10,
            'response_tokens': 20,
            'total_tokens': 30
        }
        response = self.client.post(self.sentiment_analysis_url, json.dumps({
            'message': 'This is a test message for sentiment analysis.'
        }), content_type='application/json')

        expected_response = {
            'message': 'This is a test message for sentiment analysis.',
            'response': 'Sentiment: Neutral\nReason: The review does not express any strong positive or negative emotions, indicating a neutral sentiment.'
        }
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_response)

    def test_sentiment_analysis_get(self):
        ChatSentimentAnalysis.objects.create(user=self.user, message='Test message', response='Sentiment response here')
        response = self.client.get(self.sentiment_analysis_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('chats', response.json())
        self.assertIn('username', response.json())

    def test_sentiment_analysis_unauthorized(self):
        self.client.logout()
        response = self.client.post(self.sentiment_analysis_url, json.dumps({
            'message': 'This should fail due to unauthorized user.'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {'error_message': 'Unauthorized'})

class DashboardViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.dashboard_url = reverse('dashboard')
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_dashboard_unauthorized(self):
        self.client.logout()
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {'error_message': 'Unauthorized'})

    def test_dashboard_success(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True,  'username': 'testuser'})

    def test_dashboard_invalid_method(self):
        response = self.client.post(self.dashboard_url)
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(response.content, {'success': False, 'error_message': 'Invalid request method'})

class GetCSRFTokenViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.get_csrf_token_url = reverse('get_csrf_token')

    def test_get_csrf_token(self):
        response = self.client.get(self.get_csrf_token_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('csrftoken', response.json())
