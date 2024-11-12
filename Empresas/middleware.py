from django.db import connections
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout
from Agenda.views import set_empresa_database
import logging

logger = logging.getLogger(__name__)


class SetDatabaseMiddleware(MiddlewareMixin):
    def process_request(self, request):
        empresa_database = request.session.get('empresa_database', None)
        logger.debug(f'Configuração do banco de dados: {empresa_database}')
        
        if empresa_database:
            try:
                connections[empresa_database]  # Valida a existência da conexão
                connections.databases['default'] = connections[empresa_database].settings_dict
            except KeyError:
                logger.error(f'Banco de dados não encontrado para: {empresa_database}')
                connections.databases['default'] = connections['default'].settings_dict

    def process_response(self, request, response):
        # Se o usuário fizer logout, limpar a conexão do banco de dados
        if request.user.is_authenticated and request.path == '/logout/':
            del connections.databases['default']
        return response


class EmpresaMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'empresa') and request.user.empresa:
            
            set_empresa_database(request.user.empresa)
        else:
            
            pass