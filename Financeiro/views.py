from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import ContaAPagar, ContaAReceber
from .forms import ContaAPagarForm, ContaAReceberForm, DateRangeForm
from django.shortcuts import render
from django.db.models import Sum
from datetime import date, timedelta


# Views para ContaAPagar
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

    # Verificar se o formulário foi enviado
    if request.method == 'GET':
        form = DateRangeForm(request.GET)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

    else:
        form = DateRangeForm(initial={'start_date': start_date, 'end_date': end_date})

    # Filtrar contas a receber e a pagar no período
    entradas = ContaAReceber.objects.filter(
        data_recebimento__range=[start_date, end_date],
        status_recebimento=True
    ).aggregate(total_entradas=Sum('valor'))['total_entradas'] or 0

    saidas = ContaAPagar.objects.filter(
        data_pagamento__range=[start_date, end_date],
        status_pagamento=True
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


def contas_a_receber(request):
    filter_params = {}
    status = request.GET.get('status')
    if status:
        filter_params['status_recebimento'] = status
    
    
    contas = ContaAReceber.objects.filter(**filter_params)

    sort_by = request.GET.get('sort_by', 'data_emissao') 
    contas = contas.order_by(sort_by)
    print(f"Ordenando por: {sort_by}")

    return render(request, 'conta_a_receber_list', {'contas': contas})



def contas_a_pagar(request):
    filter_params = {}
    
    status = request.GET.get('status')
    if status:
        filter_params['status_pagamento'] = status

    contas = ContaAPagar.objects.filter(**filter_params)
    sort_by = request.GET.get('sort_by', 'data_emissao')
    contas = contas.order_by(sort_by)
    print(f"Ordenando por: {sort_by}")

    return render(request, 'conta_a_pagar_list', {'contas': contas})
