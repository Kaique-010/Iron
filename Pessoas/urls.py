from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from Pessoas.views import exportar_pessoas_excel

appname= 'Pessoas'

urlpatterns = [
    path('pessoas/lista/', views.PessoasListView.as_view(), name='pessoaslistas'),
    path('pessoas/criar/', views.PessoasCreateView.as_view(), name='pessoasscriar'),
    path('pessoas/<int:pk>/detalhes/', views.PessoasDetailView.as_view(), name='pessoasdetalhe'),
    path('pessoas/<int:pk>/editar/', views.PessoasUpdateView.as_view(), name='pessoaseditar'),
    path('pessoas/<int:pk>/excluir/', views.PessoasDeleteView.as_view(), name='pessoasexcluir'),
    path('exportarpessoas/', exportar_pessoas_excel, name='exportar_pessoas_excel'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
