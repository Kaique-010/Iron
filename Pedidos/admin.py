from django.contrib import admin
from .models import Pedido

class PedidosAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente','data', 'status', 'total')
    search_fields = ('id',)
    list_filter = ['id', 'cliente', 'status']

admin.site.register(Pedido, PedidosAdmin)
