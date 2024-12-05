from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),

    path('create_appointment/', views.create_appointment, name='create_appointment'),  # Для создания записи
    path('view_appointments/', views.view_appointments, name='view_appointments'),  # Для просмотра записей
    path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),# Для удаления записи

    path('create_spa_service/', views.create_spa_service, name='add_spa_service'),
    path('view-services/', views.view_spa_services, name='view_spa_services'),  # Маршрут для просмотра услуг
    path('delete_spa_service/<int:spa_service_id>/', views.delete_spa_service, name='delete_spa_service'),# Для удаления записи

    path('news/', views.view_news, name='news'),  # Маршрут для страницы новостей
    path('create-news/', views.create_news, name='create_news'),
    path('delete-news/<int:news_id>/', views.delete_news, name='delete_news'),
]

#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)