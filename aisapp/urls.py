from django.urls import path
from aisapp import views

urlpatterns = [
    path('', views.signin, name ='signin'),
    path('dashboard/', views.dashboard, name ='dashboard'),
    path('logout/', views.logout, name ='logout'),
    path('form/', views.form_view, name ='form'),
    path('stock/', views.stock, name='stock'),
    path('report/', views.report_view, name='report'),
]