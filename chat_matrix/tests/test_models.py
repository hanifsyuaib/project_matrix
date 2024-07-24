from django.test import TestCase
from django.contrib.auth.models import User
from chat_matrix.models import ChatSentimentAnalysis, ChatSummary
from datetime import datetime

class ChatSentimentAnalysisModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser', 
            password='password'
        )
        self.chat = ChatSentimentAnalysis.objects.create(
            user=self.user,
            message='Test message',
            response='Test response',
            sentiment='Positive',
            reason='The response was encouraging',
            message_tokens=5,
            response_tokens=4,
            total_tokens=9
        )

    def test_chat_sentiment_analysis_creation(self):
        self.assertEqual(self.chat.user, self.user)
        self.assertEqual(self.chat.message, 'Test message')
        self.assertEqual(self.chat.response, 'Test response')
        self.assertEqual(self.chat.sentiment, 'Positive')
        self.assertEqual(self.chat.reason, 'The response was encouraging')
        self.assertEqual(self.chat.message_tokens, 5)
        self.assertEqual(self.chat.response_tokens, 4)
        self.assertEqual(self.chat.total_tokens, 9)
        self.assertTrue(isinstance(self.chat.created_at, datetime))

    def test_chat_sentiment_analysis_string_representation(self):
        expected_str = f'{self.user.username}: Test message'
        self.assertEqual(str(self.chat), expected_str)


class ChatSummaryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='password')
        self.chat_summary = ChatSummary.objects.create(
            user=self.user,
            message='Test message',
            response='Test response',
            summary='This is a summary',
            keywords='summary, test',
            message_tokens=5,
            response_tokens=4,
            total_tokens=9
        )

    def test_chat_summary_creation(self):
        self.assertEqual(self.chat_summary.user, self.user)
        self.assertEqual(self.chat_summary.message, 'Test message')
        self.assertEqual(self.chat_summary.response, 'Test response')
        self.assertEqual(self.chat_summary.summary, 'This is a summary')
        self.assertEqual(self.chat_summary.keywords, 'summary, test')
        self.assertEqual(self.chat_summary.message_tokens, 5)
        self.assertEqual(self.chat_summary.response_tokens, 4)
        self.assertEqual(self.chat_summary.total_tokens, 9)
        self.assertTrue(isinstance(self.chat_summary.created_at, datetime))

    def test_chat_summary_string_representation(self):
        expected_str = f'{self.user.username}: Test message'
        self.assertEqual(str(self.chat_summary), expected_str)
