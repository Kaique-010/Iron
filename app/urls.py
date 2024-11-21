from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views
#from .views import register_user

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('', include('Marcas.urls')),
    path('', include('Familias.urls')),
    path('', include('Grupo.urls')),
    path('', include('Localidades.urls')),
    path('', include('Pessoas.urls')),
    path('', include('Pedidos.urls')),
    path('', include('Produtos.urls')),
    path('', include('Entradas_Produtos.urls')),
    path('', include('Saidas_Produtos.urls')),
    path('', include('Financeiro.urls')),
    path('', include('Agenda.urls')),
    path('', include('Ordem_de_Servico.urls')),
    path('ordem/', include('OrdemProducao.urls')),
    path('', include('CFOP.urls')),
    path('', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    #path('empresa-inativa/', views.empresa_inativa, name='empresa_inativa'),
    #path('register_user/', register_user, name='register_user')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:  # Certifique-se de que está em modo DEBUG
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),  # Adicione esta linha
    ] + urlpatterns
