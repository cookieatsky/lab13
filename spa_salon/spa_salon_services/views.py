from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт успешно создан для {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
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