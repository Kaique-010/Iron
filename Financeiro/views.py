from io import BytesIO
from django.db import connection
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import openpyxl
from .models import ContaAPagar, ContaAReceber
from .forms import ContaAPagarForm, ContaAReceberForm, DateRangeForm
from django.shortcuts import render
from django.db.models import Sum
from datetime import date, timedelta
from django.utils.dateparse import parse_date


class ContaAPagarListView(ListView):
    model = ContaAPagar
    template_name = 'conta_a_pagar_list.html'
    context_object_name = 'contas_a_pagar'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        descricao = self.request.GET.get('descricao')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        status = self.request.GET.get('status')

        start_date = parse_date(start_date) if start_date else None
        end_date = parse_date(end_date) if end_date else None

        if descricao:
            queryset = queryset.filter(descricao__icontains=descricao)
        
        if start_date and end_date:
            queryset = queryset.filter(data_emissao__range=(start_date, end_date))
        elif start_date:
            queryset = queryset.filter(data_emissao__gte=start_date)
        elif end_date:
            queryset = queryset.filter(data_emissao__lte=end_date)
        
        if status:
            queryset = queryset.filter(status_pagamento=status == 'True')

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contas = self.get_queryset()
        context['total_contas'] = contas.count()
        context['total_valor'] = contas.aggregate(total_valor=Sum('valor'))['total_valor'] or 0
        return context
    
class ContaAPagarDetailView(DetailView):
    model = ContaAPagar
    template_name = 'conta_a_pagar_detail.html'
    context_object_name = 'conta_a_pagar'
    

class ContaAPagarCreateView(CreateView):
    model = ContaAPagar
    template_name = 'conta_a_pagar_update.html'
    form_class = ContaAPagarForm
    success_url = reverse_lazy('conta_a_pagar_list')

class ContaAPagarUpdateView(UpdateView):
    model = ContaAPagar
    template_name = 'conta_a_pagar_update.html'
    form_class = ContaAPagarForm
    success_url = reverse_lazy('conta_a_pagar_list')

class ContaAPagarDeleteView(DeleteView):
    model = ContaAPagar
    template_name = 'conta_a_pagar_delete.html'
    success_url = reverse_lazy('conta_a_pagar_list')

# Views para ContaAReceber
class ContaAReceberListView(ListView):
    model = ContaAReceber
    template_name = 'conta_a_receber_list.html'
    context_object_name = 'contas_a_receber'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        descricao = self.request.GET.get('descricao')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        status = self.request.GET.get('status')

        start_date = parse_date(start_date) if start_date else None
        end_date = parse_date(end_date) if end_date else None

        if descricao:
            queryset = queryset.filter(descricao__icontains=descricao)
        
        if start_date and end_date:
            queryset = queryset.filter(data_emissao__range=(start_date, end_date))
        elif start_date:
            queryset = queryset.filter(data_emissao__gte=start_date)
        elif end_date:
            queryset = queryset.filter(data_emissao__lte=end_date)
        
        if status:
            queryset = queryset.filter(status_recebimento=status == 'True')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contas = self.get_queryset()
        context['total_contas'] = contas.count()
        context['total_valor'] = contas.aggregate(total_valor=Sum('valor'))['total_valor'] or 0
        return context

class ContaAReceberDetailView(DetailView):
    model = ContaAReceber
    template_name = 'conta_a_receber_detail.html'
    context_object_name = 'conta_a_receber'

class ContaAReceberCreateView(CreateView):
    model = ContaAReceber
    template_name = 'conta_a_receber_update.html'
    form_class = ContaAReceberForm
    success_url = reverse_lazy('conta_a_receber_list')

class ContaAReceberUpdateView(UpdateView):
    model = ContaAReceber
    template_name = 'conta_a_receber_update.html'
    form_class = ContaAReceberForm
    success_url = reverse_lazy('conta_a_receber_list')

class ContaAReceberDeleteView(DeleteView):
    model = ContaAReceber
    template_name = 'conta_a_receber_delete.html'
    success_url = reverse_lazy('conta_a_receber_list')


def totaisapagar(request):
    contas = ContaAPagar.objects.all()
    total_contas = contas.count()
    total_valor = contas.aggregate(total_valor=Sum('valor'))['total_valor'] or 0
    
    context = {
        'total_contas': total_contas,
        'total_valor': total_valor
    }
    
    return render(request, 'conta_a_pagar_list.html', context)


def fluxo_caixa(request):
    # Período padrão (últimos 30 dias)
    start_date = date.today() - timedelta(days=30)
    end_date = date.today()
    
    if request.method == 'GET':
        form = DateRangeForm(request.GET)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
    else:
        form = DateRangeForm(initial={'start_date': start_date, 'end_date': end_date})

    # Filtrar contas a receber e a pagar no período
    entradas = ContaAReceber.objects.filter(
        data_vencimento__range=[start_date, end_date]
    ).aggregate(total_entradas=Sum('valor'))['total_entradas'] or 0

    saidas = ContaAPagar.objects.filter(
        data_vencimento__range=[start_date, end_date]
    ).aggregate(total_saidas=Sum('valor'))['total_saidas'] or 0

    saldo_inicial = 0  # Ajuste conforme necessário
    saldo_final = saldo_inicial + entradas - saidas

    context = {
        'form': form,
        'saldo_inicial': saldo_inicial,
        'entradas': entradas,
        'saidas': saidas,
        'saldo_final': saldo_final,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'fluxo_caixa.html', context)



def dash(request):
    start_date = date.today() - timedelta(days=30)
    end_date = date.today()

    # Verifica se o formulário foi enviado e se as datas são válidas
    if request.method == 'GET' and 'start_date' in request.GET and 'end_date' in request.GET:
        form = DateRangeForm(request.GET)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
    else:
        form = DateRangeForm(initial={'start_date': start_date, 'end_date': end_date})

    # Calcula o total de entradas
    entradas = ContaAReceber.objects.filter(
        data_vencimento__range=[start_date, end_date]
    ).aggregate(total_entradas=Sum('valor'))['total_entradas'] or 0

    # Calcula o total de saídas
    saidas = ContaAPagar.objects.filter(
        data_vencimento__range=[start_date, end_date]
    ).aggregate(total_saidas=Sum('valor'))['total_saidas'] or 0

    saldo_inicial = 1  

       
    saldo = entradas - saidas

    context = {
        'form': form,
        'financeiro_dash': {
            'saldo_inicial': saldo_inicial,
            'entradas': entradas,
            'saidas': saidas,
            'saldo': saldo,
            'start_date': start_date,
            'end_date': end_date,
            
        }
    }

    return render(request, 'dash.html', context)




def exportar_contaapagar_excel(request):
    # Cria uma planilha do Excel
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Contas a Pagar'


    columns = ['Documento', 'Descrição', 'Valor', 'Emissão', 'Vencimento', 'Status', 'Categoria', 'Forma de Pagamento']
    worksheet.append(columns)

    contas = ContaAPagar.objects.all()  
    for conta in contas:
        worksheet.append([
            conta.documento,
            conta.descricao,
            conta.valor,
            conta.data_emissao.strftime('%d/%m/%Y') if conta.data_emissao else '',  
            conta.data_vencimento.strftime('%d/%m/%Y') if conta.data_vencimento else '',  
            conta.status_pagamento,
            str(conta.categorias),
            str(conta.forma_pagamento),
        ])
   
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=contas_a_pagar.xlsx'  # Nome do arquivo atualizado
    return response


def exportar_contaareceber_excel(request):
    
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Contas a Receber'

    # Define o cabeçalho
    columns = ['Documento', 'Descrição', 'Valor', 'Emissão', 'Vencimento', 'Status', 'Categoria', 'Forma de Recebimento']
    worksheet.append(columns)

    
    contas = ContaAReceber.objects.all() 
    for conta in contas:
        worksheet.append([
            conta.documento,
            conta.descricao,
            conta.valor,
            conta.data_emissao.strftime('%d/%m/%Y') if conta.data_emissao else '',
            conta.data_vencimento.strftime('%d/%m/%Y') if conta.data_vencimento else '',  
            conta.status_recebimento, 
            str(conta.categorias),
            str(conta.forma_recebimento)
        ])
   
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=contas_a_receber.xlsx'  
    return response
