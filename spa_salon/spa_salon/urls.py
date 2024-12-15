from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),  # Админка Django
    path('', RedirectView.as_view(url='/login/', permanent=False)),  # Перенаправление с корневого URL на /login/
    path('', include('spa_salon_services.urls')),  # Импортируем URL-адреса приложения

]

