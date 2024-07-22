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

def ask_openai(message):
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages =[
            {
                "role": "system", 
                "content": '''
                                You are an helpful assistant called ChatMatrix. 
                                Have nothing related to openai and chatgpt.
                                User will give a review and your job is to do sentiment analysis,
                                which grouped them into "Positive", "Negative", or "Neutral".   

                            '''
            },
            {
                "role": "user", "content": message
            },
        ],
        max_tokens = 300
    )
    

    # Retrieve token usage
    token_usage = response.usage
    print(f"\nMessage: {message}\nToken Used: {token_usage}\n")

    answer = response.choices[0].message.content.strip()
    return answer

@login_required(login_url='http://localhost:8080/login') # Soon to be changed
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response, 'username': request.user.username})
    
    # For GET requests, return existing chats
    chats = Chat.objects.filter(user=request.user)
    chat_data = [{'message': chat.message, 'response': chat.response, 'username': request.user.username} for chat in chats]
    return JsonResponse({'chats': chat_data})

def logout(request):
    auth.logout(request)
    return JsonResponse({'success': True})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            csrf_token = get_token(request)
            return JsonResponse({'success': True, 'csrfToken': csrf_token, 'redirect_url': '/chatbot/'})
        else:
            return JsonResponse({'success': False, 'error_message': 'Invalid username or password'}, status=400)

    return JsonResponse({'success': False, 'error_message': 'Invalid request method'}, status=400)

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