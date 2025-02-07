from django.apps import AppConfig

class VendasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vendas'

    def ready(self):
        import vendas.templatetags.venda_filters

