'''class TenantRouter:
    def db_for_read(self, model, **hints):
        # Verifica se o modelo é um CustomUser ou se o 'tenant' está no request
        tenant = hints.get('tenant')  # Passando 'tenant' no contexto da consulta

        if tenant:
            return tenant.database  # Retorna o banco de dados da empresa
        return 'default'  # Caso contrário, retorna o banco de dados default

    def db_for_write(self, model, **hints):
        tenant = hints.get('tenant')  # Passando 'tenant' no contexto da consulta

        if tenant:
            return tenant.database  # Retorna o banco de dados da empresa
        return 'default'  # Caso contrário, retorna o banco de dados default

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Permite migrações apenas no banco de dados correspondente
        return db == 'default' or db == hints.get('tenant')  # Ajuste aqui
'''