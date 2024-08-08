from django.contrib import admin
from .models import Localidade

class LocalidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

admin.site.register(Localidade, LocalidadeAdmin)
