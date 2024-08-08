from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from .models import Produtos
from django.urls import reverse_lazy
from django.shortcuts import render
from django.db.models import Sum

class ProdutosListView(ListView):
    model = models.Produtos
    template_name = 'produtoslistas.html'
    context_object_name = 'produtos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.GET.get('nome')
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produtos = self.get_queryset()
        context['contagem_produtos'] = produtos.count()
        context['total_saldo'] = produtos.aggregate(total_saldo=Sum('quantidade'))['total_saldo'] or 0
        context['total_preco_vista'] = sum(preco.preco_venda_vista for produto in produtos for preco in produto.precos.all())
        context['total_preco_prazo'] = sum(preco.preco_venda_prazo for produto in produtos for preco in produto.precos.all())
        return context

class ProdutosCreateView(CreateView):
    model = models.Produtos
    template_name = 'produtoscriar.html'
    form_class = forms.Produtos
    success_url = reverse_lazy('produtoslistas')

class ProdutosDetailView(DetailView):
    model = models.Produtos
    template_name = 'produtosdetalhe.html'

class ProdutosUpdateView(UpdateView):
    model = models.Produtos
    form_class = forms.Produtos
    template_name = 'produtoseditar.html'
    success_url = reverse_lazy('produtoslistas')

class ProdutosDeleteView(DeleteView):
    model = models.Produtos
    template_name = 'produtosexcluir.html'
    success_url = reverse_lazy('produtoslistas')
