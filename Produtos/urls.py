from django.urls import path
from . import views

appname= 'Produtos'

urlpatterns = [
    path('produtos/lista/', views.ProdutosListView.as_view(), name='produtoslistas'),
    path('produtos/criar/', views.ProdutosCreateView.as_view(), name='produtoscriar'),
    path('produtos/<int:pk>/detalhes/', views.ProdutosDetailView.as_view(), name='produtosdetalhe'),
    path('produtos/<int:pk>/editar/', views.ProdutosUpdateView.as_view(), name='produtoseditar'),
    path('produtos/<int:pk>/excluir/', views.ProdutosDeleteView.as_view(), name='produtosexcluir'),

]
