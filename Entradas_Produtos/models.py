from django.db import models
from Pessoas.models import Pessoas
from Produtos.models import Produtos

class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True) 
    modificado = models.DateTimeField('Data de Modificação', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True  


class Entrada_Produtos(Base):
    pessoa = models.ForeignKey(Pessoas, on_delete=models.PROTECT, blank=False, null=False, related_name= 'entradas')
    produto = models.ForeignKey(Produtos, on_delete=models.PROTECT, blank=False, null=False, related_name='entradas')
    quantidade = models.IntegerField()
    documento = models.CharField('Nº Documento', max_length= 20, blank= True, null= True)
    observacoes = models.TextField('Observações', max_length=200, blank= True, null= True)

    class Meta:
        ordering = ['-criado']
    
    class Meta:
        verbose_name = 'Entrada Produto'
        verbose_name_plural = 'Entrada Produtos'

def __str__(self):
    return str(self.produtos)
    