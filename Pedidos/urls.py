from django.urls import path
from . import views
from .views import pedido_itens,exportar_pedidos_excel

appname= 'pedidos'

urlpatterns = [
    path('pedidos/lista/', views.PedidosListView.as_view(), name='pedidoslistas'),
    path('pedidos/criar/', views.PedidosCreateView.as_view(), name='pedidoscriar'),
    path('pedidos/<int:pk>/detalhes/', views.PedidosDetailView.as_view(), name='pedidosdetalhe'),
    path('pedidos/<int:pk>/editar/', views.PedidosUpdateView.as_view(), name='pedidoseditar'),
    path('pedidos/<int:pk>/excluir/', views.PedidosDeleteView.as_view(), name='pedidosexcluir'),
    path('pedidos/<int:pedido_id>/itens/', pedido_itens, name='pedido_itens'),
    path('exportar/', exportar_pedidos_excel, name='exportar_pedidos_excel'),

]
