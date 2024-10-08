# Generated by Django 5.0.7 on 2024-08-07 13:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Pessoas', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['criado', 'id'],
            },
        ),
        migrations.CreateModel(
            name='FormasPagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Forma de Pagamento',
                'verbose_name_plural': 'Formas de Pagamento',
                'ordering': ['criado', 'id'],
            },
        ),
        migrations.CreateModel(
            name='FormasRecebimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Forma de Recebimento',
                'verbose_name_plural': 'Formas de Recebimento',
                'ordering': ['criado', 'id'],
            },
        ),
        migrations.CreateModel(
            name='ContaAPagar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('documento', models.CharField(max_length=20, verbose_name='Documento')),
                ('descricao', models.CharField(max_length=255, verbose_name='Descrição')),
                ('parcela', models.IntegerField(verbose_name='Parcelas')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor')),
                ('data_emissao', models.DateField(verbose_name='Data de Emissão')),
                ('data_vencimento', models.DateField(verbose_name='Vencimento')),
                ('data_pagamento', models.DateField(blank=True, null=True, verbose_name='Data de Pagamento')),
                ('status_pagamento', models.BooleanField(default=False, verbose_name='Status de Pagamento')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('categorias', models.ForeignKey(max_length=100, on_delete=django.db.models.deletion.PROTECT, to='Financeiro.categorias')),
                ('pessoas', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contas_a_pagar', to='Pessoas.pessoas')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contas_a_pagar', to=settings.AUTH_USER_MODEL)),
                ('forma_pagamento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Financeiro.formaspagamento')),
            ],
            options={
                'verbose_name': 'Conta a Pagar',
                'verbose_name_plural': 'Contas a Pagar',
                'ordering': ['criado', 'id'],
            },
        ),
        migrations.CreateModel(
            name='ContaAReceber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('documento', models.CharField(max_length=20, verbose_name='Documento')),
                ('descricao', models.CharField(max_length=255, verbose_name='Descrição')),
                ('parcela', models.IntegerField(verbose_name='Parcelas')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor')),
                ('data_emissao', models.DateField(verbose_name='Data de Emissão')),
                ('data_vencimento', models.DateField(verbose_name='Vencimento')),
                ('data_recebimento', models.DateField(blank=True, null=True, verbose_name='Data de Recebimento')),
                ('status_recebimento', models.BooleanField(default=False)),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('categorias', models.ForeignKey(max_length=100, on_delete=django.db.models.deletion.PROTECT, to='Financeiro.categorias')),
                ('pessoas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contas_a_receber', to='Pessoas.pessoas')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contas_a_receber', to=settings.AUTH_USER_MODEL)),
                ('forma_recebimento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Financeiro.formasrecebimento')),
            ],
            options={
                'verbose_name': 'Conta a Receber',
                'verbose_name_plural': 'Contas a Receber',
                'ordering': ['criado', 'id'],
            },
        ),
    ]
