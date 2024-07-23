from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import logout
from django.middleware.csrf import get_token

import json

from .models import Chat

import openai
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    )

def openai_sentiment_analysis(message):
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages =[
            {
                "role": "system", 
                "content":  '''
                                You are an helpful assistant called ChatMatrix. 
                                Have nothing related to openai and chatgpt.
                                User will give a review and your job is to do sentiment analysis,
                                which grouped them into "Positive", "Negative", or "Neutral".
                                Make sure to only response either "Positive", "Negative", or "Neutral".   

                            '''
            },
            {
                "role": "user", "content": message
            },
        ],
        max_tokens = 300
    )

    # Retrieve answer and token usage
    token_usage = response.usage

    message_tokens = token_usage.prompt_tokens
    response_tokens = token_usage.completion_tokens
    total_tokens = token_usage.total_tokens
    answer = response.choices[0].message.content.strip()

    return {
            "answer": answer, 
            "message_tokens": message_tokens, 
            "response_tokens": response_tokens, 
            "total_tokens": total_tokens
    }

def sentiment_analysis(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error_message': 'Unauthorized'}, status=401)

    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        result = openai_sentiment_analysis(message)

        chat = Chat(
            user=request.user, 
            message=message, 
            response=result["answer"], 
            created_at=timezone.now(),
            message_tokens=result["message_tokens"],
            response_tokens=result["response_tokens"],
            total_tokens=result["total_tokens"]
        )
        chat.save()
        return JsonResponse({'message': message, 'response': result["answer"]})
    
    # For GET requests, return existing chats
    chats = Chat.objects.filter(user=request.user)
    chat_data = [{'message': chat.message, 'response': chat.response} for chat in chats]
    return JsonResponse({'chats': chat_data, 'username': request.user.username})

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return JsonResponse({'success': True}, status=200)

    return JsonResponse({'success': False, 'error_message': 'Invalid request method'}, status=405)

def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'success': False, 'error_message': 'Invalid username or password'}, status=400)

    return JsonResponse({'success': False, 'error_message': 'Invalid request method'}, status=405)

def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return JsonResponse({'success': True}, status=201)
            except Exception as e:
                return JsonResponse({'success': False, 'error_message': str(e)}, status=400)
        else:
            return JsonResponse({'success': False, 'error_message': 'Passwords do not match'}, status=400)
    
    return JsonResponse({'success': False, 'error_message': 'Invalid request method'}, status=405)

@ensure_csrf_cookie
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrftoken': csrf_token})