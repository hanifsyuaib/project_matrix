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
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import ChatSentimentAnalysis, ChatSummary, ChatPlateRecognition

import json
import openai
import os
import re

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    )

def openai_plate_recognition(message):
    response = client.chat.completions.create(
          model="gpt-4o-mini",
          messages=[
            {
              "role": "user",
              "content": [
                {"type": "text", 
                 "text": '''
                            Checking Number Plate Recognition and its expired time (down below), 
                            can you identify from the image and return response in this strict format:
                            "Number Plate: <number-plate>. \nExpired Time: <expired-time>"
                         '''
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": message, # Image URL or Base 64 encoded image
                  },
                },
              ],
            }
          ],
          max_tokens=200,
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

def plate_recognition(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error_message': 'Unauthorized'}, status=401)

    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        result = openai_plate_recognition(message)
        number_plate, expired_time = extract_number_plate_and_expired_time(result["answer"])

        chat = ChatPlateRecognition(
            user=request.user, 
            message=message, 
            response=result["answer"], 
            number_plate=number_plate,
            expired_time=expired_time,
            created_at=timezone.now(),
            message_tokens=result["message_tokens"],
            response_tokens=result["response_tokens"],
            total_tokens=result["total_tokens"]
        )
        chat.save()
        return JsonResponse({'message': message, 'response': result["answer"]})
    
    # For GET requests, return existing chats
    chats = ChatPlateRecognition.objects.filter(user=request.user)
    chat_data = [{'message': chat.message, 'response': chat.response} for chat in chats]
    return JsonResponse({'chats': chat_data, 'username': request.user.username})

def extract_number_plate_and_expired_time(formatted_string):
    # Split the string into lines
    lines = formatted_string.split('\n')

    # Extract number plate from the first line
    number_plate_line = lines[0].strip()
    number_plate = number_plate_line.replace('Number Plate:', '').replace('.', '').strip()
    
    # Collect all lines after the first one for the reason
    expired_time_lines = lines[1:]
    expired_time = '\n'.join(line.strip() for line in expired_time_lines).replace('Expired Time:', '').strip()

    return number_plate, expired_time

def openai_summary(message):
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages =[
            {
                "role": "system", 
                "content":  '''
                                You are an helpful assistant called ChatMatrix. 
                                Have nothing related to openai and chatgpt.
                                User will give a text, your job is to summarize it into Bahasa Indonesia 
                                and find keywords then put it into an array bracket.
                                Give response in this strict format: "Summary:\n<summary>\n\nKeywords:\n[<keywords>]"   

                            '''
            },
            {
                "role": "user", "content": message
            },
        ],
        max_tokens = 2000
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

def summary(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error_message': 'Unauthorized'}, status=401)

    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        result = openai_summary(message)
        summary, keywords = extract_summary_and_keywords(result["answer"])

        chat = ChatSummary(
            user=request.user, 
            message=message, 
            response=result["answer"], 
            summary=summary,
            keywords=keywords,
            created_at=timezone.now(),
            message_tokens=result["message_tokens"],
            response_tokens=result["response_tokens"],
            total_tokens=result["total_tokens"]
        )
        chat.save()
        return JsonResponse({'message': message, 'response': result["answer"]})
    
    # For GET requests, return existing chats
    chats = ChatSummary.objects.filter(user=request.user)
    chat_data = [{'message': chat.message, 'response': chat.response} for chat in chats]
    return JsonResponse({'chats': chat_data, 'username': request.user.username})

def extract_summary_and_keywords(formatted_string):
    # Split the string into lines
    lines = formatted_string.split('\n')

    # Extract the summary from the lines between 'Summary:' and 'Keywords:'
    summary_start_index = lines.index('Summary:') + 1
    keywords_start_index = lines.index('Keywords:')
    
    # Extract summary
    summary_lines = lines[summary_start_index:keywords_start_index - 1]
    summary = '\n'.join(line.strip() for line in summary_lines)
    
    # Extract keywords
    keywords_line = lines[keywords_start_index + 1].strip()
    if keywords_line.startswith('[') and keywords_line.endswith(']'):
        keywords = keywords_line[1:-1].strip()
    else:
        keywords = ''

    return summary, keywords

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
                                Give response in this strict format: "Sentiment: <sentiment>. \nReason:\n<reason>"   

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
        sentiment, reason = extract_sentiment_and_reason(result["answer"])

        chat = ChatSentimentAnalysis(
            user=request.user, 
            message=message, 
            response=result["answer"], 
            sentiment=sentiment,
            reason=reason,
            created_at=timezone.now(),
            message_tokens=result["message_tokens"],
            response_tokens=result["response_tokens"],
            total_tokens=result["total_tokens"]
        )
        chat.save()
        return JsonResponse({'message': message, 'response': result["answer"]})
    
    # For GET requests, return existing chats
    chats = ChatSentimentAnalysis.objects.filter(user=request.user)
    chat_data = [{'message': chat.message, 'response': chat.response} for chat in chats]
    return JsonResponse({'chats': chat_data, 'username': request.user.username})

def extract_sentiment_and_reason(formatted_string):
    # Split the string into lines
    lines = formatted_string.split('\n')

    # Extract sentiment from the first line
    sentiment_line = lines[0].strip()
    sentiment = sentiment_line.replace('Sentiment:', '').replace('.', '').strip()
    
    # Collect all lines after the first one for the reason
    reason_lines = lines[1:]
    reason = '\n'.join(line.strip() for line in reason_lines).replace('Reason:', '').strip()

    return sentiment, reason

def dashboard(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return JsonResponse({'error_message': 'Unauthorized'}, status=401)

        return JsonResponse({'success': True, 'username': request.user.username}, status=200)

    return JsonResponse({'success': False, 'error_message': 'Invalid request method'}, status=405)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return JsonResponse({'success': True}, status=200)

    return JsonResponse({'success': False, 'error_message': 'Invalid request method'}, status=405)

def login(request):
    if request.method == 'POST':

        if request.user.is_authenticated:
            auth.logout(request)

        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'success': False, 'error_message': 'Invalid username or password.'}, status=200)

    return JsonResponse({'success': False, 'error_message': 'Invalid request method'}, status=405)

def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r'\d', password):
        raise ValidationError("Password must contain at least one digit.")
    if not re.search(r'[\W_]', password):
        raise ValidationError("Password must contain at least one special character.")

def validate_registration_data(username, email, password1, password2):
    if password1 != password2:
        raise ValidationError("Passwords do not match.")

    try:
        validate_email(email)
    except ValidationError as e:
        raise ValidationError(e.message)

    try:
        validate_password(password1)
    except ValidationError as e:
        raise ValidationError(e.message)

    if User.objects.filter(username=username).exists():
        raise ValidationError("Username already exists.")

    if User.objects.filter(email=email).exists():
        raise ValidationError("Email already exists.")

def register(request):
    if request.method == 'POST':

        if request.user.is_authenticated:
            auth.logout(request)
        
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')

        try:
            validate_registration_data(username, email, password1, password2)
            user = User.objects.create_user(username, email, password1)
            user.save()
            auth.login(request, user)   
            return JsonResponse({'success': True}, status=201)

        except ValidationError as e:
            return JsonResponse({'success': False, 'error_message': e.message}, status=200)

        except Exception as e:
            return JsonResponse({'success': False, 'error_message': e.message}, status=400)

    return JsonResponse({'success': False, 'error_message': 'Invalid request method'}, status=405)
 
@ensure_csrf_cookie
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrftoken': csrf_token})