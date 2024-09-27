from django.db.models.signals import pre_save
from django.dispatch import receiver
from Pedidos.models import ItemPedido

@receiver(pre_save, sender=ItemPedido)
def atualizar_total(sender, instance, **kwargs):
    print(f"Atualizando total para o item {instance}")
    instance.total = instance.get_total()
