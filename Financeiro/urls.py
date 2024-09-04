from django.urls import path
from .views import (
    ContaAPagarListView, ContaAPagarDetailView, ContaAPagarCreateView, ContaAPagarUpdateView, ContaAPagarDeleteView,
    ContaAReceberListView, ContaAReceberDetailView, ContaAReceberCreateView, ContaAReceberUpdateView, ContaAReceberDeleteView, fluxo_caixa, dash,exportar_contaapagar_excel, exportar_contaareceber_excel
)

urlpatterns = [
    path('contas_a_pagar/', ContaAPagarListView.as_view(), name='conta_a_pagar_list'),
    path('contas_a_pagar/<int:pk>/', ContaAPagarDetailView.as_view(), name='conta_a_pagar_detail'),
    path('contas_a_pagar/criar/', ContaAPagarCreateView.as_view(), name='conta_a_pagar_create'),
    path('contas_a_pagar/<int:pk>/editar/', ContaAPagarUpdateView.as_view(), name='conta_a_pagar_update'),
    path('contas_a_pagar/<int:pk>/excluir/', ContaAPagarDeleteView.as_view(), name='conta_a_pagar_delete'),
    path('fluxo_caixa/', fluxo_caixa, name='fluxo_caixa'),
    path('fluxo_caixa/dash', dash, name='dash'),
    path('contas_a_receber/', ContaAReceberListView.as_view(), name='conta_a_receber_list'),
    path('contas_a_receber/<int:pk>/', ContaAReceberDetailView.as_view(), name='conta_a_receber_detail'),
    path('contas_a_receber/criar/', ContaAReceberCreateView.as_view(), name='conta_a_receber_create'),
    path('contas_a_receber/<int:pk>/editar/', ContaAReceberUpdateView.as_view(), name='conta_a_receber_update'),
    path('contas_a_receber/<int:pk>/excluir/', ContaAReceberDeleteView.as_view(), name='conta_a_receber_delete'),
    path('exportarapagar/', exportar_contaapagar_excel, name='exportar_contaapagar_excel'),
    path('exportarareceber/', exportar_contaareceber_excel, name='exportar_contaareceber_excel'),
]
