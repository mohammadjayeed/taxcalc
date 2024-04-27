from django.apps import AppConfig


class CalculateTaxAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calculate_tax_app'

    def ready(self):
        import calculate_tax_app.signals