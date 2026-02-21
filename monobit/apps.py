from django.apps import AppConfig


class MonobitConfig(AppConfig):
    name = "monobit"

    def ready(self):
        import monobit.signals
        from monobit.config_loader import ConfigProxy
        from django.conf import settings

        settings.config = ConfigProxy()
