# Generated by Django 5.1.2 on 2024-11-21 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Produtos', '0005_produtos_ncm'),
    ]

    operations = [
        migrations.AddField(
            model_name='produtos',
            name='tipo_produto',
            field=models.CharField(choices=[('USO_CONSUMO', 'Uso e Consumo'), ('VENDA', 'Produto de Venda'), ('MATERIA_PRIMA', 'Matéria-Prima'), ('LOCACAO', 'Produto de Locação')], default='VENDA', max_length=20, verbose_name='Tipo de Produto'),
        ),
    ]