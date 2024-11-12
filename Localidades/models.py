import uuid
from django.db import models
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
        
        
class Localidade(Base):
    nome = models.CharField('Nome', max_length=50) 
    


    class Meta:
        verbose_name = 'Localidade'
        verbose_name_plural = 'Localidades'

    class Meta:
        ordering = ['nome']
        db_table = 'localidades'
    
    def __str__(self):
        return self.nome  