from django.contrib import admin
from .models import Produtos, Precos

class ProdutosAdmin(admin.ModelAdmin):
    list_display = ('id','ativo','nome', 'grupo', 'familia', 'imagem_tag')
    list_filter = ('grupo', 'familia', 'ativo')
    search_fields = ('nome', 'descricao')
    readonly_fields = ('imagem_tag',)
    fieldsets = (
        (None, {
            'fields': ('ativo','nome', 'grupo', 'familia','marca', 'localidade', 'imagem', 'descricao',)
        }),
        ('Opções Avançadas', {
            'classes': ('collapse',),
            'fields': ('tamanho', 'peso',),
        }),
    )

admin.site.register(Produtos, ProdutosAdmin)

@admin.register(Precos)
class PrecosAdmin(admin.ModelAdmin):
    list_display = ['produto', 'preco_compra', 'preco_venda_vista', 'preco_venda_prazo', 'percentual_venda_vista', 'percentual_venda_prazo']
    search_fields = ['produto__nome']
