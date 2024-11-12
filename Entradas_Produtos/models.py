from django.db import models
from Pessoas.models import Pessoas
from Produtos.models import Produtos
from app import settings
from Empresas.models import Empresa


class EmpresaManager(models.Manager):
    def for_user(self, user):
        if not user.is_authenticated:
            return self.none()
        return self.filter(empresa=user.empresa)
    
class Base(models.Model):
    criado = models.DateField('Criado em', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True


class Entrada_Produtos(Base):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    pessoa = models.ForeignKey(Pessoas, on_delete=models.PROTECT, blank=False, null=False, related_name= 'entradas')
    produto = models.ForeignKey(Produtos, on_delete=models.PROTECT, blank=False, null=False, related_name='entradas')
    quantidade = models.IntegerField()
    documento = models.CharField('Nº Documento', max_length= 20, blank= True, null= True)
    observacoes = models.TextField('Observações', max_length=200, blank= True, null= True)
    
    objects = EmpresaManager()

    class Meta:
        ordering = ['-criado']
    
    class Meta:
        verbose_name = 'Entrada Produto'
        verbose_name_plural = 'Entrada Produtos'
        db_table = 'entradas'

def __str__(self):
    return str(self.produto)
    