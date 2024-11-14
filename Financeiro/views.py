from io import BytesIO
from django.db import IntegrityError, connection, connections
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import openpyxl
from .models import ContaAPagar, ContaAReceber, FormasPagamento, FormasRecebimento, Categorias
from .forms import ContaAPagarForm, ContaAReceberForm, DateRangeForm, CategoriaForm, FormasPagamentoForm, FormasRecebimentoForm
from django.shortcuts import redirect, render
from django.db.models import Sum
from datetime import date, timedelta
from django.utils.dateparse import parse_date


def set_empresa_database(empresa):
    db_alias = empresa.database  
    if db_alias not in connections:
        raise IntegrityError(f"Banco de dados {db_alias} não configurado.")
    connections['default'] = connections[db_alias]



class EmpresaBaseView:
    """
    Classe base para configurar a empresa e banco de dados de cada view.
    """
    def set_empresa(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        set_empresa_database(self.request.user.empresa)


class ContaAPagarListView(EmpresaBaseView, ListView):
    model = ContaAPagar
    template_name = 'conta_a_pagar_list.html'
    context_object_name = 'contas_a_pagar'
    paginate_by = 10

    def get_queryset(self):
        self.set_empresa()  # Configura o banco de dados
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


class ContaAPagarDetailView(EmpresaBaseView, DetailView):
    model = ContaAPagar
    template_name = 'conta_a_pagar_detail.html'
    context_object_name = 'conta_a_pagar'

    def get_object(self):
        self.set_empresa()  # Configura o banco de dados
        return super().get_object()


class ContaAPagarCreateView(EmpresaBaseView, CreateView):
    model = ContaAPagar
    template_name = 'conta_a_pagar_update.html'
    form_class = ContaAPagarForm
    success_url = reverse_lazy('conta_a_pagar_list')

    def form_valid(self, form):
        
        if not self.request.user.is_authenticated:
            return redirect('login')  # Ou redirecionar para a página desejada
        
        
        if not hasattr(self.request.user, 'empresa') or not self.request.user.empresa:
            raise PermissionDenied("Usuário não associado a uma empresa.")
        
        
        set_empresa_database(self.request.user.empresa)
        form.instance.empresa = self.request.user.empresa
        
        return super().form_valid(form)

class ContaAPagarUpdateView(EmpresaBaseView, UpdateView):
    model = ContaAPagar
    template_name = 'conta_a_pagar_update.html'
    form_class = ContaAPagarForm
    success_url = reverse_lazy('conta_a_pagar_list')

    def form_valid(self, form):
        
        if not self.request.user.is_authenticated:
            return redirect('login')  # Ou redirecionar para a página desejada
        
        
        if not hasattr(self.request.user, 'empresa') or not self.request.user.empresa:
            raise PermissionDenied("Usuário não associado a uma empresa.")
        
        
        set_empresa_database(self.request.user.empresa)
        form.instance.empresa = self.request.user.empresa
        
        return super().form_valid(form)


class ContaAPagarDeleteView(EmpresaBaseView, DeleteView):
    model = ContaAPagar
    template_name = 'conta_a_pagar_delete.html'
    success_url = reverse_lazy('conta_a_pagar_list')

    def get_object(self):
        self.set_empresa()  # Configura o banco de dados
        return super().get_object()




class ContaAReceberListView(EmpresaBaseView, ListView):
    model = ContaAReceber
    template_name = 'conta_a_receber_list.html'
    context_object_name = 'contas_a_receber'
    paginate_by = 10

    def get_queryset(self):
        self.set_empresa()  # Configura o banco de dados
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


class ContaAReceberDetailView(EmpresaBaseView, DetailView):
    model = ContaAReceber
    template_name = 'conta_a_receber_detail.html'
    context_object_name = 'conta_a_receber'

    def get_object(self):
        self.set_empresa()  # Configura o banco de dados
        return super().get_object()


class ContaAReceberCreateView(EmpresaBaseView, CreateView):
    model = ContaAReceber
    template_name = 'conta_a_receber_update.html'
    form_class = ContaAReceberForm
    success_url = reverse_lazy('conta_a_receber_list')

    def form_valid(self, form):
        
        if not self.request.user.is_authenticated:
            return redirect('login')  # Ou redirecionar para a página desejada
        
        
        if not hasattr(self.request.user, 'empresa') or not self.request.user.empresa:
            raise PermissionDenied("Usuário não associado a uma empresa.")
        
        
        set_empresa_database(self.request.user.empresa)
        form.instance.empresa = self.request.user.empresa
        
        return super().form_valid(form)


class ContaAReceberUpdateView(EmpresaBaseView, UpdateView):
    model = ContaAReceber
    template_name = 'conta_a_receber_update.html'
    form_class = ContaAReceberForm
    success_url = reverse_lazy('conta_a_receber_list')

    def form_valid(self, form):
        
        if not self.request.user.is_authenticated:
            return redirect('login')  # Ou redirecionar para a página desejada
        
        
        if not hasattr(self.request.user, 'empresa') or not self.request.user.empresa:
            raise PermissionDenied("Usuário não associado a uma empresa.")
        
        
        set_empresa_database(self.request.user.empresa)
        form.instance.empresa = self.request.user.empresa
        
        return super().form_valid(form)


class ContaAReceberDeleteView(EmpresaBaseView, DeleteView):
    model = ContaAReceber
    template_name = 'conta_a_receber_delete.html'
    success_url = reverse_lazy('conta_a_receber_list')

    def get_object(self):
        self.set_empresa()  # Configura o banco de dados
        return super().get_object()
    


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



class FormaRecebimentoListView(EmpresaBaseView, ListView):
    model = FormasRecebimento
    template_name = 'formas_recebimento_list.html'
    context_object_name = 'formas_recebimento'
    paginate_by = 10

    def get_queryset(self):
        self.set_empresa() 
        queryset = super().get_queryset()
        descricao = self.request.GET.get('descricao')
        
        if descricao:
            queryset = queryset.filter(descricao__icontains=descricao)
        
        return queryset


class FormaRecebimentoDetailView(EmpresaBaseView, DetailView):
    model = FormasRecebimento
    template_name = 'formas_recebimento_detail.html'
    context_object_name = 'forma_recebimento'

    def get_object(self):
        self.set_empresa()  # Configura o banco de dados
        return super().get_object()


class FormaRecebimentoCreateView(EmpresaBaseView, CreateView):
    model = FormasRecebimento
    template_name = 'formas_recebimento_form.html'
    form_class = FormasRecebimentoForm
    success_url = reverse_lazy('formas_recebimento_list')

    def form_valid(self, form):
        
        if not self.request.user.is_authenticated:
            return redirect('login')  # Ou redirecionar para a página desejada
        
        
        if not hasattr(self.request.user, 'empresa') or not self.request.user.empresa:
            raise PermissionDenied("Usuário não associado a uma empresa.")
        
        
        set_empresa_database(self.request.user.empresa)
        form.instance.empresa = self.request.user.empresa
        form.instance.user = self.request.user
        
        return super().form_valid(form)


class FormaRecebimentoUpdateView(EmpresaBaseView, UpdateView):
    model = FormasRecebimento
    template_name = 'formas_recebimento_form.html'
    form_class = FormasRecebimentoForm
    success_url = reverse_lazy('forma_recebimento_list')

    def form_valid(self, form):
        
        if not self.request.user.is_authenticated:
            return redirect('login')  # Ou redirecionar para a página desejada
        
        
        if not hasattr(self.request.user, 'empresa') or not self.request.user.empresa:
            raise PermissionDenied("Usuário não associado a uma empresa.")
        
        
        set_empresa_database(self.request.user.empresa)
        form.instance.empresa = self.request.user.empresa
        
        return super().form_valid(form)


class FormaRecebimentoDeleteView(EmpresaBaseView, DeleteView):
    model = FormasRecebimento
    template_name = 'formas_recebimento_confirm_delete.html'
    success_url = reverse_lazy('forma_recebimento_list')



class FormaPagamentoListView(EmpresaBaseView, ListView):
    model = FormasPagamento
    template_name = 'formas_pagamento_list.html'
    context_object_name = 'formas_pagamento'
    paginate_by = 10

    def get_queryset(self):
        self.set_empresa()  
        queryset = super().get_queryset()
        descricao = self.request.GET.get('descricao')
        
        if descricao:
            queryset = queryset.filter(descricao__icontains=descricao)
        
        return queryset


class FormaPagamentoDetailView(EmpresaBaseView, DetailView):
    model = FormasPagamento
    template_name = 'formas_pagamento_detail.html'
    context_object_name = 'forma_pagamento'

    def get_object(self):
        self.set_empresa()  
        return super().get_object()


class FormaPagamentoCreateView(EmpresaBaseView, CreateView):
    model = FormasPagamento
    form_class = FormasPagamentoForm
    template_name = 'formas_pagamento_form.html'
    success_url = reverse_lazy('formas_pagamento_list')

    def form_valid(self, form):
        
        if not self.request.user.is_authenticated:
            return redirect('login')  # Ou redirecionar para a página desejada
        
        
        if not hasattr(self.request.user, 'empresa') or not self.request.user.empresa:
            raise PermissionDenied("Usuário não associado a uma empresa.")
        
        
        set_empresa_database(self.request.user.empresa)
        form.instance.empresa = self.request.user.empresa
        form.instance.user = self.request.user
        
        return super().form_valid(form)


class FormaPagamentoUpdateView(EmpresaBaseView, UpdateView):
    model = FormasPagamento
    form_class = FormasPagamentoForm
    template_name = 'formas_pagamento_form.html'
    success_url = reverse_lazy('formas_pagamento_list')

    def form_valid(self, form):
        
        if not self.request.user.is_authenticated:
            return redirect('login')  # Ou redirecionar para a página desejada
        
        
        if not hasattr(self.request.user, 'empresa') or not self.request.user.empresa:
            raise PermissionDenied("Usuário não associado a uma empresa.")
        
        
        set_empresa_database(self.request.user.empresa)
        form.instance.empresa = self.request.user.empresa
        
        return super().form_valid(form)


class FormaPagamentoDeleteView(EmpresaBaseView, DeleteView):
    model = FormasPagamento
    template_name = 'formas_pagamento_confirm_delete.html'
    success_url = reverse_lazy('formas_pagamento_list')


class CategoriaListView(EmpresaBaseView, ListView):
    model = Categorias
    template_name = 'categorias_list.html'
    context_object_name = 'categorias'
    paginate_by = 10

    def get_queryset(self):
        self.set_empresa()  # Configura o banco de dados
        queryset = super().get_queryset()
        descricao = self.request.GET.get('descricao')
        
        if descricao:
            queryset = queryset.filter(descricao__icontains=descricao)
        
        return queryset


class CategoriaDetailView(EmpresaBaseView, DetailView):
    model = Categorias
    template_name = 'categorias_detail.html'
    context_object_name = 'categoria'

    def get_object(self):
        self.set_empresa()  
        return super().get_object()


class CategoriaCreateView(EmpresaBaseView, CreateView):
    model = Categorias
    template_name = 'categorias_form.html'
    form_class = CategoriaForm
    success_url = reverse_lazy('categorias_list')

    def form_valid(self, form):
        
        if not self.request.user.is_authenticated:
            return redirect('login')  # Ou redirecionar para a página desejada
        
        
        if not hasattr(self.request.user, 'empresa') or not self.request.user.empresa:
            raise PermissionDenied("Usuário não associado a uma empresa.")
        
        
        set_empresa_database(self.request.user.empresa)
        form.instance.empresa = self.request.user.empresa
        form.instance.user = self.request.user
        
        return super().form_valid(form)


class CategoriaUpdateView(EmpresaBaseView, UpdateView):
    model = Categorias
    template_name = 'categorias_form.html'
    form_class = CategoriaForm
    success_url = reverse_lazy('categorias_list')

    def form_valid(self, form):
        
        if not self.request.user.is_authenticated:
            return redirect('login')  # Ou redirecionar para a página desejada
        
        
        if not hasattr(self.request.user, 'empresa') or not self.request.user.empresa:
            raise PermissionDenied("Usuário não associado a uma empresa.")
        
        
        set_empresa_database(self.request.user.empresa)
        form.instance.empresa = self.request.user.empresa
        
        return super().form_valid(form)


class CategoriaDeleteView(EmpresaBaseView, DeleteView):
    model = Categorias
    template_name = 'categorias_confirm_delete.html'
    success_url = reverse_lazy('categorias_list')



