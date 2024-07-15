# chat_matrix

## Guide to use chat_matrix on Windows

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
### 5. Create a file ".env" in root directory and put "OPENAI_API_KEY = <your_api_key>" inside

### 6. Run server with port, for example:
```
python manage.py runserver 8000
```
