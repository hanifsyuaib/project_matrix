from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import openai
import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    )

@csrf_exempt
def openai_plate_recognition(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    image_source = data.get("image_source") # URL or Base 64 encoded image
    if not image_source:
        return JsonResponse({'error': 'Image source is required'}, status=400)

    try:
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

        number_plate, expired_time = extract_number_plate_and_expired_time(answer)

        result = {
                "image_source": image_source,
                "answer": answer,
                "number_plate": number_plate,
                "expired_time": expired_time, 
                "message_tokens": message_tokens, 
                "response_tokens": response_tokens, 
                "total_tokens": total_tokens
        }

        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)

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
