from django.db import models
from django.conf import settings
from Pessoas.models import Pessoas
from Empresas.models import Empresa


class Base(models.Model):
    criado = models.DateField('Criado em', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True
        

class Evento(Base):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    responsavel = models.ForeignKey(Pessoas, on_delete=models.PROTECT, null=True, blank=True)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    horario = models.TimeField()
    local = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="eventos_usuario")

   
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['id']
        db_table = 'evento'
