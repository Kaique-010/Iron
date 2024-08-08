from django.urls import path
from . import views

appname= 'Familias'

urlpatterns = [
    path('familias/listas/', views.FamiliasListView.as_view(), name='familiaslistas'),
    path('familias/criar/', views.FamiliaCreateView.as_view(), name='familiascriar'),
    path('familias/<int:pk>/detalhes/', views.FamiliaDetailView.as_view(), name='familiasdetalhe'),
    path('familias/<int:pk>/editar/', views.FamiliaUpdateView.as_view(), name='familiaseditar'),
    path('familias/<int:pk>/excluir/', views.FamiliaDeleteView.as_view(), name='familiasexcluir'),

]
