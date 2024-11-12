from django.urls import path
from .views import AgendaCreateView, AgendaListView, AgendaDeleteView, AgendaDetailView, AgendaUpdateView
from .views import eventos_futuros_json, eventos_json, eventos_futuros

appname= 'Eventos'

urlpatterns = [
    path('agenda/listar', AgendaListView.as_view(), name='listar_eventos'),
    path('agenda/criar/', AgendaCreateView.as_view(), name='criar_evento'),
    path('agenda/<int:pk>/detalhes/', AgendaDetailView.as_view(), name='detalhe_evento'),
    path('agenda/<int:pk>/editar/', AgendaUpdateView.as_view(), name='editar_evento'),
    path('agenda/<int:pk>/excluir/',AgendaDeleteView.as_view(), name='excluir_evento'),
    path('eventos-futuros/json/', eventos_futuros_json, name='eventos_futuros_json'),  # URL para eventos futuros em JSON
    path('eventos-futuros/', eventos_futuros, name='eventos_futuros'),  # URL para a página de eventos futuros
    path('eventos/', eventos_json, name='eventos'),
]