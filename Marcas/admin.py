from django.contrib import admin
from .models import Marcas

class MarcasAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

admin.site.register(Marcas, MarcasAdmin)