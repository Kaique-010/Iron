from django.db import models
from django.db.models import signals
from django.template.defaultfilters import slugify
from stdimage import StdImageField
from django.utils.html import mark_safe

class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True)
    modificado = models.DateField('Data de Modificação', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

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

    def __str__(self):
        return self.nome

    def imagem_tag(self):
        try:
            return mark_safe(f'<img src="{self.foto.url}" width="80" height="80" />')
        except AttributeError:
            return "No Image"
        
    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering = ['id', 'criado', 'modificado']

def pessoas_pre_save(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.nome)

signals.pre_save.connect(pessoas_pre_save, sender=Pessoas)


