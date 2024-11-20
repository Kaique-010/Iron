# urls.py da sua app
from django.urls import path
from . import views

appname= 'CFOP'

urlpatterns = [
    path('cfop/cadastrar/', views.CFOPCreateView.as_view(), name='cfop_cadastrar'),
    path('cfop/lista', views.CFOPListView.as_view(), name='cfop_lista'), 
    path('cfop/editar/<int:pk>/', views.CFOPUpdateView.as_view(), name='cfop_editar'),
    path('cfop/excluir/<int:pk>/', views.CFOPDeleteView.as_view(), name='cfop_excluir'),
]
