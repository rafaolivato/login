# autenticacao/apps.py
from django.apps import AppConfig

class AutenticacaoConfig(AppConfig):
    name = 'autenticacao'

    def ready(self):
        import autenticacao.signals
