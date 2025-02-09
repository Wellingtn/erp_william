from django.apps import AppConfig

class VendasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vendas'

    def ready(self):
        # Remove the import of signals for now
        pass

