from django.urls import path
from . import views

appname= 'Localidades'

urlpatterns = [
    path('localidades/lista/', views.LocalidadesListView.as_view(), name='localidadeslistas'),
    path('localidades/criar/', views.LocalidadesCreateView.as_view(), name='localidadescriar'),
    path('localidades/<int:pk>/detalhes/', views.LocalidadesDetailView.as_view(), name='localidadesdetalhe'),
    path('localidades/<int:pk>/editar/', views.LocalidadesUpdateView.as_view(), name='localidadeseditar'),
    path('localidades/<int:pk>/excluir/', views.LocalidadesDeleteView.as_view(), name='localidadesexcluir'),

]
