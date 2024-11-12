import uuid
from django import forms
from django.db import models
from Pessoas.models import Pessoas
from Produtos.models import Produtos
from sequences import get_next_value
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

class OrdemServico(Base):
    numero_os = models.CharField('Nº O.S', max_length=20, unique=True, blank=True)
    cliente = models.ForeignKey(Pessoas, on_delete=models.CASCADE, related_name='ordens_servico')
    data_abertura = models.DateField() 
    data_fechamento = models.DateField(blank=True, null=True)  


    class Meta:
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
        ordering = ['criado', 'numero_os']
        db_table = 'os'
    
    def calcular_total(self):
        total = sum(item.valor for item in self.itens.all())
        return total
    
    def save(self, *args, **kwargs):
        if not self.numero_os:
            self.numero_os = get_next_value('ordem_servico_numero')
        super().save(*args, **kwargs)
    

    def __str__(self):
        return f"OS {self.id} - {self.numero_os} - {self.cliente}"

class ItensOs(Base):
    numero_os = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='itens')
    item_numero = models.IntegerField()
    peca = models.ForeignKey(Produtos, on_delete=models.CASCADE, related_name='peca')
    servico = models.ForeignKey(Produtos, on_delete=models.CASCADE, related_name='servico', blank=True, null=True)
    peca_quantidade = models.FloatField()
    peca_unitario = models.FloatField()
    peca_desconto = models.FloatField()
    peca_total = models.FloatField()

    class Meta:
        verbose_name = 'Peça'
        verbose_name_plural = 'Peças'
        unique_together = ('numero_os', 'item_numero')
        ordering = ['criado', 'numero_os']
        db_table = 'itensos'

    def __str__(self):
        return f"ItensOs {self.id} - {self.item_numero} - {self.peca} - {self.servico}"
    
    def clean_peca_desconto(self):
        peca_desconto = self.cleaned_data.get('peca_desconto')
        if peca_desconto is not None and peca_desconto < 0:
            raise forms.ValidationError("O desconto da peça não pode ser negativo.")
        return peca_desconto

    def calcular_total(self):
        total = sum(item.valor for item in self.itens.all())
        return total
    
    def save(self, *args, **kwargs):
        if not self.numero_os:
            self.numero_os = get_next_value('ordem_servico_numero')
        super().save(*args, **kwargs)