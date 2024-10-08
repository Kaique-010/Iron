# Generated by Django 5.0.7 on 2024-08-07 13:02

import stdimage.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pessoas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Data de Criação')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Data de Modificação')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome Completo')),
                ('cpf', models.CharField(blank=True, max_length=14, null=True, unique=True, verbose_name='CPF')),
                ('rg', models.CharField(blank=True, max_length=9, null=True, verbose_name='RG')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('cnpj', models.CharField(blank=True, max_length=14, null=True, unique=True, verbose_name='CNPJ')),
                ('ie', models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='IE')),
                ('telefone', models.CharField(max_length=14, unique=True, verbose_name='Telefone')),
                ('foto', stdimage.models.StdImageField(blank=True, force_min_size=False, upload_to='pessoas', variations={'thumb': (150, 150)}, verbose_name='Imagem')),
                ('obs', models.TextField(max_length=100, verbose_name='Observações')),
                ('classificacao', models.CharField(choices=[('Cliente', 'Cliente'), ('Fornecedor', 'Fornecedor'), ('Funcionário', 'Funcionário'), ('Ambos', 'Ambos')], max_length=20, verbose_name='Classificação')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Pessoa',
                'verbose_name_plural': 'Pessoas',
                'ordering': ['id', 'criado', 'modificado'],
            },
        ),
    ]
