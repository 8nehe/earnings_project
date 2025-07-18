from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.create_employee, name='create_employee'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('register/', views.register, name='register'),

]