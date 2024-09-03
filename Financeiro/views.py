from django.db import connection
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import ContaAPagar, ContaAReceber
from .forms import ContaAPagarForm, ContaAReceberForm, DateRangeForm
from django.shortcuts import render
from django.db.models import Sum
from datetime import date, timedelta


class ContaAPagarListView(ListView):
    model = ContaAPagar
    template_name = 'conta_a_pagar_list.html'
    context_object_name = 'contas_a_pagar'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        descricao = self.request.GET.get('descricao')

        if descricao:
            queryset = queryset.filter(descricao__icontains=descricao)

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

        if descricao:
            queryset = queryset.filter(descricao__icontains=descricao)

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