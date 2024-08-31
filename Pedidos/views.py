from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.forms import inlineformset_factory, formset_factory
from django.core import serializers
from .models import Pedido, ItemPedido
from .forms import ItemPedidoForm, PedidoForm
from Produtos.models import Produtos

ItemPedidoFormSet = inlineformset_factory(Pedido, ItemPedido, form=ItemPedidoForm, extra=1, can_delete=True)

class PedidosListView(ListView):
    model = Pedido
    template_name = 'pedidoslistas.html'
    context_object_name = 'pedidos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        pedido = self.request.GET.get('pedido')
        if pedido:
            queryset = queryset.filter(id__icontains=pedido)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pedidos = self.get_queryset()
        context['contagem_pedidos'] = pedidos.count()
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
