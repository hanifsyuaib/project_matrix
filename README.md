# ChatMatrix Backend

This is the backend for the ChatMatrix application, built with Django. The backend communicates with the frontend Vue.js to provide chat functionalities, including sentiment analysis and text summarization

## Guide to use on Windows

### 1. Download Python

### 2. Prepare and activate enviroment for packages to be stored
```
python -m venv env
env\Scripts\activate.bat
```
### 3. Install requirement
```
pip install -r requirements.txt
``` 
### 4. Make migrations and migrate for setup database
```
python manage.py makemigrations
python manage.py migrate
```
### 5. Create a file ".env" in root directory and put fill this out inside:
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

# HTTPS frontend URL in Production
HTTPS_FRONTEND = '<your_https_frontend>'

# Domain in Production (WITHOUT HTTPS)
FRONTEND_DOMAIN = '<your_frontend_domain>'
BACKEND_DOMAIN = '<your_backend_domain>'
```	

### 6. Run server with port, for example:
```
python manage.py runserver
```
or
```
python manage.py runserver 8000
```

### 7. Create Admin user for accessing the Django admin interface in this route '/admin/'
```
python manage.py createsuperuser
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.