from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from Pedidos.models import ItemPedido

@receiver(pre_save, sender=ItemPedido)
def atualizar_total_item(sender, instance, **kwargs):
    """Atualiza o total do item antes de salvá-lo."""
    instance.total = instance.get_total()

@receiver(post_save, sender=ItemPedido)
def atualizar_total_pedido(sender, instance, **kwargs):
    """Atualiza total do pedido após salvar item"""
    instance.pedido.save()

@receiver(post_delete, sender=ItemPedido)
def atualizar_total_pedido_exclusao(sender, instance, **kwargs):
    """Atualiza total do pedido após excluir item"""
    instance.pedido.save()