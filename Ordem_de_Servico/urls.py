from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import exportar_os_excel

appname= 'Os'

urlpatterns = [
    path('Os/lista/', views.OsListView.as_view(), name='Oslistas'),
    path('Os/criar/', views.OsCreateView.as_view(), name='Oscriar'),
    path('Os/<int:pk>/detalhes/', views.OsDetailView.as_view(), name='Osdetalhe'),
    path('Os/<int:pk>/editar/', views.OsUpdateView.as_view(), name='Oseditar'),
    path('Os/<int:pk>/excluir/', views.OsDeleteView.as_view(), name='Osexcluir'),
    path('exportaros/', exportar_os_excel, name='exportar_os_excel'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
