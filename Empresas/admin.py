from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Empresa, CustomUser, Licenca
from django.db import connections

import logging

logger = logging.getLogger(__name__)

# Registro da Empresa no Admin
@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'document', 'database')
    search_fields = ('name', 'document')



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'empresa')
    list_filter = ('is_staff', 'is_active', 'empresa')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('empresa',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('empresa',)}),
    )

    def save_model(self, request, obj, form, change):
        if obj.empresa:
            empresa_db = obj.empresa.database
            using_db = empresa_db
            
            # Registra no log o banco de dados utilizado
            logger.info(f"Usuário será salvo no banco de dados: {using_db}")
            
            # Verifique se a conexão com o banco de dados existe
            if using_db in connections:
                try:
                    with connections[using_db].cursor() as cursor:
                        obj.save(using=using_db)
                except Exception as e:
                    logger.error(f"Erro ao salvar no banco {using_db}: {e}")
                    raise
            else:
                logger.error(f"Banco de dados {using_db} não encontrado nas configurações.")
                raise ValueError(f"Banco de dados {using_db} não encontrado.")
        else:
            obj.save(using='default')  # Salva no banco de dados padrão


@admin.register(Licenca)
class LicencaAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'documento', 'data_ativacao', 'ativo')
    list_filter = ('ativo', 'empresa')
    search_fields = ( 'documento', 'empresa__name')
    ordering = ('data_ativacao',)

    # Adicionando campos para o formulário de cadastro de Licença
    fieldsets = (
        (None, {
            'fields': ( 'empresa', 'documento', 'data_ativacao', 'data_expiracao', 'ativo')
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': ('nome', 'empresa', 'documento', 'data_ativacao', 'ativo')
        }),
    )