from django.urls import path
from aisapp import views

urlpatterns = [
    path('', views.dashboard, name ='dashboard'), 
]