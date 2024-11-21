from django.urls import path
from .views import (
    EtapaCreateView,
    EtapaListView,
    OrdemProducaoListView,
    OrdemProducaoCreateView,
    OrdemProducaoDetailView,
    OrdemProducaoDeleteView,
    EtapaProducaoView,
    ResponsavelCreateView,
    ResponsavelListView,
    
)

app_name = 'OrdemProducao'

urlpatterns = [
    path('ordemlista/', OrdemProducaoListView.as_view(), name='ordem_list'),
    path('create/', OrdemProducaoCreateView.as_view(), name='create'),
    path('<int:pk>/detalhes', OrdemProducaoDetailView.as_view(), name='detail'),
    path('<int:pk>/excluir', OrdemProducaoDeleteView.as_view(), name='confirm_delete'),
    path('ordens/<int:pk>/etapas/', EtapaProducaoView.as_view(), name='etapas'),
    path('etapas/', EtapaListView.as_view(), name='etapa_list'),
    path('etapas/nova/', EtapaCreateView.as_view(), name='etapa_create'),
    path('responsaveis/', ResponsavelListView.as_view(), name='responsavel_list'),
    path('responsaveis/novo/', ResponsavelCreateView.as_view(), name='responsavel_create'),

]
