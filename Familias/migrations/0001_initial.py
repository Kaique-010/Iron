# Generated by Django 5.1.2 on 2024-11-08 20:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Empresas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Familia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('nome', models.CharField(max_length=50, verbose_name='Nome')),
                ('descricao', models.TextField(blank=True, max_length=100, null=True, verbose_name='Descrição')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.empresa')),
            ],
            options={
                'verbose_name': 'Família',
                'verbose_name_plural': 'Famílias',
                'db_table': 'familias',
            },
        ),
    ]
