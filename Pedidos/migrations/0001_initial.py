# Generated by Django 5.1.2 on 2024-11-08 20:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Empresas', '0001_initial'),
        ('Financeiro', '0001_initial'),
        ('Pessoas', '0001_initial'),
        ('Produtos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('nome_cliente', models.CharField(blank=True, max_length=100, verbose_name='Nome Cliente')),
                ('data', models.DateField(blank=True, null=True, verbose_name='Data do Pedido')),
                ('status', models.CharField(choices=[('Pendente', 'Pendente'), ('Processando', 'Processando'), ('Enviado', 'Enviado'), ('Concluído', 'Concluído'), ('Cancelado', 'Cancelado')], default='Pendente', max_length=20, verbose_name='Status')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total')),
                ('nome_vendedor', models.CharField(blank=True, max_length=100, verbose_name='Nome do Vendedor')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('contato_realizado', models.BooleanField(default=False)),
                ('data_contato', models.DateField(blank=True, null=True)),
                ('notas_contato', models.TextField(blank=True, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pedidos', to='Pessoas.pessoas')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.empresa')),
                ('financeiro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Financeiro.formasrecebimento')),
                ('vendedor', models.ForeignKey(blank=True, limit_choices_to={'classificacao': 'Vendedor'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vendas', to='Pessoas.pessoas')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'db_table': 'pedidos',
                'ordering': ['criado', 'id'],
                'get_latest_by': 'data',
            },
        ),
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(verbose_name='Quantidade')),
                ('preco_unitario', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço Unitário')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='Produtos.produtos')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='Pedidos.pedido')),
            ],
            options={
                'verbose_name': 'Item Pedido',
                'verbose_name_plural': 'Itens Pedido',
                'ordering': ['id'],
            },
        ),
    ]
