from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.main'
    def ready(self) -> None:
        from . import signals
        return super().ready()