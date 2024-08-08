from django.contrib import admin
from .models import Familia


class FamiliaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


admin.site.register(Familia, FamiliaAdmin)
