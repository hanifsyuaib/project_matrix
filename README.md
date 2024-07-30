# ChatMatrix Backend

## Description

This is the backend for the ChatMatrix application, built with Django. The backend communicates with the frontend Vue.js to provide chat functionalities, including sentiment analysis, text summarization, and number plate recognition.

## Table of Contents

1. [Description](#description)
2. [Table of Contents](#table-of-contents)
3. [Sonarcloud Badges](#sonarcloud-badges)
4. [Features](#features)
5. [Installation](#installation)
6. [License](#license)

## Sonarcloud Badges
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=hanifsyuaib_project_matrix&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=hanifsyuaib_project_matrix)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=hanifsyuaib_project_matrix&metric=coverage)](https://sonarcloud.io/summary/new_code?id=hanifsyuaib_project_matrix)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=hanifsyuaib_project_matrix&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=hanifsyuaib_project_matrix)

## Features 
1. Automatic License Plate Recognition (ALPR) API

2. ChatMatrix
	- Sentiment Analysis
	- Summarize Text
	- Number Plate Recognition

## Installation

1. Download Python

2. Prepare and activate enviroment for packages to be stored
```
python -m venv env
env\Scripts\activate.bat
```

3. Install requirement
```
pip install -r requirements.txt
``` 

4. Create a file ".env" in root directory and put fill this out inside:
```
# OPENAI API
OPENAI_API_KEY = '<your_openai_api_key>'

# Database Postgresql
DB_NAME = '<your_db_name>'
DB_USER = '<your_db_user>'
DB_PASSWORD = '<your_db_password>'
DB_HOST = '<your_db_host>'
DB_PORT = '<your_db_port>'

# Secret key for django in settings.py
SECRET_KEY = '<your_secret_key>'

# HTTPS/HTTP frontend URL in Production
HTTPS_FRONTEND = '<your_https_frontend>'

# Domain in Production (WITHOUT HTTPS/HTTP)
FRONTEND_DOMAIN = '<your_frontend_domain>'
BACKEND_DOMAIN = '<your_backend_domain>'
```	

5. Make migrations and migrate for setup database
```
python manage.py makemigrations
python manage.py migrate
```

6. Run server with host and port, for example:
```
python manage.py runserver
```
or
```
python manage.py runserver 0.0.0.0:8000
```

7. Additional: Create Admin user for accessing the Django admin interface in this route '/admin/'
```
python manage.py createsuperuser
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.