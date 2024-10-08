from django.urls import path
from . import views

urlpatterns = [
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('change-password/', views.change_password, name='change_password'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('sentiment-analysis/', views.sentiment_analysis, name='sentiment_analysis'),
    path('summary/', views.summary, name='summary'),
    path('plate-recognition/', views.plate_recognition, name='plate_recognition'),
]
