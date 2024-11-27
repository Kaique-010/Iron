# app/apps.py
from django.apps import AppConfig

class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        import app.signals  # Certifique-se de que os sinais sejam registrados
