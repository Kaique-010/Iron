from django.db import models
from django.contrib.auth.models import User
from Pessoas.models import Pessoas
from Financeiro.models import FormasRecebimento
from Produtos.models import Produtos
from sequences import get_next_value

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
    numero_pedido = models.CharField('Nº Pedido', max_length=20, unique=True, blank=True)
    cliente = models.ForeignKey(Pessoas, on_delete=models.PROTECT, related_name='pedidos')
    data = models.DateTimeField('Data do Pedido', blank=True, null=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='Pendente')
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0)
    vendedor = models.ForeignKey(Pessoas, on_delete=models.PROTECT, limit_choices_to={'classificacao': 'Vendedor'}, related_name='vendas', default='Sem Vendedor')
    nome_vendedor = models.CharField('Nome do Vendedor', max_length=100, blank=True)
    financeiro = models.ForeignKey(FormasRecebimento, on_delete=models.PROTECT, default='1')
    forma_recebimento = models.CharField('Forma de Recebimento', max_length=100, blank=True)
    observacoes = models.TextField('Observações', blank=True, null=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['criado', 'id']

    def __str__(self):
        return f'Pedido {self.id} - {self.cliente} - {self.status}'

    def calcular_total(self):
        return sum(item.get_total() for item in self.itens.all())

    
    def num(self, *args, **kwargs):
        if not self.numero_pedido:
         self.numero_pedido = get_next_value('numero_pedido')
         super().num(*args, **kwargs) 
    
    def save(self, *args, **kwargs):
        # Atualiza o total antes de salvar
        self.total = self.calcular_total()
        
        # Preenche os campos nome_vendedor e forma_recebimento
        if self.vendedor:
            self.nome_vendedor = self.vendedor.nome
        if self.financeiro:
            self.forma_recebimento = self.financeiro.descricao
        
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
