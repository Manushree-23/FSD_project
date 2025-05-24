from django.apps import AppConfig


class DonationAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'donation_app'

    def ready(self):
        import donation_app.signals