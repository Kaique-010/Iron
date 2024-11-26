from django.urls import path
from .views import (
    AtualizarValorPagoView, ContaAPagarListView, ContaAPagarDetailView, ContaAPagarCreateView, ContaAPagarUpdateView, ContaAPagarDeleteView,
    ContaAReceberListView, ContaAReceberDetailView, ContaAReceberCreateView, ContaAReceberUpdateView, ContaAReceberDeleteView, EditarParcelaView, ExcluirParcelaView, ParcelasListView, fluxo_caixa, dash,exportar_contaapagar_excel, exportar_contaareceber_excel, GerarParcelasView, ParcelasListView
)
from Financeiro.views import (
    FormaPagamentoListView, FormaPagamentoCreateView, FormaPagamentoUpdateView, FormaPagamentoDeleteView,
    FormaRecebimentoListView, FormaRecebimentoCreateView, FormaRecebimentoUpdateView, FormaRecebimentoDeleteView,
    CategoriaListView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView,
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


    path('formas-pagamento/', FormaPagamentoListView.as_view(), name='formas_pagamento_list'),
    path('formas-pagamento/novo/', FormaPagamentoCreateView.as_view(), name='formas_pagamento_create'),
    path('formas-pagamento/editar/<int:pk>/', FormaPagamentoUpdateView.as_view(), name='formas_pagamento_update'),
    path('formas-pagamento/excluir/<int:pk>/', FormaPagamentoDeleteView.as_view(), name='formas_pagamento_confirm_delete'),

    # URLs para Formas de Recebimento
    path('formas-recebimento/', FormaRecebimentoListView.as_view(), name='formas_recebimento_list'),
    path('formas-recebimento/novo/', FormaRecebimentoCreateView.as_view(), name='formas_recebimento_create'),
    path('formas-recebimento/editar/<int:pk>/', FormaRecebimentoUpdateView.as_view(), name='formas_recebimento_update'),
    path('formas-recebimento/excluir/<int:pk>/', FormaRecebimentoDeleteView.as_view(), name='formas_recebimento_confirm_delete'),

    # URLs para Categorias
    path('categorias/', CategoriaListView.as_view(), name='categorias_list'),
    path('categorias/novo/', CategoriaCreateView.as_view(), name='categorias_create'),
    path('categorias/editar/<int:pk>/', CategoriaUpdateView.as_view(), name='categorias_update'),
    path('categorias/excluir/<int:pk>/', CategoriaDeleteView.as_view(), name='categorias_confirm_delete'),
    
    path("gerar-parcelas/", GerarParcelasView.as_view(), name="gerar_parcelas"),
    path("parcelas/", ParcelasListView.as_view(), name="parcelas_geradas"),
    path("atualizar-valor-pago/", AtualizarValorPagoView.as_view(), name="atualizar_valor_pago"),
    path('excluir/<int:pk>/', ExcluirParcelaView.as_view(), name='excluir_parcela'),
     path('editar/<int:pk>/', EditarParcelaView.as_view(), name='editar_parcela'),
]