from django.urls import path
from . import views

appname= 'Grupos'

urlpatterns = [
    path('grupos/lista/', views.GruposListView.as_view(), name='gruposlistas'),
    path('grupos/criar/', views.GruposCreateView.as_view(), name='gruposcriar'),
    path('grupos/<int:pk>/detalhes/', views.GruposDetailView.as_view(), name='gruposdetalhe'),
    path('grupos/<int:pk>/editar/', views.GruposUpdateView.as_view(), name='gruposeditar'),
    path('grupos/<int:pk>/excluir/', views.GruposDeleteView.as_view(), name='gruposexcluir'),

]
