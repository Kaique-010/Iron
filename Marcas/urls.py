from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

appname= 'Marcas'

urlpatterns = [
    path('marcas/lista/', views.MarcasListView.as_view(), name='marcaslistas'),
    path('marcas/criar/', views.MarcasCreateView.as_view(), name='marcascriar'),
    path('marcas/<int:pk>/detalhes/', views.MarcasDetailView.as_view(), name='marcasdetalhe'),
    path('marcas/<int:pk>/editar/', views.MarcasUpdateView.as_view(), name='marcaseditar'),
    path('marcas/<int:pk>/excluir/', views.MarcasDeleteView.as_view(), name='marcasexcluir'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
