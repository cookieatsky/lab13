from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
from datetime import time

class SpaService(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Значение по умолчанию для цены
    duration = models.IntegerField(default=30)  # Значение по умолчанию для продолжительности в минутах
    service_type = models.CharField(max_length=100, default='Общий');  # Значение по умолчанию для типа услуги

    def __str__(self):
        return self.name


class Appointment(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': False})
    service = models.ForeignKey(SpaService, on_delete=models.CASCADE)
    staff_member = models.CharField(max_length=100, default='Неизвестный мастер')  # Значение по умолчанию для имени мастера
    appointment_date = models.DateField(null=True, default=None)  # Путь к исправлению проблемы с датой
    appointment_time = models.TimeField(null=True, default=None)  # Установка времени по умолчанию на 00:00
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Значение по умолчанию для цены

    def __str__(self):
        return f"{self.client.username} - {self.service.name} on {self.appointment_date} at {self.appointment_time}"


# Новая модель профиля для расширения модели пользователя
class Profile(models.Model):
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, blank=False, null=False)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания записи
    image = models.ImageField(upload_to='news_images/')  # Поле для загрузки изображения
    def __str__(self):
        return self.title