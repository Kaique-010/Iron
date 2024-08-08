from django.contrib import admin
from .models import Pessoas

class PessoasAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'nome', 'email', 'cpf', 'rg', 'cnpj', 'ie', 'telefone', 'imagem_tag', 'obs'
    )
    list_filter = ('nome', 'classificacao',)  
    readonly_fields = ('imagem_tag',)  

    def imagem_tag(self, obj):
        return obj.imagem_tag()  

    imagem_tag.short_description = 'Foto'

admin.site.register(Pessoas, PessoasAdmin)
