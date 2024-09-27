from django_cron import CronJobBase, Schedule
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.db import connection
import logging

logger = logging.getLogger(__name__)


class EnviarEmailsClientesInativosCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'Pedidos.enviar_email_clientes_inativos'

    def do(self):
        hoje = timezone.now().date()
        dias_para_contato = 1  
        data_limite = hoje - timedelta(days=dias_para_contato)

        query = """
            SELECT DISTINCT 
                p.cliente_id AS cliente_id,
                pe.email AS email,
                MAX(p.data) AS ultima_compra,
                p.nome_cliente AS nome_cliente
            FROM pedidos_pedido p
            JOIN pessoas_pessoas pe ON p.cliente_id = pe.id
            WHERE p.data <= %s
            GROUP BY p.cliente_id, pe.email, p.nome_cliente
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [data_limite])
            rows = cursor.fetchall()
            clientes_inativos = [
                {
                    'cliente_id': row[0],
                    'email': row[1],
                    'ultima_compra': row[2],
                    'nome_cliente': row[3],
                }
                for row in rows
            ]

        logger.info(f'Clientes inativos encontrados: {clientes_inativos}')

        for cliente in clientes_inativos:
            send_mail(
                'Estamos com saudades!',
                f'Olá {cliente["nome_cliente"]},\n\nEstamos sentindo sua falta. Venha nos visitar novamente!',
                'leokaique7@gmail.com',
                [cliente['email']],
            )
            logger.info(f'Email enviado para: {cliente["email"]}')