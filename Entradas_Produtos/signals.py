from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from Entradas_Produtos.models import Entrada_Produtos


@receiver(post_save, sender=Entrada_Produtos)
def update_produtos_quantidade(sender, instance, created, **kwargs):
    if created:
        if instance.quantidade > 0:
            produto = instance.produto
            produto.quantidade += instance.quantidade
            produto.save()

@receiver(post_delete, sender=Entrada_Produtos)
def update_produto_quantidade_on_delete(sender, instance, **kwargs):
    if instance.quantidade > 0:
        produto = instance.produto
        if produto: 
            produto.quantidade -= instance.quantidade
            produto.save()
