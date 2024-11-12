from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from Pedidos.models import ItemPedido

@receiver(pre_save, sender=ItemPedido)
def atualizar_total_item(sender, instance, **kwargs):
    """Atualiza o total do item antes de salvá-lo."""
    instance.total = instance.get_total()

@receiver([post_save, post_delete], sender=ItemPedido)
def atualizar_total_pedido(sender, instance, **kwargs):
    """Recalcula e atualiza o total do pedido sempre que um item é salvo ou excluído."""
    pedido = instance.pedido

    # Verifica se o pedido existe para evitar erros.
    if pedido:
        pedido.total = pedido.calcular_total()
        # Usa `update_fields` para evitar loop infinito.
        pedido.save(update_fields=['total'])
