'''from django.apps import AppConfig


class OrdemproducaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'OrdemProducao'

    def ready(self):
        import OrdemProducao.signals  
'''