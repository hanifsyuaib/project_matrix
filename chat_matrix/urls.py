from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('onboarding/', views.onboarding, name='onboarding'),
    path('chatting/', views.chatting, name='chatting'),

    path('chatbot', views.chatbot, name='chatbot'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
]
