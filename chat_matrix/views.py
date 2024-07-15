from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat

from django.utils import timezone
from django.contrib.auth.decorators import login_required

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
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
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