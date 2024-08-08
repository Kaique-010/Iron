from django.db import models
from django.contrib.auth.models import User
from Pessoas.models import Pessoas



class Base(models.Model):
    criado = models.DateField('Criado em', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True


class FormasRecebimento(Base):
    descricao = models.CharField('Descrição', max_length=100)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Forma de Recebimento'
        verbose_name_plural = 'Formas de Recebimento'
        ordering = ['criado', 'id']


class FormasPagamento(Base):
    descricao = models.CharField('Descrição', max_length=100)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Forma de Pagamento'
        verbose_name_plural = 'Formas de Pagamento'
        ordering = ['criado', 'id']

class Categorias(Base):
    descricao = models.CharField('Descrição', max_length=100)
       
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['criado', 'id']
    
    def __str__(self):
        return self.descricao


class ContaAPagar(Base):
    documento = models.CharField('Documento',max_length=20)
    descricao = models.CharField('Descrição',max_length=255)
    parcela = models.IntegerField('Parcelas')
    valor = models.DecimalField('Valor',max_digits=10, decimal_places=2)
    data_emissao = models.DateField('Data de Emissão')
    data_vencimento = models.DateField('Vencimento')
    data_pagamento = models.DateField('Data de Pagamento', null=True, blank=True)
    status_pagamento = models.BooleanField('Status de Pagamento',default=False)
    pessoas = models.ForeignKey(Pessoas, on_delete=models.PROTECT, related_name='contas_a_pagar')
    categorias = models.ForeignKey(Categorias, on_delete= models.PROTECT, max_length=100)
    observacoes = models.TextField('Observações',null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='contas_a_pagar')
    forma_pagamento = models.ForeignKey(FormasPagamento, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Conta a Pagar'
        verbose_name_plural = 'Contas a Pagar'
        ordering = ['criado', 'id']
    
    def __str__(self):
        return self.descricao
    
    


class ContaAReceber(Base):
    documento = models.CharField('Documento',max_length=20)
    descricao = models.CharField('Descrição',max_length=255)
    parcela = models.IntegerField('Parcelas')
    valor = models.DecimalField('Valor',max_digits=10, decimal_places=2)
    data_emissao = models.DateField('Data de Emissão')
    data_vencimento = models.DateField('Vencimento')
    data_recebimento = models.DateField('Data de Recebimento', null=True, blank=True)
    status_recebimento = models.BooleanField(default=False)
    pessoas = models.ForeignKey(Pessoas, on_delete=models.CASCADE, related_name='contas_a_receber')
    categorias = models.ForeignKey(Categorias, on_delete= models.PROTECT, max_length=100)
    observacoes = models.TextField('Observações',null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contas_a_receber')
    forma_recebimento = models.ForeignKey(FormasRecebimento, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Conta a Receber'
        verbose_name_plural = 'Contas a Receber'
        ordering = ['criado', 'id']
    
    def __str__(self):
        return self.descricao
    

