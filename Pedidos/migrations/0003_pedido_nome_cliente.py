# Generated by Django 5.0.7 on 2024-09-05 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0002_pedido_forma_recebimento_pedido_nome_vendedor'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='nome_cliente',
            field=models.CharField(blank=True, max_length=100, verbose_name='Nome Cliente'),
        ),
    ]
