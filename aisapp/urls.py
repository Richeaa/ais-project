from django.urls import path
from aisapp import views

urlpatterns = [
    path('', views.signin, name ='signin'),
    path('dashboard/', views.dashboard, name ='dashboard'),
    path('logout/', views.logout, name ='logout'),
    path('form/', views.form_view, name ='form'),
    path('stock/', views.stock, name='stock'),
    path('report/', views.report_view, name='report'),
    path('production-plan/', views.production_plan, name='production_plan'),
    path('production-plan/edit/<int:id>/', views.edit_production_plan, name='edit_production_plan'),
    path('production-plan/delete/<int:id>/', views.delete_production_plan, name='delete_production_plan'),
    path('production-issue/', views.production_issue, name='production_issue'),
    path('production-issue/edit/<int:id>/', views.edit_production_issue, name='edit_production_issue'),
    path('production-issue/delete/<int:id>/', views.delete_production_issue, name='delete_production_issue'),
]