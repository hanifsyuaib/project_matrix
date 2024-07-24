from django.test import SimpleTestCase
from django.urls import reverse, resolve
from chat_matrix import views

class URLTests(SimpleTestCase):
    def test_get_csrf_token_url(self):
        url = reverse('get_csrf_token')
        self.assertEqual(resolve(url).func, views.get_csrf_token)

    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, views.register)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, views.login)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, views.logout)

    def test_sentiment_analysis_url(self):
        url = reverse('sentiment_analysis')
        self.assertEqual(resolve(url).func, views.sentiment_analysis)

    def test_summary_url(self):
        url = reverse('summary')
        self.assertEqual(resolve(url).func, views.summary)