from django.db import models
from django.contrib.auth.models import User

class SpaService(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    service_name = models.CharField(max_length=255)
    appointment_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.service_name} - {self.appointment_date}"


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