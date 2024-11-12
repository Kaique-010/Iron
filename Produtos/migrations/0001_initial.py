# Generated by Django 5.1.2 on 2024-11-08 20:44

import django.db.models.deletion
import stdimage.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Empresas', '0001_initial'),
        ('Familias', '0001_initial'),
        ('Grupo', '0001_initial'),
        ('Localidades', '0001_initial'),
        ('Marcas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('nome', models.CharField(max_length=50, verbose_name='Nome')),
                ('imagem', stdimage.models.StdImageField(force_min_size=False, upload_to='produtos', variations={'thumbnail': (150, 150)}, verbose_name='Imagem')),
                ('tamanho', models.CharField(blank=True, max_length=10, null=True, verbose_name='Tamanho')),
                ('peso', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Peso (em gramas)')),
                ('quantidade', models.IntegerField(default=0)),
                ('descricao', models.TextField(blank=True, max_length=100, null=True, verbose_name='Descrição')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.empresa')),
                ('familia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='produtos', to='Familias.familia')),
                ('grupo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='produtos', to='Grupo.grupo')),
                ('localidade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='produtos', to='Localidades.localidade')),
                ('marca', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='produtos', to='Marcas.marcas')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'db_table': 'produtos',
                'ordering': ['id', 'criado', 'modificado'],
            },
        ),
        migrations.CreateModel(
            name='Precos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco_compra', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço de Compra')),
                ('preco_venda_vista', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço de Venda à Vista')),
                ('preco_venda_prazo', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço de Venda a Prazo')),
                ('percentual_venda_vista', models.DecimalField(decimal_places=2, editable=False, max_digits=5, verbose_name='Percentual sobre Preço de Venda à Vista')),
                ('percentual_venda_prazo', models.DecimalField(decimal_places=2, editable=False, max_digits=5, verbose_name='Percentual sobre Preço de Venda a Prazo')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='precos', to='Produtos.produtos')),
            ],
            options={
                'verbose_name': 'Preço',
                'verbose_name_plural': 'Preços',
            },
        ),
    ]
