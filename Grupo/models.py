from django.db import models


class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True) 
    modificado = models.DateTimeField('Data de Modificação', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True  

class Grupo(Base):
    nome = models.CharField('Nome', max_length=50) 
    descricao = models.TextField('Descrição', max_length= 100, blank= True, null= True)



    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'

    class Meta:
        ordering = ['nome']
    
    def __str__(self):
        return self.nome  