from django.urls import path
from . import views

urlpatterns = [
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('sentiment-analysis/', views.sentiment_analysis, name='sentiment_analysis'),
]
