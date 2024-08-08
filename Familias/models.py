from django.db import models

class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True) 
    modificado = models.DateTimeField('Data de Modificação', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True  



class Familia(Base):
    nome = models.CharField('Nome', max_length=50)
    descricao = models.TextField('Descrição', max_length= 100,blank= True, null= True)

    class Meta:
        ordering = ['id','nome']

    class Meta:
        verbose_name = 'Família'  # Nome singular no admin
        verbose_name_plural = 'Famílias'  # Nome plural no admin
        
    def __str__(self):
        return self.nome