# Generated by Django 5.0.7 on 2024-08-07 13:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Pessoas', '0001_initial'),
        ('Produtos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Saida_Produtos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Data de Criação')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Data de Modificação')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('quantidade', models.IntegerField()),
                ('documento', models.CharField(blank=True, max_length=20, null=True, verbose_name='Nº Documento')),
                ('observacoes', models.TextField(blank=True, max_length=200, null=True, verbose_name='Observações')),
                ('pessoa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='saidas', to='Pessoas.pessoas')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='saidas', to='Produtos.produtos')),
            ],
            options={
                'verbose_name': 'Saída Produto',
                'verbose_name_plural': 'Saída Produtos',
            },
        ),
    ]
