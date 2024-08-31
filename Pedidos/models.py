from django.db import models
from django.contrib.auth.models import User
from Pessoas.models import Pessoas
from Financeiro.models import ContaAReceber
from Produtos.models import Produtos

class Base(models.Model):
    criado = models.DateField('Criado em', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True

class Pedido(Base):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Processando', 'Processando'),
        ('Enviado', 'Enviado'),
        ('Concluído', 'Concluído'),
        ('Cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Pessoas, on_delete=models.PROTECT, related_name='pedidos')
    data = models.DateTimeField('Data do Pedido', blank=True, null=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='Pendente')
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0)
    observacoes = models.TextField('Observações', blank=True, null=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['criado', 'id']

    def __str__(self):
        return f'Pedido {self.id} - {self.cliente} - {self.status}'

    def calcular_total(self):
        # Calcula o total somando os totais dos itens
        return sum(item.get_total() for item in self.itens.all())

    def save(self, *args, **kwargs):
        # Atualiza o total antes de salvar
        self.total = self.calcular_total()
        super().save(*args, **kwargs)

class ItemPedido(Base):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE, related_name='itens')
    quantidade = models.PositiveIntegerField('Quantidade')
    preco_unitario = models.DecimalField('Preço Unitário', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Item Pedido'
        verbose_name_plural = 'Itens Pedido'
        ordering = ['criado', 'id']

    def __str__(self):
        return f'{self.produto} - {self.quantidade} x {self.preco_unitario}'

    def get_total(self):
        return self.quantidade * self.preco_unitario
