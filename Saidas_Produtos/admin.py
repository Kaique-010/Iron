from django.contrib import admin
from .models import Saida_Produtos

class Saida_ProdutosAdmin(admin.ModelAdmin):
    list_display = ('produto', 'pessoa', 'quantidade', 'criado', 'modificado', 'id', 'documento')
    list_filter = ('criado', 'modificado', 'produto', 'quantidade')

admin.site.register(Saida_Produtos, Saida_ProdutosAdmin)