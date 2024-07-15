from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import logout as auth_logout

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

@login_required(login_url='/login')
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    
    # For GET requests, return existing chats
    chats = Chat.objects.filter(user=request.user)
    chat_data = [{'message': chat.message, 'response': chat.response} for chat in chats]
    return JsonResponse({'chats': chat_data})

@ensure_csrf_cookie
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return JsonResponse({'success': True, 'redirect_url': '/chatbot/'})
        else:
            return JsonResponse({'success': False, 'error_message': 'Invalid username or password'}, status=400)

    return JsonResponse({'success': False, 'error_message': 'Invalid request method'}, status=400)


@csrf_exempt # Later on, handle csrf token correctly
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
                return JsonResponse({'success': True, 'redirect_url': 'chatbot'}, status=201)
            except:
                return JsonResponse({'success': False, 'error_message': 'Error creating account'}, status=400)
        else:
            return JsonResponse({'success': False, 'error_message': 'Passwords do not match'}, status=400)
    return JsonResponse({'success': False, 'error_message': 'Invalid request method'}, status=405)

def logout(request):
    auth_logout(request)
    return redirect('login')


def onboarding(request):
    context = {
        'message': "Welcome to the Onboarding Page!"
    }
    return render(request, 'chat_matrix_onboarding.html', context)

def home(request):
    context = {
        'message': "Welcome to the Home Page!"
    }
    return render(request, 'chat_matrix_home.html', context)

def chatting(request):
    context = {
        'message': "Welcome to the Chatting Page!"
    }
    return render(request, 'chat_matrix_chatting.html', context)