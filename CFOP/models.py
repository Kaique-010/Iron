from django.db import models
from Empresas.models import Empresa


class EmpresaManager(models.Manager):
    def for_user(self, user):
        if not user.is_authenticated:
            return self.none()
        return self.filter(empresa=user.empresa)

class Base(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    criado = models.DateField('Criado em', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    objects = EmpresaManager()
    
    class Meta:
        abstract = True


class CFOP(Base):
    
    CST_ICMS_CHOICES = [
    ('00', 'Tributada integralmente'),
    ('10', 'Tributada e com cobrança do ICMS por substituição tributária'),
    ('20', 'Com redução de base de cálculo'),
    ('30', 'Isenta ou não tributada e com cobrança do ICMS por substituição tributária'),
    ('40', 'Isenta'),
    ('41', 'Não tributada'),
    ('50', 'Suspensão'),
    ('51', 'Diferimento'),
    ('60', 'ICMS cobrado anteriormente por substituição tributária'),
    ('70', 'Com redução de base de cálculo e cobrança do ICMS por substituição tributária'),
    ('90', 'Outras'),
]


    CST_PIS_CHOICES = [
    ('01', 'Operação Tributável com Alíquota Básica'),
    ('02', 'Operação Tributável com Alíquota Diferenciada'),
    ('03', 'Operação Tributável com Alíquota por Unidade de Medida'),
    ('04', 'Operação Tributável Monofásica - Alíquota Zero'),
    ('05', 'Operação Tributável por Substituição Tributária'),
    ('06', 'Operação Tributável - Alíquota Zero'),
    ('07', 'Operação Isenta da Contribuição'),
    ('08', 'Operação sem Incidência da Contribuição'),
    ('09', 'Operação com Suspensão da Contribuição'),
    ('49', 'Outras Operações de Saída'),
]


    CST_COFINS_CHOICES = [
    ('01', 'Operação Tributável com Alíquota Básica'),
    ('02', 'Operação Tributável com Alíquota Diferenciada'),
    ('03', 'Operação Tributável com Alíquota por Unidade de Medida'),
    ('04', 'Operação Tributável Monofásica - Alíquota Zero'),
    ('05', 'Operação Tributável por Substituição Tributária'),
    ('06', 'Operação Tributável - Alíquota Zero'),
    ('07', 'Operação Isenta da Contribuição'),
    ('08', 'Operação sem Incidência da Contribuição'),
    ('09', 'Operação com Suspensão da Contribuição'),
    ('49', 'Outras Operações de Saída'),
]


    CST_IPI_CHOICES = [
    ('00', 'Entrada com Recuperação de Crédito'),
    ('01', 'Entrada Tributada com Alíquota Zero'),
    ('02', 'Entrada Isenta'),
    ('03', 'Entrada Não Tributada'),
    ('04', 'Entrada Imune'),
    ('05', 'Entrada com Suspensão'),
    ('49', 'Outras Entradas'),
    ('50', 'Saída Tributada'),
    ('51', 'Saída Tributada com Alíquota Zero'),
    ('52', 'Saída Isenta'),
    ('53', 'Saída Não Tributada'),
    ('54', 'Saída Imune'),
    ('55', 'Saída com Suspensão'),
    ('99', 'Outras Saídas'),
]

    
    CFOP_CHOICES = [
    # Operações de Entrada (Compra)
    ('1101', '1101 - Compra para industrialização'),
    ('1102', '1102 - Compra para comercialização'),
    ('1111', '1111 - Compra para industrialização por encomenda'),
    ('1113', '1113 - Compra para industrialização sob o regime de drawback'),
    ('1116', '1116 - Compra para utilização na prestação de serviço'),
    ('1121', '1121 - Devolução de venda de produção do estabelecimento'),
    ('1122', '1122 - Devolução de venda de mercadoria adquirida ou recebida de terceiros'),
    ('1201', '1201 - Entrada para industrialização por conta e ordem do adquirente da mercadoria, quando esta não transitar pelo estabelecimento do adquirente'),
    ('1202', '1202 - Entrada para industrialização por conta e ordem do adquirente da mercadoria, quando esta transitar pelo estabelecimento do adquirente'),
    ('1301', '1301 - Entrada de mercadoria com previsão de exportação'),
    ('1403', '1403 - Compra para comercialização com substituição tributária'),
    ('2101', '2101 - Compra para industrialização, de mercadoria procedente de outro estado'),
    ('2102', '2102 - Compra para comercialização, de mercadoria procedente de outro estado'),
    ('2103', '2103 - Compra para uso ou consumo, de mercadoria procedente de outro estado'),
    ('2201', '2201 - Devolução de venda de mercadoria adquirida de outro estado'),
    ('2202', '2202 - Devolução de venda de mercadoria adquirida de outro estado, com ICMS devido por substituição tributária'),
    ('2301', '2301 - Compra de mercadoria em consignação, de outro estado'),
    ('2401', '2401 - Entrada de mercadoria importada, de outro estado'),
    ('2701', '2701 - Entrada de mercadoria de fora do estado por conta e ordem de terceiros'),

    # Operações de Saída (Venda)
    ('5101', '5101 - Venda de produção do estabelecimento'),
    ('5102', '5102 - Venda de mercadoria adquirida ou recebida de terceiros'),
    ('5111', '5111 - Venda de produção do estabelecimento sob o regime de drawback'),
    ('5112', '5112 - Venda de mercadoria adquirida ou recebida de terceiros, utilizada em processo de industrialização sob o regime de drawback'),
    ('5113', '5113 - Venda de produção do estabelecimento destinada à Zona Franca de Manaus'),
    ('5114', '5114 - Venda de mercadoria adquirida de terceiros destinada à Zona Franca de Manaus'),
    ('5401', '5401 - Venda de produção do estabelecimento em operação com substituição tributária'),
    ('5403', '5403 - Venda de mercadoria adquirida ou recebida de terceiros em operação com substituição tributária'),
    ('5501', '5501 - Remessa de produção do estabelecimento com fim específico de exportação'),
    ('5502', '5502 - Remessa de mercadoria adquirida ou recebida de terceiros com fim específico de exportação'),
    ('5553', '5553 - Venda de energia elétrica para distribuição ou comercialização'),
    ('5554', '5554 - Venda de energia elétrica para estabelecimento comercial'),
    ('6101', '6101 - Venda de produção do estabelecimento ao consumidor final'),
    ('6102', '6102 - Venda de mercadoria adquirida de terceiros ao consumidor final'),
    ('6108', '6108 - Venda de mercadoria adquirida de terceiros ao consumidor final com isenção de ICMS'),
    ('6110', '6110 - Venda de produção do estabelecimento a empresa do Simples Nacional com isenção de ICMS'),
    ('6124', '6124 - Venda de produção do estabelecimento para industrialização por terceiros'),

    # Outros
    ('5931', '5931 - Prestação de serviço de transporte de carga'),
    ('5932', '5932 - Prestação de serviço de transporte de passageiros'),
    ('6931', '6931 - Prestação de serviço de comunicação'),
    ('6932', '6932 - Prestação de serviço de telecomunicação'),
    ('7949', '7949 - Outras saídas'),
    ('8949', '8949 - Outras entradas'),
]



    cfop = models.CharField("CFOP Fiscal", max_length=4, choices=CFOP_CHOICES, unique=True)
    descricao_fiscal = models.CharField("Descrição Fiscal", max_length=255)
    finalidade = models.CharField("Finalidade do CFOP",max_length=255, choices=[('1', 'Entrada'),('2', 'Saída'),('3', 'Devolução'),('4', 'Simples Remessa'),('5', 'Outros')])
    

    aplica_icms = models.BooleanField("Aplica ICMS?", default=False)
    aplica_pis = models.BooleanField("Aplica PIS?", default=False)
    aplica_cofins = models.BooleanField("Aplica COFINS?", default=False)
    aplica_ipi = models.BooleanField("Aplica IPI?", default=False)

    
    # Campos para ICMS com choices
    cst_icms = models.CharField("CST ICMS", max_length=2, choices=CST_ICMS_CHOICES, blank=True, null=True)
    modalidade_calculo_icms = models.CharField("Modalidade de Cálculo ICMS", max_length=50, blank=True, null=True)
    aliquota_icms = models.DecimalField("Alíquota ICMS (%)", max_digits=5, decimal_places=2, blank=True, null=True)
    reducao_icms = models.DecimalField("Redução ICMS (%)", max_digits=5, decimal_places=2, blank=True, null=True)
    mva = models.DecimalField("MVA (%)", max_digits=5, decimal_places=2, blank=True, null=True)

    
    # Campos para PIS com choices
    cst_pis = models.CharField("CST PIS", max_length=2, choices=CST_PIS_CHOICES, blank=True, null=True)
    aliquota_pis = models.DecimalField("Alíquota PIS (%)", max_digits=5, decimal_places=2, blank=True, null=True)

    
    # Campos para COFINS com choices
    cst_cofins = models.CharField("CST COFINS", max_length=2, choices=CST_COFINS_CHOICES, blank=True, null=True)
    aliquota_cofins = models.DecimalField("Alíquota COFINS (%)", max_digits=5, decimal_places=2, blank=True, null=True)

    
    # Campos para IPI com choices
    cst_ipi = models.CharField("CST IPI", max_length=2, choices=CST_IPI_CHOICES, blank=True, null=True)
    aliquota_ipi = models.DecimalField("Alíquota IPI (%)", max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.cfop} - {self.descricao_fiscal}"
    
    objects = EmpresaManager()
    
    class Meta:
        verbose_name = "CFOP"
        verbose_name_plural = "CFOPs"