from django.apps import AppConfig


class MartilloConfig(AppConfig):
    name = 'martillo'

    def ready(self):
        import martillo.signals
