
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from Produtos.models import Produtos

@receiver(post_save, sender=Produtos)
def enviar_alerta_estoque_baixo(sender, instance, created, **kwargs):
    if instance.quantidade <= instance.estoque_minimo:
        subject = f'Alerta de Estoque Baixo: {instance.nome}'
        message = f'O estoque do produto {instance.nome} está abaixo do mínimo estabelecido. Quantidade atual: {instance.quantidade}.'
        recipient_list = ['responsavel@empresa.com']
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
