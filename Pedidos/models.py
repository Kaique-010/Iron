# models.py
import uuid
from django.db import models
from Pessoas.models import Pessoas
from Financeiro.models import FormasRecebimento
from Produtos.models import Produtos
from app import settings
from Empresas.models import Empresa


class EmpresaManager(models.Manager):
    def for_user(self, user):
        if not user.is_authenticated:
            return self.none()
        return self.filter(empresa=user.empresa)

class Base(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    criado = models.DateField('Criado em', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    
    objects = EmpresaManager()
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
    nome_cliente = models.CharField('Nome Cliente', max_length=100, blank=True)
    data = models.DateField('Data do Pedido', blank=True, null=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='Pendente')
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0)
    vendedor = models.ForeignKey(Pessoas, on_delete=models.PROTECT, limit_choices_to={'classificacao': 'Vendedor'}, related_name='vendas', null=True, blank=True)
    nome_vendedor = models.CharField('Nome do Vendedor', max_length=100, blank=True)
    financeiro = models.ForeignKey(FormasRecebimento, on_delete=models.PROTECT, null=True, blank=True)
    observacoes = models.TextField('Observações', blank=True, null=True)
    contato_realizado = models.BooleanField(default=False)
    data_contato = models.DateField(null=True, blank=True)
    notas_contato = models.TextField(blank=True, null=True)


    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['criado', 'id']
        get_latest_by = 'data'
        db_table = 'pedidos'

    def __str__(self):
        return f'Pedido {self.id} - {self.cliente} - {self.status}'

    def save(self, *args, **kwargs):
        """Atualiza os campos relacionados e salva o pedido."""
        self.atualizar_campos_relacionados()
        super().save(*args, **kwargs)  # Salva normalmente.

    def calcular_total(self):
        """Calcula o total com base nos itens associados."""
        return sum(item.total for item in self.itens.all())  

    def atualizar_campos_relacionados(self):
        """Atualiza os campos do cliente, vendedor e financeiro."""
        if self.vendedor:
            self.nome_vendedor = self.vendedor.nome
        if self.financeiro:
            self.forma_recebimento = self.financeiro.descricao
        if self.cliente:
            self.nome_cliente = self.cliente.nome

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE, related_name='itens')
    quantidade = models.PositiveIntegerField('Quantidade')
    preco_unitario = models.DecimalField('Preço Unitário', max_digits=10, decimal_places=2)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0)


    class Meta:
        verbose_name = 'Item Pedido'
        verbose_name_plural = 'Itens Pedido'
        ordering = ['id']

    def __str__(self):
        return f'{self.produto} - {self.quantidade} x {self.preco_unitario}'

    def __str__(self):
        return f'{self.produto} - {self.quantidade} x {self.preco_unitario}'

    def get_total(self):
        return self.quantidade * self.preco_unitario

   