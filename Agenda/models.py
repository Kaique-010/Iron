from django.db import models
from Pessoas.models import Pessoas

class Evento(models.Model):
    responsavel= models.ForeignKey(Pessoas, on_delete=models.PROTECT)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    horario = models.TimeField()
    local = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.titulo
