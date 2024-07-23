from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField() # Input from User
    response = models.TextField() # Output/response from System
    created_at = models.DateTimeField(auto_now_add=True)
    message_tokens = models.IntegerField(validators=[MinValueValidator(0)])
    response_tokens = models.IntegerField(validators=[MinValueValidator(0)])
    total_tokens = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.user.username}: {self.message}'