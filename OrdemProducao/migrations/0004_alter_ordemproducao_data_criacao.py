# Generated by Django 5.1.2 on 2024-11-26 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrdemProducao', '0003_ordemproducao_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemproducao',
            name='data_criacao',
            field=models.DateField(verbose_name='Data de Criação'),
        ),
    ]