import uuid
from django.db import models
from django.db.models import signals
from django.template.defaultfilters import slugify
from stdimage import StdImageField
from django.utils.html import mark_safe
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

class Classificacao(models.TextChoices):
    CLIENTE = 'Cliente', 'Cliente'
    FORNECEDOR = 'Fornecedor', 'Fornecedor'
    FUNCIONARIO = 'Funcionário', 'Funcionário'
    VENDEDOR = 'Vendedor', 'Vendedor'
    AMBOS = 'Ambos', 'Ambos'

class Pessoas(Base):
    nome = models.CharField('Nome Completo', max_length=100)
    cpf = models.CharField('CPF', max_length=14, unique=True, blank=True, null=True)
    rg = models.CharField('RG', max_length=9, blank=True, null=True)
    email = models.EmailField('E-mail')
    cnpj = models.CharField('CNPJ', max_length=14, unique=True, blank=True, null=True)
    ie = models.CharField('IE', max_length=11, unique=True, blank=True, null=True)
    telefone = models.CharField('Telefone', max_length=14, unique=True)
    foto = StdImageField('Imagem', upload_to='pessoas', variations={'thumb': (150, 150)}, blank=True)
    obs = models.TextField('Observações', max_length=100)
    classificacao = models.CharField('Classificação', max_length=20, choices=Classificacao.choices)
    slug = models.SlugField('Slug', max_length=255, unique=True, blank=True)
    cep = models.CharField(max_length=9, default='00000-000')
    logradouro = models.CharField(max_length=255, blank=True, null=True)
    numero = models.IntegerField(default= 0)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)


    def __str__(self):
        return self.nome

    def imagem_tag(self):
        try:
            return mark_safe(f'<img src="{self.foto.url}" width="80" height="80" />')
        except AttributeError:
            return "No Image"
    @classmethod
    def get_vendedores(cls, user=None):
        if user:
            return cls.objects.filter(usuario=user, classificacao='vendedor')
        return cls.objects.none()
    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering = ['id', 'criado', 'modificado']
        db_table = 'pessoas'

def pessoas_pre_save(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.nome)

signals.pre_save.connect(pessoas_pre_save, sender=Pessoas)


