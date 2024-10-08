# Generated by Django 5.0.7 on 2024-08-13 17:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Pessoas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('data_inicio', models.DateTimeField()),
                ('data_fim', models.DateTimeField()),
                ('horario', models.TimeField()),
                ('local', models.CharField(blank=True, max_length=200, null=True)),
                ('responsavel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Pessoas.pessoas')),
            ],
        ),
    ]
