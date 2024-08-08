from django.contrib import admin
from .models import Entrada_Produtos

class Entrada_ProdutosAdmin(admin.ModelAdmin):
    list_display = ('produto', 'pessoa', 'quantidade', 'criado', 'modificado', 'id', 'documento')
    list_filter = ('criado', 'modificado', 'produto', 'quantidade')

admin.site.register(Entrada_Produtos, Entrada_ProdutosAdmin)