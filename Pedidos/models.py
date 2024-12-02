# models.py
import uuid
from django.db import models
from django.db import transaction
from django.utils import timezone
from django.db.models import Sum, F
from django.core.exceptions import ValidationError
from Pessoas.models import Pessoas
from Financeiro.models import FormasRecebimento
from Produtos.models import Precos, Produtos
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

class PedidoManager(models.Manager):
    def pedidos_pendentes(self):
        return self.filter(status='Pendente').select_related('cliente', 'vendedor').prefetch_related('itens__produto')
    
    def pedidos_do_vendedor(self, vendedor):
        return self.filter(vendedor=vendedor).select_related('cliente').prefetch_related('itens__produto')
    
    def pedidos_por_periodo(self, data_inicial, data_final):
        return self.filter(data__range=[data_inicial, data_final])

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
    vendedor = models.ForeignKey(Pessoas, on_delete=models.PROTECT, 
                                 limit_choices_to={'classificacao': 'Vendedor'}, 
                                 related_name='vendas', 
                                 null=True, blank=True)
    nome_vendedor = models.CharField('Nome do Vendedor', max_length=100, blank=True)
    financeiro = models.ForeignKey(FormasRecebimento, on_delete=models.PROTECT, null=True, blank=True)
    observacoes = models.TextField('Observações', blank=True, null=True)
    contato_realizado = models.BooleanField(default=False)
    data_contato = models.DateField(null=True, blank=True)
    notas_contato = models.TextField(blank=True, null=True)
    numero_pedido = models.PositiveIntegerField(unique=True, editable=False)

    objects = PedidoManager()

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['criado', 'id']
        get_latest_by = 'data'
        db_table = 'pedidos'

    def __str__(self):
        return f'Pedido {self.numero_pedido} - {self.cliente} - {self.status}'

    def clean(self):
        if self.vendedor and self.vendedor.classificacao != 'Vendedor':
            raise ValidationError("O vendedor selecionado não é válido")

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Verifica se já tem um número de pedido
            if not self.numero_pedido:
                self.numero_pedido = self.gerar_numero_pedido()

            # Salva o pedido para gerar o PK
            super().save(*args, **kwargs)
            
            # Agora que o pedido tem um PK, podemos calcular o total
            self.total = self.calcular_total()
            
            # Atualiza campos relacionados
            self.atualizar_campos_relacionados()

            # Salva novamente com o total calculado
            super().save(*args, **kwargs)

    def gerar_numero_pedido(self):
        ultimo_pedido = Pedido.objects.order_by('numero_pedido').last()
        return (ultimo_pedido.numero_pedido + 1) if ultimo_pedido else 1

    def atualizar_campos_relacionados(self):
        if self.vendedor:
            self.nome_vendedor = self.vendedor.nome
        if self.cliente:
            self.nome_cliente = self.cliente.nome

    def calcular_total(self):
        return self.itens.all().aggregate(
            total=Sum(F('total'))
        )['total'] or 0

    def cancelar_pedido(self):
        with transaction.atomic():
            for item in self.itens.all():
                item.reverter_estoque()
            self.status = 'Cancelado'
            self.save()
            self.registrar_evento("Cancelado", "Pedido cancelado e estoque revertido.")

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE, related_name='itens')
    quantidade = models.PositiveIntegerField('Quantidade')
    preco_unitario = models.DecimalField('Preço Unitário', max_digits=10, decimal_places=2)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, editable=False)

    class Meta:
        verbose_name = 'Item Pedido'
        verbose_name_plural = 'Itens Pedido'
        ordering = ['id']

    def __str__(self):
        return f'{self.produto} - {self.quantidade} x {self.preco_unitario}'

    def clean(self):
        if self.pk:  
            item_antigo = ItemPedido.objects.get(pk=self.pk)
            quantidade_alterada = self.quantidade - item_antigo.quantidade
        else:  
            quantidade_alterada = self.quantidade

        # Verificação de quantidade do produto e alteração de quantidade
        if self.produto.quantidade is not None and quantidade_alterada is not None:
            if quantidade_alterada > self.produto.quantidade:
                raise ValidationError(f"Estoque insuficiente para {self.produto}")
        else:
            raise ValidationError(f"Estoque do produto {self.produto} não definido ou quantidade inválida.")

        # Verificar se a quantidade é válida
        if self.quantidade is not None and self.quantidade > 0:
            if self.quantidade > self.produto.quantidade:
                raise ValidationError(f"Estoque insuficiente para o produto {self.produto}.")
        else:
            raise ValidationError("A quantidade não pode ser menor ou igual a zero.")

        # Verificação de preço unitário
        if self.preco_unitario is not None and self.preco_unitario > 0:
            if self.preco_unitario != self.produto.precos.first().preco_venda_vista:
                raise ValidationError(f'O preço unitário deve ser {self.produto.precos.first().preco_venda_vista}')
        else:
            raise ValidationError("O preço unitário não pode ser zero ou negativo.")

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.preco()
            self.total = self.get_total()
            self.full_clean()
            super().save(*args, **kwargs)
            self.atualizar_estoque()

    def get_total(self):
        return self.quantidade * self.preco_unitario

    def atualizar_estoque(self):
        if self.pk:  
            item_antigo = ItemPedido.objects.get(pk=self.pk)
            diferenca_quantidade = self.quantidade - item_antigo.quantidade
        else:  
            diferenca_quantidade = self.quantidade

        self.produto.quantidade -= diferenca_quantidade
        self.produto.save()

    def reverter_estoque(self):
        self.produto.quantidade += self.quantidade
        self.produto.save()

    def preco(self):
        preco = Precos.objects.filter(produto=self.produto).first()
        if preco:
            self.preco_unitario = preco.preco_venda_vista



class PedidoHistorico(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='historico')
    acao = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pedido} - {self.acao} - {self.data_hora}"


def registrar_evento(self, acao, descricao=""):
    PedidoHistorico.objects.create(pedido=self, acao=acao, descricao=descricao)