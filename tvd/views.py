from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

import json
import openai
import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    )

def extract_two_variable_value_from_string(formatted_string, first_variable_name, second_variable_name):
    # Split the string into lines
    lines = formatted_string.split('\n')

    # Extract first variable from the first line
    first_variable_line = lines[0].strip()
    first_variable = first_variable_line.replace(first_variable_name, '').replace('.', '').strip()
    
    # Collect all lines after the first one for the reason
    second_variable_lines = lines[1:]
    second_variable = '\n'.join(line.strip() for line in second_variable_lines).replace(second_variable_name, '').replace('.', '').strip()

    return first_variable, second_variable


def validate_image_source_request(request):
    if request.method != 'POST':
        raise ValidationError('Invalid request method')

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        raise ValidationError('Invalid JSON data')

    image_source = data.get("image_source")  # URL or Base 64 encoded image
    if not image_source:
        raise ValidationError('Image source is required')

    return image_source

@csrf_exempt
def openai_tvd_helmet(request):
    try:
        image_source = validate_image_source_request(request)
        first_variable_name = 'Total Occupants On Motorcycle:'
        second_variable_name = 'All Occupants Are Wearing Helmets:'

        prompt_to_openai = f'''
                                Based on the image, please focus on the area inside the green square.
                                Identify the number occupants on the motorcycle and check if all occupants are wearing helmets.  
                                Return your response in the following strict string format: 
                                {first_variable_name} <integer>. \n{second_variable_name} <boolean>.
                            '''
        response = client.chat.completions.create(
          model="gpt-4o-mini",
          messages=[
            {
              "role": "user",
              "content": [
                {  
                  "type": "text", 
                  "text": prompt_to_openai
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": image_source,
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

        total_occupants, are_occupants_wearing_helmets = extract_two_variable_value_from_string(answer, first_variable_name, second_variable_name)

        result = {
                "image_source": image_source,
                "answer": answer,
                "total_occupants": total_occupants,
                "are_occupants_wearing_helmets": are_occupants_wearing_helmets,
                "message_tokens": message_tokens, 
                "response_tokens": response_tokens, 
                "total_tokens": total_tokens
        }

        return JsonResponse(result)

    except ValidationError as e:
        return JsonResponse({'error': 'Validation error occurred: ' + e.message}, status=400)

    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)

@csrf_exempt
def openai_tvd_seatbelt(request):
    try:
        image_source = validate_image_source_request(request)
        first_variable_name = 'Total Occupants Inside The Vehicle:'
        second_variable_name = 'All Occupants Are Wearing Seatbelt:'

        prompt_to_openai = f'''
                                Based on the image, please focus on the area inside the yellow square.
                                Identify the number occupants inside the vehicle and check if all occupants are wearing seatbelt.  
                                Return your response in the following strict string format: 
                                {first_variable_name} <integer>. \n{second_variable_name} <boolean>.
                            '''
        response = client.chat.completions.create(
          model="gpt-4o-mini",
          messages=[
            {
              "role": "user",
              "content": [
                {  
                  "type": "text", 
                  "text": prompt_to_openai
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": image_source,
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

        total_occupants, are_occupants_wearing_seatbelt = extract_two_variable_value_from_string(answer, first_variable_name, second_variable_name)

        result = {
                "image_source": image_source,
                "answer": answer,
                "total_occupants": total_occupants,
                "are_occupants_wearing_seatbelt": are_occupants_wearing_seatbelt,
                "message_tokens": message_tokens, 
                "response_tokens": response_tokens, 
                "total_tokens": total_tokens
        }

        return JsonResponse(result)

    except ValidationError as e:
        return JsonResponse({'error': 'Validation error occurred: ' + e.message}, status=400)

    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)

@csrf_exempt
def openai_tvd_mobile_phone(request):
    try:
        image_source = validate_image_source_request(request)

        prompt_to_openai = f'''
                                Based on the image, please focus on the area inside the yellow square.
                                Check if the driver inside the vehicle is using mobile phone.  
                                Return your response in the following strict string format: boolean
                           '''
        response = client.chat.completions.create(
          model="gpt-4o-mini",
          messages=[
            {
              "role": "user",
              "content": [
                {  
                  "type": "text", 
                  "text": prompt_to_openai
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": image_source,
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

        result = {
                "image_source": image_source,
                "answer": answer,
                "driver_using_mobile_phone": answer,
                "message_tokens": message_tokens, 
                "response_tokens": response_tokens, 
                "total_tokens": total_tokens
        }

        return JsonResponse(result)

    except ValidationError as e:
        return JsonResponse({'error': 'Validation error occurred: ' + e.message}, status=400)

    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)


@csrf_exempt
def openai_tvd_car(request):
    try:
        image_source = validate_image_source_request(request)

        prompt_to_openai = f'''
                                Based on the image, please focus on the area inside the yellow square.
                                The Question down below:
                                1. Count human inside the car.
                                2. Check if all human inside the car are wearing seatbelt.
                                3. Check if the driver inside the car is using mobile phone.  
                                Return your response in the following strict string format down below: 
                                Total Human = integer
                                Are All Human Wearing Seatbelt = boolean.
                                Is Driver Using Mobile Phone = boolean.
                           '''
        response = client.chat.completions.create(
          model="gpt-4o-mini",
          messages=[
            {
              "role": "user",
              "content": [
                {  
                  "type": "text", 
                  "text": prompt_to_openai
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": image_source,
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

        result = {
                "image_source": image_source,
                "answer": answer,
                "message_tokens": message_tokens, 
                "response_tokens": response_tokens, 
                "total_tokens": total_tokens
        }

        return JsonResponse(result)

    except ValidationError as e:
        return JsonResponse({'error': 'Validation error occurred: ' + e.message}, status=400)

    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)