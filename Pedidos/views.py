from datetime import date, timedelta
import json
from io import BytesIO
import openpyxl
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, DeleteView
from django.forms import inlineformset_factory
from django.core import serializers
from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django.db.models import Sum, Count, F, Max
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from django.db import connection
from collections import namedtuple
from Financeiro.models import FormasRecebimento
from Pessoas.models import Pessoas
from .models import Pedido, ItemPedido
from .forms import CRMForm, ItemPedidoForm, PedidoForm
from Produtos.models import Produtos
from Financeiro.forms import DateRangeForm
from django.core.exceptions import MultipleObjectsReturned
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse



# Função utilitária para converter resultados de cursor em dicionário
def dictfetchall(cursor):
    """Converte todas as linhas do cursor em um dicionário."""
    columns = [col[0] for col in cursor.description]
    Row = namedtuple('Row', columns)
    return [Row(*row)._asdict() for row in cursor.fetchall()]


# Formset para ItemPedido
ItemPedidoFormSet = inlineformset_factory(Pedido, ItemPedido, form=ItemPedidoForm, extra=1, can_delete=True)


class PedidosListView(ListView):
    model = Pedido
    template_name = 'pedidoslistas.html'
    context_object_name = 'pedidos'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        pedido = self.request.GET.get('pedido')
        cliente = self.request.GET.get('cliente')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if pedido:
            queryset = queryset.filter(id__icontains=pedido)
        if cliente:
            queryset = queryset.filter(cliente__nome__icontains=cliente)
        if start_date:
            start_date = parse_date(start_date)
            if start_date:
                queryset = queryset.filter(data__gte=start_date)
        if end_date:
            end_date = parse_date(end_date)
            if end_date:
                queryset = queryset.filter(data__lte=end_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = DateRangeForm(self.request.GET or None)

        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')

        context['form'] = form
        context['total_count'] = self.get_queryset().count()
        context['total_value'] = self.get_queryset().aggregate(total_value=Sum('total'))['total_value'] or 0
        context['start_date'] = start_date
        context['end_date'] = end_date

        return context



def criar_pedido(request):
    pedido_status = Pedido._meta.get_field('status').choices
    clientes = Pessoas.objects.all()
    formas = Pedido.forma_recebimento  # Verifique se isso é definido corretamente

    if request.method == 'POST':
        status = request.POST.get('status')
        cliente_id = request.POST.get('cliente')
        data = request.POST.get('data')
        
        if not data:
            return HttpResponseBadRequest("Data não pode estar vazia")

        itens = []
        for i in range(0, len(request.POST.getlist('itens[0][produto_id]'))):
            produto_id = request.POST.get(f'itens[{i}][produto_id]')
            quantidade = request.POST.get(f'itens[{i}][quantidade]')
            preco_unitario = request.POST.get(f'itens[{i}][preco_unitario]')
            if produto_id and quantidade and preco_unitario:
                try:
                    itens.append((int(produto_id), int(quantidade), float(preco_unitario)))
                except ValueError:
                    return HttpResponseBadRequest("Dados dos itens inválidos")

        if not itens:
            return HttpResponseBadRequest("Nenhum item foi adicionado ao pedido")

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO pedidos_pedido (status, cliente_id, data, forma_recebimento)
                VALUES (%s, %s, %s, %s)
            """, [status, cliente_id, data, 'forma_recebimento_placeholder'])  # Ajuste conforme necessário
            pedido_id = cursor.lastrowid
            
            for produto_id, quantidade, preco_unitario in itens:
                cursor.execute("""
                    INSERT INTO pedidos_itempedido (pedido_id, produto_id, quantidade, preco_unitario)
                    VALUES (%s, %s, %s, %s)
                """, [pedido_id, produto_id, quantidade, preco_unitario])
        
        return redirect('pedidoslistas')  

    context = {
        'pedido_status': pedido_status,
        'clientes': clientes,
        'formas': formas
    }

    return render(request, 'pedidoscriar.html', context)




def buscar_produtos(request):
    query = request.GET.get('q', '')
    produtos = Produtos.objects.filter(nome__icontains=query)
    resultado = [{'id': produto.id, 'nome': produto.nome} for produto in produtos]
    return JsonResponse(resultado, safe=False)


class PedidosUpdateView(UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedidoseditar.html'
    success_url = reverse_lazy('pedidoslistas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            formset = ItemPedidoFormSet(self.request.POST, instance=self.object)
        else:
            formset = ItemPedidoFormSet(instance=self.object)
        context['formset'] = formset
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Atualiza o formset com a instância do pedido existente ou recém-atualizado
        formset = ItemPedidoFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()  # Salva o formset com os itens
        else:
            # Em caso de erro, renderiza o template com erros
            return self.render_to_response(self.get_context_data(form=form, formset=formset))
        
        return response

class PedidosDetailView(DetailView):
    model = Pedido
    template_name = 'pedidosdetalhe.html'

class PedidosDeleteView(DeleteView):
    model = Pedido
    template_name = 'pedidosexcluir.html'
    success_url = reverse_lazy('pedidoslistas')

def pedido_itens(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    context = {'pedido': pedido}
    return render(request, 'pedido_itens.html', context)

def criar_planilha_pedidos(pedidos):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Pedidos'
    columns = ['Nº Pedido', 'Data', 'Cliente', 'Total Pedido', 'Vendedor']
    worksheet.append(columns)
    for pedido in pedidos:
        worksheet.append([
            pedido.id,  # Alterado de pedido.pedido_id para pedido.id
            pedido.data.strftime('%d-%m-%y'),
            pedido.cliente.nome if pedido.cliente else '',
            pedido.total,
            pedido.nome_vendedor
        ])
    return workbook

def exportar_pedidos_excel(request):
    pedidos = Pedido.objects.all()
    workbook = criar_planilha_pedidos(pedidos)
    worksheet_itens = workbook.create_sheet(title='Itens dos Pedidos')
    columns_itens = ['Nº Pedido', 'Item', 'Quantidade', 'Preço Unitário', 'Subtotal']
    worksheet_itens.append(columns_itens)
    itens_pedidos = ItemPedido.objects.select_related('pedido').all()
    for item in itens_pedidos:
        worksheet_itens.append([
            item.pedido.id,  # Alterado de item.pedido.pedido_id para item.pedido.id
            item.produto.nome,
            item.quantidade,
            item.preco_unitario,
            item.quantidade * item.preco_unitario,
        ])

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=pedidos.xlsx'
    return response

def crm(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    cliente = request.GET.get('cliente')

    start_date = parse_date(start_date) if start_date else None
    end_date = parse_date(end_date) if end_date else None

    query = """
        SELECT 
            p.id AS "Nº Pedido",  
            p.data,
            p.cliente_id AS "Cliente",
            p.nome_cliente AS "Nome Cliente",
            p.nome_vendedor AS "Nome Vendedor",
            p.notas_contato AS "Notas Contato",
            p.id AS "pedido_id"
        FROM pedidos_pedido p
        INNER JOIN (
            SELECT 
                cliente_id,
                MAX(id) AS max_numero_pedido  
            FROM pedidos_pedido
            GROUP BY cliente_id
        ) sub ON p.cliente_id = sub.cliente_id AND p.id = sub.max_numero_pedido
    """

    params = []
    if start_date and end_date:
        query += " WHERE p.data BETWEEN %s AND %s"
        params.extend([start_date, end_date])

    if cliente:
        query += " AND p.nome_cliente LIKE %s"
        params.append(f"%{cliente}%")

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        result = cursor.fetchall()

    context = {
        'crm_data': result,
        'start_date': start_date,
        'end_date': end_date,
        'form': CRMForm(initial={'start_date': start_date, 'end_date': end_date}),
    }
    return render(request, 'crm.html', context)

def marcar_contato_realizado(request, pedido_id):
    try:
        pedido = Pedido.objects.get(id=pedido_id)  # Alterado de numero_pedido para id
        pedido.contato_realizado = True
        pedido.data_contato = now().date()
        pedido.save()
    except Pedido.DoesNotExist:
        return redirect('crm')
    except MultipleObjectsReturned:
        return redirect('crm')

    return redirect('detalhar_contato', pedido_id=pedido_id)

def detalhar_contato(request, pedido_id):
    query = """
         SELECT
            p.id AS "numero_pedido",  # Alterado de p.pedido_id para p.id
            p.data,
            p.nome_cliente AS "nome_cliente",
            p.nome_vendedor AS "nome_vendedor",
            pc.telefone AS "telefone_cliente",
            pc.email AS "email_cliente",
            p.notas_contato
        FROM pedidos_pedido p
        LEFT JOIN pessoas_pessoas pc ON p.cliente_id = pc.id
        WHERE p.id = %s  # Alterado de pedido_id para id
    """

    params = [pedido_id]

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        resultado = dictfetchall(cursor)

    if not resultado:
        raise Http404("Pedido não encontrado")

    pedido = resultado[0]

    if request.method == 'POST':
        notas = request.POST.get('notas')
        update_query = """
            UPDATE pedidos_pedido
            SET notas_contato = %s
            WHERE id = %s  # Alterado de pedido_id para id
        """
        with connection.cursor() as cursor:
            cursor.execute(update_query, [notas, pedido_id])

        return redirect('/crm/')

    context = {
        'pedido': pedido,
    }

    return render(request, 'detalhar_contato.html', context)

def dashboard(request):
    vendedor = request.GET.get('vendedor', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    # Obter lista de vendedores
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT vendedor_id, nome_vendedor
            FROM pedidos_pedido
            WHERE status != 'Cancelado'
            ORDER BY nome_vendedor ASC;
        """)
        vendedores = cursor.fetchall()
        vendedores_list = [{'id': vendedor[0], 'nome': vendedor[1]} for vendedor in vendedores]

    # Consulta principal
    query = """
        SELECT 
            nome_vendedor AS "Nome_Vendedor",
            COUNT(*) AS "Total_Pedidos",
            SUM(total) AS "Total_Valor_Pedido"
        FROM 
            pedidos_pedido
        WHERE 
            status != 'Cancelado'
    """

    params = []
    if vendedor:
        query += " AND vendedor_id = %s"
        params.append(vendedor)
    
    if data_inicio:
        query += " AND data >= %s"
        params.append(data_inicio)

    if data_fim:
        query += " AND data <= %s"
        params.append(data_fim)
    
    query += """
        GROUP BY 
            vendedor_id, nome_vendedor
        ORDER BY 
            nome_vendedor ASC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        data = dictfetchall(cursor)

    # Prepare data for the chart
    labels = [item['Nome_Vendedor'] for item in data]
    total_pedidos = [float(item['Total_Pedidos']) for item in data]
    total_valor_pedido = [float(item['Total_Valor_Pedido']) for item in data]

    context = {
        'labels': json.dumps(labels),
        'total_pedidos': json.dumps(total_pedidos),
        'total_valor_pedido': json.dumps(total_valor_pedido),
        'vendedor': vendedor,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'vendedores': vendedores_list
    }

    return render(request, 'dashboard.html', context)


def enviar_emails_inativos(request):
    hoje = date.today()
    
    if request.method == 'GET':
        dias_para_contato = int(request.GET.get('dias', 180))
        data_limite = hoje - timedelta(days=dias_para_contato)
        
        query = """
            SELECT 
                p.cliente_id AS cliente_id,
                pe.email AS email,
                MAX(p.data) AS ultima_compra,
                MAX(p.total) AS total,
                p.nome_cliente AS nome_cliente
            FROM pedidos_pedido p
            JOIN pessoas_pessoas pe ON p.cliente_id = pe.id
            WHERE p.data <= %s
            GROUP BY p.cliente_id, pe.email, p.nome_cliente
                    """
        
        with connection.cursor() as cursor:
            cursor.execute(query, [data_limite])
            rows = cursor.fetchall()
            clientes_inativos = [
                {
                    'cliente_id': row[0],
                    'email': row[1],
                    'ultima_compra': row[2],
                    'total': row[3],
                    'nome_cliente': row[4],
                }
                for row in rows
            ]
        
        context = {
            'clientes_inativos': clientes_inativos,
            'dias_para_contato': dias_para_contato,
        }
        return render(request, 'emails_inativos.html', context)
    
    elif request.method == 'POST':
        clientes_ids = request.POST.getlist('clientes')
        mensagem = request.POST.get('mensagem')
        
        if not clientes_ids or not mensagem:
            return HttpResponseBadRequest("Nenhum cliente selecionado ou mensagem vazia.")
        
        query = """
            SELECT email FROM pessoas_pessoas
            WHERE id IN %s
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query, [tuple(clientes_ids)])
            emails = [row[0] for row in cursor.fetchall()]
        
        send_mail(
            subject='Estamos com saudades!',
            message=mensagem,
            from_email='sistema@empresa.com',
            recipient_list=emails,
        )
        
        return redirect('enviar_emails_inativos')  
    
    return HttpResponseBadRequest("Método inválido.")


def emails(request):
    hoje = date.today()
    dias_para_contato = int(request.GET.get('dias', 180))
    data_limite = hoje - timedelta(days=dias_para_contato)

    query = """
        SELECT 
            DISTINCT 
            p.cliente_id,
            pe.email,
            MAX(p.data) AS ultima_compra,
            p.total AS total
        FROM pedidos_pedido p
        JOIN pessoas_pessoas pe ON p.cliente_id = pe.id
        WHERE p.data <= %s
        GROUP BY p.cliente_id, pe.email
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [data_limite])
        clientes_inativos = cursor.fetchall()

    context = {
        'clientes_inativos': clientes_inativos,
        'data_limite': data_limite,
        'dias_para_contato': dias_para_contato
    }

    return render(request, 'emails_inativos.html', context)


def clientes_inativos_por_ultima_compra(request):
    hoje = date.today()
    dias_para_contato = int(request.GET.get('dias', 180))
    data_limite = hoje - timedelta(days=dias_para_contato)

    query = """
        SELECT 
            p.cliente_id,
            pe.email,
            MAX(p.data) AS ultima_compra,
            p.total AS total
        FROM pedidos_pedido p
        JOIN pessoas_pessoas pe ON p.cliente_id = pe.id
        GROUP BY p.cliente_id, pe.email
        HAVING MAX(p.data) <= %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [data_limite])
        clientes_inativos = cursor.fetchall()

    context = {
        'clientes_inativos': clientes_inativos,
        'dias_para_contato': dias_para_contato,
    }
    return render(request, 'clientes_inativos.html', context)


def emails(request):
    hoje = date.today()
    dias_para_contato = int(request.GET.get('dias', 180))
    data_limite = hoje - timedelta(days=dias_para_contato)

    query = """
        SELECT 
            DISTINCT 
            p.cliente_id,
            pe.email,
            MAX(p.data) AS ultima_compra,
            p.total AS total
        FROM pedidos_pedido p
        JOIN pessoas_pessoas pe ON p.cliente_id = pe.id
        WHERE p.data <= %s
        GROUP BY p.cliente_id, pe.email
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [data_limite])
        clientes_inativos = cursor.fetchall()

    context = {
        'clientes_inativos': clientes_inativos,
        'data_limite': data_limite,
        'dias_para_contato': dias_para_contato
    }

    return render(request, 'emails_inativos.html', context)


def clientes_inativos_por_ultima_compra(request):
    hoje = date.today()
    dias_para_contato = int(request.GET.get('dias', 180))
    data_limite = hoje - timedelta(days=dias_para_contato)

    query = """
        SELECT 
            p.cliente_id,
            pe.email,
            MAX(p.data) AS ultima_compra,
            p.total AS total
        FROM pedidos_pedido p
        JOIN pessoas_pessoas pe ON p.cliente_id = pe.id
        GROUP BY p.cliente_id, pe.email
        HAVING MAX(p.data) <= %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [data_limite])
        clientes_inativos = cursor.fetchall()

    context = {
        'clientes_inativos': clientes_inativos,
        'dias_para_contato': dias_para_contato,
    }
    return render(request, 'clientes_inativos.html', context)