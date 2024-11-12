# Generated by Django 5.1.2 on 2024-11-11 18:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0004_alter_customuser_last_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='Licenca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('documento', models.CharField(max_length=100, unique=True, verbose_name='Número da Licença')),
                ('data_ativacao', models.DateField(verbose_name='Data de Ativação')),
                ('data_expiracao', models.DateField(verbose_name='Data de Expiração')),
                ('tipo', models.CharField(choices=[('mensal', 'Mensal'), ('anual', 'Anual'), ('permanente', 'Permanente')], max_length=50, verbose_name='Tipo de Licença')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.empresa')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
