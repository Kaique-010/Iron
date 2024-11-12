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
    criado = models.DateField('Criado em', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True

class Grupo(Base):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nome = models.CharField('Nome', max_length=50) 
    descricao = models.TextField('Descrição', max_length= 100, blank= True, null= True)
    

    objects = EmpresaManager()
    
    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'

    class Meta:
        ordering = ['nome']
        db_table = 'grupos'
        
    
    def __str__(self):
        return self.nome  