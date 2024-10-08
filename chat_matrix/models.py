from django.db import models
from django.contrib.auth.models import User

class ChatSentimentAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField() # Input from User
    response = models.TextField() # Output/response from System
    sentiment = models.TextField(default="")
    reason = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    message_tokens = models.IntegerField(default=0)
    response_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}: {self.message}'

class ChatSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField() # Input from User
    response = models.TextField() # Output/response from System
    summary = models.TextField(default="")
    keywords = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    message_tokens = models.IntegerField(default=0)
    response_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}: {self.message}'

class ChatPlateRecognition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField() # Input from User
    response = models.TextField() # Output/response from System
    number_plate = models.TextField(default="")
    expired_time = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    message_tokens = models.IntegerField(default=0)
    response_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}: {self.message}'