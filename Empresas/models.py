from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Base(models.Model):
    criado = models.DateField('Criado em', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True


class Empresa(Base):
    name = models.CharField('Nome da Empresa', max_length=100)
    document = models.CharField('CPF/CNPJ', max_length=18, unique=True)
    database = models.CharField('Banco de Dados', max_length=100, unique=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)  # Remova o valor padrão


    def __str__(self):
        return self.username


class Licenca(Base):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    documento = models.CharField('Número da Licença', max_length=100, unique=True)
    data_ativacao = models.DateField('Data de Ativação')
    data_expiracao = models.DateField('Data de Expiração')
    tipo = models.CharField('Tipo de Licença', max_length=50, choices=[('mensal', 'Mensal'), ('anual', 'Anual'), ('permanente', 'Permanente')])
    ativo = models.BooleanField('Ativo?', default=True)

    def __str__(self):
        return f'Licença {self.documento} - {self.empresa.name}'

    def is_ativa(self):
        return self.ativo and (self.data_expiracao > timezone.now().date())