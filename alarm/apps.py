from django.apps import AppConfig


class AlarmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alarm'

    def ready(self):
        import alarm.signals    # Import the Signals module.