from django.contrib import admin
from .models import Evento


class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'responsavel','data_inicio', 'data_fim', 'horario', 'local', 'descricao')
    search_fields = ('titulo', 'responsavel','data_inicio', 'data_fim', 'horario', 'local', 'descricao')
    list_filter = ('titulo', 'responsavel','data_inicio',)



admin.site.register(Evento, EventoAdmin)