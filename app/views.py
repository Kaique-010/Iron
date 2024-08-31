from django.shortcuts import render
from Produtos.models import Produtos, Precos, models
from Entradas_Produtos.models import Entrada_Produtos
from Saidas_Produtos.models import Saida_Produtos
from django.db.models import Sum, F
 

def home(request):

    
    # Calcular o total de produtos
    total_produtos = Produtos.objects.count()

    # Calcular o total de produtos ativos
    total_produtos_ativos = Produtos.objects.filter(ativo=True).count()

    # Calcular o total de produtos inativos
    total_produtos_inativos = Produtos.objects.filter(ativo=False).count()
    
    # Calcular o saldo total de produtos
    total_saldo_produtos = Produtos.objects.aggregate(total_quantidade=models.Sum('quantidade'))['total_quantidade'] or 0
    
    # Calcular o valor total do estoque
    valor_estoque = Produtos.objects.annotate(
        valor_total=models.Sum(models.F('quantidade') * models.F('precos__preco_compra'))
    ).aggregate(total_valor_estoque=models.Sum('valor_total'))['total_valor_estoque'] or 0

     # Calcular as entradas e saídas de estoque
    total_entradas = Entrada_Produtos.objects.count()
    total_saidas = Saida_Produtos.objects.count()
    
    # Calcular a quantidade total movimentada
    total_quantidade_entradas = Entrada_Produtos.objects.aggregate(total=Sum('quantidade'))['total'] or 0
    total_quantidade_saidas = Saida_Produtos.objects.aggregate(total=Sum('quantidade'))['total'] or 0

    # Calcular o total de movimentações
    total_movimentacoes = total_quantidade_entradas + total_quantidade_saidas

    produtos_metricas = {
        'total_produtos': total_produtos,
        'total_produtos_ativos': total_produtos_ativos,
        'total_produtos_inativos': total_produtos_inativos,
        'total_saldo_produtos': total_saldo_produtos,
        'valor_estoque': valor_estoque,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'total_quantidade_entradas': total_quantidade_entradas,
        'total_quantidade_saidas': total_quantidade_saidas,
        'total_movimentacoes': total_movimentacoes,
    }
    
    context = {'produtos_metricas': produtos_metricas}
    return render(request, 'home.html', context)
