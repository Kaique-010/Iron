from django.urls import path
from . import views

appname= 'Eventos'

urlpatterns = [
    path('agenda/listar', views.AgendaListView.as_view(), name='listar_eventos'),
    path('agenda/criar/', views.AgendaCreateView.as_view(), name='criar_evento'),
    path('agenda/<int:pk>/detalhes/', views.AgendaDetailView.as_view(), name='detalhe_evento'),
    path('agenda/<int:pk>/editar/', views.AgendaUpdateView.as_view(), name='editar_evento'),
    path('agenda/<int:pk>/excluir/', views.AgendaDeleteView.as_view(), name='excluir_evento'),

]
