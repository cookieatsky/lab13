from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm
#AppointmentForm

from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment, Profile

from django.contrib.auth.decorators import login_required, user_passes_test


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            # Проверка существования пользователя
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                messages.error(request, "Пользователь с таким именем или email уже существует.")
                return render(request, 'services/register.html', {'form': form})

            # Сохраняем пользователя
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Устанавливаем пароль
            user.save()  # Сохраняем пользователя

            if hasattr(user, 'profile'):
                print("Нихуя не вошёл в условие")
                profile = user.profile  # Получаем существующий профиль
                profile.role = form.cleaned_data['role']  # Обновляем роль
                profile.save()
                # Проверка на существование профиля
            else:
                # Создаем профиль с ролью из формы
                print("Вошёл в условие")
                Profile.objects.create(user=user, role=form.cleaned_data['role'])  # Создаем профиль

            login(request, user)  # Автоматический вход после регистрации
            return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'services/register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Укажите ваш redirect после входа
        else:
            messages.error(request, 'Неверные учетные данные.')
    return render(request, 'services/login.html')
# spa_salon_services/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'services/home.html')  # Создайте home.html в templates/services/

def logout_view(request):
    logout(request)  # Вызов функции logout для выхода пользователя
    return redirect('login')  # Перенаправляем на страницу логина или на другую страницу, например, домой


@login_required
def create_appointment(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user  # Установка текущего пользователя
            appointment.save()
            return redirect('home')  # Перенаправление после добавления
    else:
        form = UserRegistrationForm()
    return render(request, 'services/create_appointment.html', {'form': form})

@login_required
def view_appointments(request):
    appointments = Appointment.objects.filter(user=request.user)  # Записи текущего пользователя
    return render(request, 'services/view_appointments.html', {'appointments': appointments})

@user_passes_test(lambda u: u.is_superuser)
@login_required
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return redirect('view_appointments')