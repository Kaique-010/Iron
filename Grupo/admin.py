from django.contrib import admin
from .models import Grupo

class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

admin.site.register(Grupo, GrupoAdmin)