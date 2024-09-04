from datetime import date, timedelta
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.forms import inlineformset_factory, formset_factory
from django.core import serializers
from Financeiro.forms import DateRangeForm
from .models import Pedido, ItemPedido
from .forms import ItemPedidoForm, PedidoForm
from Produtos.models import Produtos
from django import forms
from django.views.generic.edit import FormMixin
from django.db.models import Sum
import openpyxl
from io import BytesIO
from django.http import HttpResponse




ItemPedidoFormSet = inlineformset_factory(Pedido, ItemPedido, form=ItemPedidoForm, extra=1, can_delete=True)

class PedidosListView(FormMixin, ListView):
    model = Pedido
    template_name = 'pedidoslistas.html'
    context_object_name = 'pedidos'
    paginate_by = 10
    form_class = DateRangeForm

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
            queryset = queryset.filter(data__gte=start_date)
        if end_date:
            queryset = queryset.filter(data__lte=end_date)
    
        return queryset

    def get_form(self, form_class=None):
        form_class = self.get_form_class()
        start_date = date.today() - timedelta(days=30)
        end_date = date.today()
        if self.request.method == 'GET':
            form = form_class(self.request.GET)
            if form.is_valid():
                start_date = form.cleaned_data.get('start_date', start_date)
                end_date = form.cleaned_data.get('end_date', end_date)
        else:
            form = form_class(initial={'start_date': start_date, 'end_date': end_date})
        
        # Formatar as datas aqui
        self.formatted_start_date = start_date.strftime('%d/%m/%Y')
        self.formatted_end_date = end_date.strftime('%d/%m/%Y')
        
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pedidos = self.get_queryset()
        context['contagem_pedidos'] = pedidos.count()
        context['valor_total'] = pedidos.aggregate(total_value=Sum('total'))['total_value'] or 0
        context['form'] = self.get_form()
        context['start_date'] = self.formatted_start_date
        context['end_date'] = self.formatted_end_date
        return context

    

def novo_pedido(request):
    ItemPedidoFormSet = formset_factory(ItemPedidoForm, extra=1)
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        formset = ItemPedidoFormSet(request.POST, prefix='items')
        if form.is_valid() and formset.is_valid():
            pedido = form.save()
            for item_form in formset:
                item = item_form.save(commit=False)
                item.pedido = pedido
                item.save()
            return redirect('pedidoslistas')
    else:
        form = PedidoForm()
        formset = ItemPedidoFormSet(prefix='items')

    produtos = Produtos.objects.all()
    produtos_json = serializers.serialize('json', produtos, fields=('id', 'nome'))

    return render(request, 'pedidoscriar.html', {
        'form': form,
        'formset': formset,
        'produtos_json': produtos_json,
    })



class PedidosCreateView(CreateView):
    model = Pedido
    template_name = 'pedidoscriar.html'
    form_class = PedidoForm
    success_url = reverse_lazy('pedidoslistas')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ItemPedidoFormSet(self.request.POST, instance=self.object)
        else:
            data['formset'] = ItemPedidoFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class PedidosUpdateView(UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedidoseditar.html'
    success_url = reverse_lazy('pedidoslistas')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ItemPedidoFormSet(self.request.POST, instance=self.object)
        else:
            data['formset'] = ItemPedidoFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


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


def total_pedidos(request):
    # Calcula o total de pedidos
    total_pedidos = Pedido.objects.all()  # Obtenha todos os pedidos
    total_count = total_pedidos.count()  # Contagem total de pedidos
    total_value = total_pedidos.aggregate(total_value=Sum('total'))['total_value'] or 0  # Soma total dos valores dos pedidos

    context = {
        'total_count': total_count,
        'total_value': total_value,
    }

    return render(request, 'pedidoslistas.html', context)


def exportar_pedidos_excel(request):
    # Cria uma planilha do Excel
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Pedidos'

    # Define o cabeçalho
    columns = ['Nº Pedido', 'Data', 'Cliente', 'Total Pedido', 'Vendedor']
    worksheet.append(columns)

    # Adiciona os dados
    pedidos = Pedido.objects.all()
    for pedido in pedidos:
        worksheet.append([
            pedido.numero_pedido,
            pedido.data.strftime('%d/%m/%Y'),
            pedido.cliente.nome if pedido.cliente else '',
            pedido.total,
            pedido.nome_vendedor
        ])
   
    # Cria uma nova aba para Itens dos Pedidos
    worksheet_itens = workbook.create_sheet(title='Itens dos Pedidos')
    
    # Define o cabeçalho para Itens dos Pedidos
    columns_itens = ['Nº Pedido', 'Item', 'Quantidade', 'Preço Unitário', 'Subtotal']
    worksheet_itens.append(columns_itens)

    # Adiciona os dados dos Itens dos Pedidos
    itens_pedidos = ItemPedido.objects.select_related('pedido').all()
    for item in itens_pedidos:
        worksheet_itens.append([
            item.pedido.numero_pedido,
            item.produto.nome,  # Presumindo que há um campo `produto` em ItemPedido com um atributo `nome`
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
