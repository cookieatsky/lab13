from django.apps import AppConfig


class ServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spa_salon_services'

    def ready(self):
        import spa_salon_services.signals  # Подключаем сигналы