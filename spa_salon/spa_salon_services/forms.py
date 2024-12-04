# spa_salon_services/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    #role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, label='Роль')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']  # Добавляем поле role