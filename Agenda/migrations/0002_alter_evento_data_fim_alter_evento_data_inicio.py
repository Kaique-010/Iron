# Generated by Django 5.0.7 on 2024-09-03 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agenda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='data_fim',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='evento',
            name='data_inicio',
            field=models.DateField(),
        ),
    ]
