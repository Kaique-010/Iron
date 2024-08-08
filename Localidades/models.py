from django.db import models


class Localidade(models.Model):
    nome = models.CharField('Nome', max_length=50) 


    class Meta:
        verbose_name = 'Localidade'
        verbose_name_plural = 'Localidades'

    class Meta:
        ordering = ['nome']
    
    def __str__(self):
        return self.nome  