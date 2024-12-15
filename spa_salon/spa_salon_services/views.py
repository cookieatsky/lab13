from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, SpaServiceForm, NewsForm
from .forms import AppointmentForm
from .models import Profile, SpaService, News

from .serializers import NewsSerializer
from rest_framework import viewsets

from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment, Profile

from django.contrib.auth.decorators import login_required, user_passes_test

#для статистики
from django.views.generic import TemplateView
from django.db.models import Count
from datetime import datetime, timedelta
import json



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


def is_admin(user):
    return hasattr(user, 'profile') and user.profile.role == 'admin'

@login_required
@user_passes_test(is_admin)  # Ограничение доступа только для администраторов
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.price = form.cleaned_data['service'].price  # Устанавливаем цену из выбранной услуги
            appointment.save()
            return redirect('view_appointments')  # Перенаправляем на страницу просмотра всех записей
    else:
        form = AppointmentForm()

    return render(request, 'services/create_appointment.html', {'form': form})
@login_required
def view_appointments(request):
    if request.user.is_authenticated and request.user.profile.role == 'admin':
        # Если пользователь администратор, показываем все записи
        appointments = Appointment.objects.all()
    else:
        # Если пользователь не администратор, показываем только его записи
        appointments = Appointment.objects.filter(client=request.user)

    return render(request, 'services/view_appointments.html', {'appointments': appointments})
@user_passes_test(is_admin)
@login_required
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return redirect('view_appointments')

@login_required
@user_passes_test(is_admin)
def create_spa_service(request):
    if request.method == 'POST':
        form = SpaServiceForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем новую услугу
            return redirect('view_spa_services')  # Перенаправляем на страницу просмотра услуг
    else:
        form = SpaServiceForm()

    return render(request, 'services/create_spa_service.html', {'form': form})

@user_passes_test(is_admin)
@login_required
def delete_spa_service(request, spa_service_id):
    spa_service = get_object_or_404(SpaService, id=spa_service_id)  # Получение услуги по ID
    spa_service.delete()  # Удаляем услугу
    return redirect('view_spa_services')  # Перенаправляем на страницу просмотра услуг

@login_required
def view_spa_services(request):
    services = SpaService.objects.all()  # Получаем список всех услуг
    return render(request, 'services/view_spa_services.html', {'services': services})

@login_required
def view_news(request):
    news_items = News.objects.all().order_by('-created_at')  # Получаем все новости и сортируем по дате
    return render(request, 'services/view_news.html', {'news_items': news_items})

@login_required
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)  # Не забудьте указать request.FILES
        if form.is_valid():
            form.save()
            return redirect('news')  # Перенаправляем на страницу новостей
    else:
        form = NewsForm()
    return render(request, 'services/create_news.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.profile.role == 'admin')  # Проверяем, что пользователь - администратор
def delete_news(request, news_id):
    news_item = get_object_or_404(News, id=news_id)  # Получаем объект новости или 404, если не найден
    news_item.delete()  # Удаляем новость
    return redirect('news')  # Перенаправляем обратно на страницу новостей




class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()  # Предоставляем все новости
    serializer_class = NewsSerializer  # Указываем сериализатор

#для статистики
class StatisticsView(TemplateView):
    template_name = 'services/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)

            daily_appointments = (
                Appointment.objects.filter(appointment_date__range=[start_date, end_date])
                .values('appointment_date')
                .annotate(count=Count('id'))
                .order_by('appointment_date')
            )

            context['daily_appointments'] = json.dumps(list(daily_appointments), default=str)

            services_statistics = (
                Appointment.objects.select_related('service')
                .values('service__name')
                .annotate(count=Count('id'))
                .order_by('-count')
            )

            context['services_statistics'] = json.dumps(list(services_statistics), default=str)

        except Exception as e:
            print(f"Error: {e}")  # Выводим ошибку в консоль сервера
            context['error_message'] = str(e)  # Если есть ошибка, добавляем сообщение в контекст

        return context