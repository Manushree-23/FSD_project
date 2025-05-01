from django.apps import AppConfig


class ShareBiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Share_Bite'

    def ready(self):
        import Share_Bite.signals
