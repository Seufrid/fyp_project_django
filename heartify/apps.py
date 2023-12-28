from django.apps import AppConfig


class HeartifyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'heartify'

    def ready(self):
        # it's important to import the signals inside ready method to avoid issues with app registry
        from . import signals  # Replace with the path to your signals.py
