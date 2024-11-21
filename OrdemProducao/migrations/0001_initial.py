# Generated by Django 5.1.2 on 2024-11-21 14:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Empresas', '0005_licenca'),
        ('Produtos', '0006_produtos_tipo_produto'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstoqueResponsavel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('quantidade_disponivel', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Quantidade Disponível')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.empresa')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='estoque_responsavel', to='Produtos.produtos')),
            ],
            options={
                'verbose_name': 'Estoque do Responsável',
                'verbose_name_plural': 'Estoques dos Responsáveis',
            },
        ),
        migrations.CreateModel(
            name='Etapa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('nome', models.CharField(max_length=100, unique=True, verbose_name='Nome da Etapa')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('ordem', models.PositiveIntegerField(default=1, verbose_name='Ordem da Etapa')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.empresa')),
            ],
            options={
                'verbose_name': 'Etapa',
                'verbose_name_plural': 'Etapas',
                'ordering': ['ordem', 'nome'],
            },
        ),
        migrations.CreateModel(
            name='EtapaProducao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('status', models.CharField(choices=[('NAO_INICIADA', 'Não Iniciada'), ('EM_PROGRESSO', 'Em Progresso'), ('CONCLUIDA', 'Concluída')], default='NAO_INICIADA', max_length=20, verbose_name='Status')),
                ('data_inicio', models.DateField(blank=True, null=True, verbose_name='Data de Início')),
                ('data_conclusao', models.DateField(blank=True, null=True, verbose_name='Data de Conclusão')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.empresa')),
                ('etapa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='producoes', to='OrdemProducao.etapa')),
            ],
            options={
                'verbose_name': 'Execução da Etapa',
                'verbose_name_plural': 'Execuções das Etapas',
                'ordering': ['ordem_producao', 'etapa__ordem'],
            },
        ),
        migrations.CreateModel(
            name='MateriaPrimaConsumida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('quantidade_usada', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Quantidade Usada')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.empresa')),
                ('etapa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materias_primas', to='OrdemProducao.etapaproducao')),
                ('materia_prima', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='usada_em_etapas', to='Produtos.produtos')),
            ],
            options={
                'verbose_name': 'Matéria-Prima Consumida',
                'verbose_name_plural': 'Matérias-Primas Consumidas',
            },
        ),
        migrations.AddField(
            model_name='etapaproducao',
            name='materias_primas_consumidas',
            field=models.ManyToManyField(blank=True, related_name='etapas_materias_primas', through='OrdemProducao.MateriaPrimaConsumida', to='Produtos.produtos'),
        ),
        migrations.CreateModel(
            name='OrdemProducao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('numero_ordem', models.CharField(max_length=20, unique=True, verbose_name='Número da Ordem')),
                ('quantidade', models.PositiveIntegerField(verbose_name='Quantidade a Produzir')),
                ('status', models.CharField(choices=[('PLANEJADA', 'Planejada'), ('EM_PROGRESSO', 'Em Progresso'), ('FINALIZADA', 'Finalizada')], default='PLANEJADA', max_length=20, verbose_name='Status')),
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='Data de Criação')),
                ('data_prevista_finalizacao', models.DateField(blank=True, null=True, verbose_name='Data Prevista de Finalização')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.empresa')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ordens_producao', to='Produtos.produtos')),
            ],
            options={
                'verbose_name': 'Ordem de Produção',
                'verbose_name_plural': 'Ordens de Produção',
                'ordering': ['-data_criacao', 'numero_ordem'],
            },
        ),
        migrations.AddField(
            model_name='etapaproducao',
            name='ordem_producao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='etapas', to='OrdemProducao.ordemproducao'),
        ),
        migrations.CreateModel(
            name='Responsavel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('cargo', models.CharField(max_length=50, verbose_name='Cargo/Função')),
                ('permissoes', models.TextField(blank=True, null=True, verbose_name='Permissões')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.empresa')),
                ('estoque_sob_responsabilidade', models.ManyToManyField(blank=True, related_name='responsaveis', through='OrdemProducao.EstoqueResponsavel', to='Produtos.produtos')),
            ],
            options={
                'verbose_name': 'Responsável',
                'verbose_name_plural': 'Responsáveis',
            },
        ),
        migrations.AddField(
            model_name='ordemproducao',
            name='responsavel_atual',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ordens_em_progresso', to='OrdemProducao.responsavel'),
        ),
        migrations.AddField(
            model_name='etapaproducao',
            name='responsavel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='etapas_responsaveis', to='OrdemProducao.responsavel'),
        ),
        migrations.AddField(
            model_name='etapa',
            name='responsavel_padrao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='etapas_padrao', to='OrdemProducao.responsavel'),
        ),
        migrations.AddField(
            model_name='estoqueresponsavel',
            name='responsavel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estoques', to='OrdemProducao.responsavel'),
        ),
    ]
