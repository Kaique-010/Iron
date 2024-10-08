# Generated by Django 5.0.7 on 2024-09-03 23:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Financeiro', '0001_initial'),
        ('Pessoas', '0002_alter_pessoas_classificacao'),
        ('Produtos', '0002_alter_produtos_familia_alter_produtos_grupo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('numero_pedido', models.CharField(blank=True, max_length=20, unique=True, verbose_name='Nº Pedido')),
                ('data', models.DateTimeField(blank=True, null=True, verbose_name='Data do Pedido')),
                ('status', models.CharField(choices=[('Pendente', 'Pendente'), ('Processando', 'Processando'), ('Enviado', 'Enviado'), ('Concluído', 'Concluído'), ('Cancelado', 'Cancelado')], default='Pendente', max_length=20, verbose_name='Status')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pedidos', to='Pessoas.pessoas')),
                ('financeiro', models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, to='Financeiro.formasrecebimento')),
                ('vendedor', models.ForeignKey(default='Sem Vendedor', limit_choices_to={'classificacao': 'Vendedor'}, on_delete=django.db.models.deletion.PROTECT, related_name='vendas', to='Pessoas.pessoas')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'ordering': ['criado', 'id'],
            },
        ),
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('quantidade', models.PositiveIntegerField(verbose_name='Quantidade')),
                ('preco_unitario', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço Unitário')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='Produtos.produtos')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='Pedidos.pedido')),
            ],
            options={
                'verbose_name': 'Item Pedido',
                'verbose_name_plural': 'Itens Pedido',
                'ordering': ['criado', 'id'],
            },
        ),
    ]
