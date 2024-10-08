# Generated by Django 5.0.7 on 2024-09-03 23:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Familias', '0001_initial'),
        ('Grupo', '0001_initial'),
        ('Produtos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produtos',
            name='familia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='produtos', to='Familias.familia'),
        ),
        migrations.AlterField(
            model_name='produtos',
            name='grupo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='produtos', to='Grupo.grupo'),
        ),
    ]
