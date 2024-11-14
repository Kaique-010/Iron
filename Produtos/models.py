import uuid
from django.db import models
from Localidades.models import Localidade
from Familias.models import Familia
from Grupo.models import Grupo
from Marcas.models import Marcas
from stdimage import StdImageField
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
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

class UnidadeMedida(models.Model):
    descricao = models.CharField("Unidades de Medidas", max_length=100)
    sigla = models.CharField("siglas", max_length=100)
    
    class Meta:
        verbose_name = 'Unidade de Medida'
        verbose_name_plural = 'Unidades de Medidas'
        ordering = ['id']
        db_table = 'unidadedemedida'
    
    objects = EmpresaManager()
    
    def __str__(self):
        return f"{self.descricao} - {self.sigla}"

class Produtos(Base):
    nome = models.CharField('Nome', max_length=50)
    unidade_medida = models.ForeignKey(UnidadeMedida, on_delete=models.PROTECT, related_name='produtos', blank= True, null=True)
    ncm = models.CharField('NCM', max_length=8, blank=True, null=True)
    localidade = models.ForeignKey(Localidade, on_delete=models.PROTECT, related_name='produtos', blank= True, null=True)
    familia = models.ForeignKey(Familia, on_delete=models.PROTECT, related_name='produtos',blank= True, null=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT, related_name='produtos',blank= True, null=True)
    marca = models.ForeignKey(Marcas, on_delete=models.PROTECT, related_name='produtos', blank= True, null=True)
    imagem = StdImageField('Imagem', upload_to='produtos', variations={'thumbnail': (150, 150)}, blank=False, null=False)
    tamanho = models.CharField('Tamanho', max_length=10, blank=True, null=True)
    peso = models.DecimalField('Peso (em gramas)', max_digits=6, decimal_places=2, blank=False, null=False)
    quantidade = models.IntegerField(default=0)
    descricao = models.TextField('Descrição', max_length=100, blank= True, null= True)

    

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['id', 'criado', 'modificado']
        db_table = 'produtos'
    
    def __str__(self):
        return self.nome

    def imagem_tag(self):
        try:
            return mark_safe(f'<img src="{self.imagem.url}" width="80" height="80" />')
        except AttributeError:
            return "No Image"

    imagem_tag.short_description = 'Imagem'


class Precos(models.Model):
    produto = models.ForeignKey(Produtos, on_delete=models.PROTECT, related_name='precos')
    preco_compra = models.DecimalField('Preço de Compra', max_digits=10, decimal_places=2)
    preco_venda_vista = models.DecimalField('Preço de Venda à Vista', max_digits=10, decimal_places=2)
    preco_venda_prazo = models.DecimalField('Preço de Venda a Prazo', max_digits=10, decimal_places=2)
    percentual_venda_vista = models.DecimalField('Percentual sobre Preço de Venda à Vista', max_digits=5, decimal_places=2)
    percentual_venda_prazo = models.DecimalField('Percentual sobre Preço de Venda a Prazo', max_digits=5, decimal_places=2)



    def __str__(self):
        return f'{self.produto.nome} - Preços'

    def clean(self):
        if self.preco_compra < 0:
            raise ValidationError({'preco_compra': 'O preço de compra não pode ser negativo.'})
        if self.preco_venda_vista < 0:
            raise ValidationError({'preco_venda_vista': 'O preço de venda à vista não pode ser negativo.'})
        if self.preco_venda_prazo < 0:
            raise ValidationError({'preco_venda_prazo': 'O preço de venda a prazo não pode ser negativo.'})
        if self.preco_compra > 0:
            self.percentual_venda_vista = ((self.preco_venda_vista - self.preco_compra) / self.preco_compra) * 100
            self.percentual_venda_prazo = ((self.preco_venda_prazo - self.preco_compra) / self.preco_compra) * 100
        print(f'Percentual Venda Vista: {self.percentual_venda_vista}')
        print(f'Percentual Venda Prazo: {self.percentual_venda_prazo}')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Preço'
        verbose_name_plural = 'Preços'


