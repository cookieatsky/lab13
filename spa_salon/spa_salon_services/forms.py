# spa_salon_services/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Appointment, SpaService, News


class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateField(
        input_formats=['%Y-%m-%d'],  # Ожидаемый формат: YYYY-MM-DD
        widget=forms.TextInput(attrs={'type': 'date'})  # Используйте HTML5 input типа date
    )
    appointment_time = forms.TimeField(
        input_formats=['%H:%M'],  # Ожидаемый формат: HH:MM
        widget=forms.TextInput(attrs={'type': 'time'})  # Используйте HTML5 input типа time
    )

    class Meta:
        model = Appointment
        fields = [
            'client',
            'service',
            'staff_member',
            'appointment_date',
            'appointment_time',
            #'price',
        ]

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, label='Роль')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']  # Добавляем поле role

class SpaServiceForm(forms.ModelForm):
    class Meta:
        model = SpaService
        fields = ['name', 'description', 'price', 'duration', 'service_type']

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image']  # Добавляем поле для изображения