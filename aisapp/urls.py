from django.urls import path
from aisapp import views

urlpatterns = [
    path('', views.dashboard, name ='dashboard'), 
    path('form/', views.form_view, name ='form'),
]