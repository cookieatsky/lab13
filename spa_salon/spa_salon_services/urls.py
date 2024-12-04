from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('create_appointment/', views.create_appointment, name='create_appointment'),  # Для создания записи
    path('view_appointments/', views.view_appointments, name='view_appointments'),  # Для просмотра записей
    path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),# Для удаления записи
    path('create_spa_service/', views.create_spa_service, name='add_spa_service'),
]