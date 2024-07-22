from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('chatbot/', views.chatbot, name='chatbot'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
]
