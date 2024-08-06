from django.urls import path
from . import views

urlpatterns = [
    path('helmet/', views.openai_tvd_helmet, name='openai_tvd_helmet'),
    path('seatbelt/', views.openai_tvd_seatbelt, name='openai_tvd_seatbelt'),
    path('mobile-phone/', views.openai_tvd_mobile_phone, name='openai_tvd_mobile_phone'),
]
