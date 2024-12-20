# Generated by Django 5.1.2 on 2024-11-08 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('titulo', models.CharField(max_length=200)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('data_inicio', models.DateField()),
                ('data_fim', models.DateField()),
                ('horario', models.TimeField()),
                ('local', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
                'db_table': 'evento',
                'ordering': ['id'],
            },
        ),
    ]
