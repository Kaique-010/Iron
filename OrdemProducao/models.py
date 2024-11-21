from django.db import models
from django.contrib.auth.models import User  
from datetime import date

from django.forms import ValidationError
from Empresas.models import Empresa
from Produtos.models import Produtos, UnidadeMedida
from Pessoas.models import Pessoas


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


class OrdemProducao(Base):
    STATUS_CHOICES = [
        ('PLANEJADA', 'Planejada'),
        ('EM_PROGRESSO', 'Em Progresso'),
        ('FINALIZADA', 'Finalizada'),
    ]

    
    numero_ordem = models.CharField('Número da Ordem', max_length=20, unique=True)
    cliente = models.ForeignKey(Pessoas, on_delete=models.PROTECT, related_name='ordens_producao')
    produto = models.ForeignKey(Produtos, on_delete=models.PROTECT, related_name='ordens_producao')
    quantidade = models.PositiveIntegerField('Quantidade a Produzir')
    unidade_medida = models.ForeignKey(UnidadeMedida,on_delete=models.CASCADE)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='PLANEJADA')
    data_criacao = models.DateField('Data de Criação')
    data_prevista_finalizacao = models.DateField('Data Prevista de Finalização', blank=True, null=True)
    responsavel_atual = models.ForeignKey(
        'Responsavel',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='ordens_em_progresso'
    )

    class Meta:
        verbose_name = 'Ordem de Produção'
        verbose_name_plural = 'Ordens de Produção'
        ordering = ['-data_criacao', 'numero_ordem']
    
    def __str__(self):
        return f"Ordem #{self.numero_ordem} - {self.produto.nome}"
    
   
    def etapas_concluidas(self):
        return self.etapas.filter(status='CONCLUIDA').count()
    
    def progresso(self):
        total = self.etapas.count()
        concluidas = self.etapas_concluidas()
        return (concluidas / total) * 100 if total > 0 else 0
    
    

class Etapa(Base):
    nome = models.CharField('Nome da Etapa', max_length=100, unique=True)
    descricao = models.TextField('Descrição', blank=True, null=True)
    responsavel_padrao = models.ForeignKey(
        'Responsavel',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='etapas_padrao'
    )
    ordem = models.PositiveIntegerField('Ordem da Etapa', default=1)

    class Meta:
        verbose_name = 'Etapa'
        verbose_name_plural = 'Etapas'
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome
    
    

class EtapaProducao(Base):
    STATUS_CHOICES = [
        ('NAO_INICIADA', 'Não Iniciada'),
        ('EM_PROGRESSO', 'Em Progresso'),
        ('CONCLUIDA', 'Concluída'),
    ]

    ordem_producao = models.ForeignKey('OrdemProducao', on_delete=models.CASCADE, related_name='etapas')
    etapa = models.ForeignKey('Etapa', on_delete=models.PROTECT, related_name='producoes')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='NAO_INICIADA')
    responsavel = models.ForeignKey(
        'Responsavel',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='etapas_responsaveis'
    )
    data_inicio = models.DateField('Data de Início', blank=True, null=True)
    data_conclusao = models.DateField('Data de Conclusão', blank=True, null=True)
    materias_primas_consumidas = models.ManyToManyField(Produtos,
        through='MateriaPrimaConsumida',
        related_name='etapas_materias_primas',
        blank=True
    )
    observacoes = models.TextField('Observações', blank=True, null=True)

    class Meta:
        verbose_name = 'Execução da Etapa'
        verbose_name_plural = 'Execuções das Etapas'
        ordering = ['ordem_producao', 'etapa__ordem']
    
    def __str__(self):
        return f"{self.etapa.nome} - {self.ordem_producao.numero_ordem}"

    def clean(self):
        if self.data_conclusao and self.data_conclusao < self.data_inicio:
            raise ValidationError("A data de conclusão não pode ser anterior à data de início.")
        super().clean()



class MateriaPrimaConsumida(Base):
    etapa = models.ForeignKey('EtapaProducao', on_delete=models.CASCADE, related_name='materias_primas')
    materia_prima = models.ForeignKey(Produtos, on_delete=models.PROTECT, related_name='usada_em_etapas')
    quantidade_usada = models.DecimalField('Quantidade Usada', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Matéria-Prima Consumida'
        verbose_name_plural = 'Matérias-Primas Consumidas'
    
    def __str__(self):
        return f"{self.materia_prima.nome} - {self.quantidade_usada}"



class Responsavel(Base):
    nome = models.CharField('Nome', max_length=100)
    cargo = models.CharField('Cargo/Função', max_length=50)
    estoque_sob_responsabilidade = models.ManyToManyField(Produtos,
        through='EstoqueResponsavel',
        related_name='responsaveis',
        blank=True
    )
    permissoes = models.TextField('Permissões', blank=True, null=True) 

    class Meta:
        verbose_name = 'Responsável'
        verbose_name_plural = 'Responsáveis'
    
    def __str__(self):
        return self.nome



class EstoqueResponsavel(Base):
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, related_name='estoques')
    produto = models.ForeignKey(Produtos, on_delete=models.PROTECT, related_name='estoque_responsavel')
    quantidade_disponivel = models.DecimalField('Quantidade Disponível', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Estoque do Responsável'
        verbose_name_plural = 'Estoques dos Responsáveis'
    
    def __str__(self):
        return f"{self.responsavel.nome} - {self.produto.nome}: {self.quantidade_disponivel}"
    
    def clean(self):
        if self.quantidade_disponivel < 0:
            raise ValidationError("A quantidade disponível não pode ser negativa.")
        super().clean()
