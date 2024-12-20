# Generated by Django 5.1.2 on 2024-11-20 23:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Empresas', '0005_licenca'),
    ]

    operations = [
        migrations.CreateModel(
            name='CFOP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('cfop', models.CharField(choices=[('1101', '1101 - Compra para industrialização'), ('1102', '1102 - Compra para comercialização'), ('1111', '1111 - Compra para industrialização por encomenda'), ('1113', '1113 - Compra para industrialização sob o regime de drawback'), ('1116', '1116 - Compra para utilização na prestação de serviço'), ('1121', '1121 - Devolução de venda de produção do estabelecimento'), ('1122', '1122 - Devolução de venda de mercadoria adquirida ou recebida de terceiros'), ('1201', '1201 - Entrada para industrialização por conta e ordem do adquirente da mercadoria, quando esta não transitar pelo estabelecimento do adquirente'), ('1202', '1202 - Entrada para industrialização por conta e ordem do adquirente da mercadoria, quando esta transitar pelo estabelecimento do adquirente'), ('1301', '1301 - Entrada de mercadoria com previsão de exportação'), ('1403', '1403 - Compra para comercialização com substituição tributária'), ('2101', '2101 - Compra para industrialização, de mercadoria procedente de outro estado'), ('2102', '2102 - Compra para comercialização, de mercadoria procedente de outro estado'), ('2103', '2103 - Compra para uso ou consumo, de mercadoria procedente de outro estado'), ('2201', '2201 - Devolução de venda de mercadoria adquirida de outro estado'), ('2202', '2202 - Devolução de venda de mercadoria adquirida de outro estado, com ICMS devido por substituição tributária'), ('2301', '2301 - Compra de mercadoria em consignação, de outro estado'), ('2401', '2401 - Entrada de mercadoria importada, de outro estado'), ('2701', '2701 - Entrada de mercadoria de fora do estado por conta e ordem de terceiros'), ('5101', '5101 - Venda de produção do estabelecimento'), ('5102', '5102 - Venda de mercadoria adquirida ou recebida de terceiros'), ('5111', '5111 - Venda de produção do estabelecimento sob o regime de drawback'), ('5112', '5112 - Venda de mercadoria adquirida ou recebida de terceiros, utilizada em processo de industrialização sob o regime de drawback'), ('5113', '5113 - Venda de produção do estabelecimento destinada à Zona Franca de Manaus'), ('5114', '5114 - Venda de mercadoria adquirida de terceiros destinada à Zona Franca de Manaus'), ('5401', '5401 - Venda de produção do estabelecimento em operação com substituição tributária'), ('5403', '5403 - Venda de mercadoria adquirida ou recebida de terceiros em operação com substituição tributária'), ('5501', '5501 - Remessa de produção do estabelecimento com fim específico de exportação'), ('5502', '5502 - Remessa de mercadoria adquirida ou recebida de terceiros com fim específico de exportação'), ('5553', '5553 - Venda de energia elétrica para distribuição ou comercialização'), ('5554', '5554 - Venda de energia elétrica para estabelecimento comercial'), ('6101', '6101 - Venda de produção do estabelecimento ao consumidor final'), ('6102', '6102 - Venda de mercadoria adquirida de terceiros ao consumidor final'), ('6108', '6108 - Venda de mercadoria adquirida de terceiros ao consumidor final com isenção de ICMS'), ('6110', '6110 - Venda de produção do estabelecimento a empresa do Simples Nacional com isenção de ICMS'), ('6124', '6124 - Venda de produção do estabelecimento para industrialização por terceiros'), ('5931', '5931 - Prestação de serviço de transporte de carga'), ('5932', '5932 - Prestação de serviço de transporte de passageiros'), ('6931', '6931 - Prestação de serviço de comunicação'), ('6932', '6932 - Prestação de serviço de telecomunicação'), ('7949', '7949 - Outras saídas'), ('8949', '8949 - Outras entradas')], max_length=4, unique=True, verbose_name='CFOP Fiscal')),
                ('descricao_fiscal', models.CharField(max_length=255, verbose_name='Descrição Fiscal')),
                ('finalidade', models.CharField(choices=[('1', 'Entrada'), ('2', 'Saída'), ('3', 'Devolução'), ('4', 'Simples Remessa'), ('5', 'Outros')], max_length=255, verbose_name='Finalidade do CFOP')),
                ('aplica_icms', models.BooleanField(default=False, verbose_name='Aplica ICMS?')),
                ('aplica_pis', models.BooleanField(default=False, verbose_name='Aplica PIS?')),
                ('aplica_cofins', models.BooleanField(default=False, verbose_name='Aplica COFINS?')),
                ('aplica_ipi', models.BooleanField(default=False, verbose_name='Aplica IPI?')),
                ('cst_icms', models.CharField(blank=True, choices=[('00', 'Tributada integralmente'), ('10', 'Tributada e com cobrança do ICMS por substituição tributária'), ('20', 'Com redução de base de cálculo'), ('30', 'Isenta ou não tributada e com cobrança do ICMS por substituição tributária'), ('40', 'Isenta'), ('41', 'Não tributada'), ('50', 'Suspensão'), ('51', 'Diferimento'), ('60', 'ICMS cobrado anteriormente por substituição tributária'), ('70', 'Com redução de base de cálculo e cobrança do ICMS por substituição tributária'), ('90', 'Outras')], max_length=2, null=True, verbose_name='CST ICMS')),
                ('modalidade_calculo_icms', models.CharField(blank=True, max_length=50, null=True, verbose_name='Modalidade de Cálculo ICMS')),
                ('aliquota_icms', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Alíquota ICMS (%)')),
                ('reducao_icms', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Redução ICMS (%)')),
                ('mva', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='MVA (%)')),
                ('cst_pis', models.CharField(blank=True, choices=[('01', 'Operação Tributável com Alíquota Básica'), ('02', 'Operação Tributável com Alíquota Diferenciada'), ('03', 'Operação Tributável com Alíquota por Unidade de Medida'), ('04', 'Operação Tributável Monofásica - Alíquota Zero'), ('05', 'Operação Tributável por Substituição Tributária'), ('06', 'Operação Tributável - Alíquota Zero'), ('07', 'Operação Isenta da Contribuição'), ('08', 'Operação sem Incidência da Contribuição'), ('09', 'Operação com Suspensão da Contribuição'), ('49', 'Outras Operações de Saída')], max_length=2, null=True, verbose_name='CST PIS')),
                ('aliquota_pis', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Alíquota PIS (%)')),
                ('cst_cofins', models.CharField(blank=True, choices=[('01', 'Operação Tributável com Alíquota Básica'), ('02', 'Operação Tributável com Alíquota Diferenciada'), ('03', 'Operação Tributável com Alíquota por Unidade de Medida'), ('04', 'Operação Tributável Monofásica - Alíquota Zero'), ('05', 'Operação Tributável por Substituição Tributária'), ('06', 'Operação Tributável - Alíquota Zero'), ('07', 'Operação Isenta da Contribuição'), ('08', 'Operação sem Incidência da Contribuição'), ('09', 'Operação com Suspensão da Contribuição'), ('49', 'Outras Operações de Saída')], max_length=2, null=True, verbose_name='CST COFINS')),
                ('aliquota_cofins', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Alíquota COFINS (%)')),
                ('cst_ipi', models.CharField(blank=True, choices=[('00', 'Entrada com Recuperação de Crédito'), ('01', 'Entrada Tributada com Alíquota Zero'), ('02', 'Entrada Isenta'), ('03', 'Entrada Não Tributada'), ('04', 'Entrada Imune'), ('05', 'Entrada com Suspensão'), ('49', 'Outras Entradas'), ('50', 'Saída Tributada'), ('51', 'Saída Tributada com Alíquota Zero'), ('52', 'Saída Isenta'), ('53', 'Saída Não Tributada'), ('54', 'Saída Imune'), ('55', 'Saída com Suspensão'), ('99', 'Outras Saídas')], max_length=2, null=True, verbose_name='CST IPI')),
                ('aliquota_ipi', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Alíquota IPI (%)')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.empresa')),
            ],
            options={
                'verbose_name': 'CFOP',
                'verbose_name_plural': 'CFOPs',
            },
        ),
    ]
