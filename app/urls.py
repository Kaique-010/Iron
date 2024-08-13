
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('', include ('Marcas.urls')),
    path('', include ('Familias.urls')),
    path('', include ('Grupo.urls')),
    path('', include ('Localidades.urls')),
    path('', include ('Pessoas.urls')),
    path('', include ('Produtos.urls')),
    path('', include ('Entradas_Produtos.urls')),
    path('', include ('Saidas_Produtos.urls')),
    path('', include ('Financeiro.urls')),
    path('', include ('Agenda.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)