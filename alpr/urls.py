from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.openai_plate_recognition, name='openai_plate_recognition'),
]
