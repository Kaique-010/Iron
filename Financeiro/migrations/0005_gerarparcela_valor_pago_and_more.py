# Generated by Django 5.1.2 on 2024-11-26 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Financeiro', '0004_gerarparcela'),
    ]

    operations = [
        migrations.AddField(
            model_name='gerarparcela',
            name='valor_pago',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='gerarparcela',
            name='pagamento_parcial',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='gerarparcela',
            name='pagamento_total',
            field=models.BooleanField(default=False),
        ),
    ]
