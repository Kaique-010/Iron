from django.db import IntegrityError, connections
from django.core.mail import send_mail
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from app import settings
from . import models, forms
from .models import Produtos
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.shortcuts import redirect
from django.db import IntegrityError
from django.db.models import Sum


def set_empresa_database(empresa):
    db_alias = empresa.database  
    if db_alias not in connections:
        raise IntegrityError(f"Banco de dados {db_alias} não configurado.")
    connections['default'] = connections[db_alias]


class ProdutosListView(ListView):
    model = models.Produtos
    template_name = 'produtoslistas.html'
    context_object_name = 'produtos'
    paginate_by = 10

    def get_queryset(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  
        
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['precos_form'] = forms.PrecosForm(self.request.POST)
        else:
            context['precos_form'] = forms.PrecosForm()
        return context

    def form_valid(self, form):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)
        form.instance.empresa = self.request.user.empresa

        context = self.get_context_data()
        precos_form = context['precos_form']

        if form.is_valid() and precos_form.is_valid():
            self.object = form.save()
            
            preco = precos_form.save(commit=False)
            preco.produto = self.object
            preco.clean()  
            preco.save()
            
            return redirect(self.success_url)
        
        return self.form_invalid(form)

class ProdutosDetailView(DetailView):
    model = models.Produtos
    template_name = 'produtosdetalhe.html'

    def get_object(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        return super().get_object()


class ProdutosUpdateView(UpdateView):
    model = models.Produtos
    form_class = forms.Produtos
    template_name = 'produtoseditar.html'
    success_url = reverse_lazy('produtoslistas')

    def form_valid(self, form):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        return super().form_valid(form)


class ProdutosDeleteView(DeleteView):
    model = models.Produtos
    template_name = 'produtosexcluir.html'
    success_url = reverse_lazy('produtoslistas')

    def get_object(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        return super().get_object()
    


class UnidadesListView(ListView):
    model = models.UnidadeMedida
    form_class = forms.Unidades
    template_name = 'unidadeslistas.html'
    context_object_name = 'unidades'
    paginate_by = 10

    def get_queryset(self):
        set_empresa_database(self.request.user.empresa)  # Configura o banco com base na empresa do usuário
        
        queryset = super().get_queryset()
        descricao = self.request.GET.get('descricao')
        
        if descricao:
            queryset = queryset.filter(descricao__icontains=descricao)
        
        return queryset



class UnidadesCreateView(CreateView):
    model = models.UnidadeMedida
    template_name = 'unidadescriar.html'
    form_class = forms.Unidades
    success_url = reverse_lazy('unidadeslistas')

    def form_valid(self, form):
       
        if not self.request.user.is_authenticated:
            return redirect('login') 
        
        
        if not hasattr(self.request.user, 'empresa') or not self.request.user.empresa:
            raise PermissionDenied("Usuário não associado a uma empresa.")
        
        
        set_empresa_database(self.request.user.empresa)
        form.instance.empresa = self.request.user.empresa
        
        return super().form_valid(form)



class UnidadesUpdateView(UpdateView):
    model = models.UnidadeMedida
    template_name = 'unidadescriar.html'
    form_class = forms.Unidades
    success_url = reverse_lazy('unidadeslistas')

    def form_valid(self, form):
       
        if not self.request.user.is_authenticated:
            return redirect('login') 
        
        
        if not hasattr(self.request.user, 'empresa') or not self.request.user.empresa:
            raise PermissionDenied("Usuário não associado a uma empresa.")
        
        
        set_empresa_database(self.request.user.empresa)
        form.instance.empresa = self.request.user.empresa
        
        return super().form_valid(form)



class UnidadesDeleteView(DeleteView):
    model = models.UnidadeMedida
    template_name = 'unidadesexcluir.html'
    success_url = reverse_lazy('unidadeslistas')

    def get_object(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa) 
        return super().get_object()
    


def aviso_estoque_baixo():
    produtos_estoque_baixo = []

    # Verificar se algum produto está com estoque abaixo do mínimo
    for produto in Produtos.objects.all():
        if produto.quantidade <= produto.estoque_minimo:
            produtos_estoque_baixo.append(produto)
    
    # Se houver produtos com estoque baixo, enviar o alerta
    if produtos_estoque_baixo:
        for produto in produtos_estoque_baixo:
            # Criar a mensagem do e-mail
            subject = f'Alerta de Estoque Baixo: {produto.nome}'
            message = f'O estoque do produto {produto.nome} está abaixo do mínimo estabelecido. Quantidade atual: {produto.quantidade}.'
            recipient_list = ['responsavel@empresa.com']  # Coloque os e-mails dos responsáveis aqui
            
            # Enviar o e-mail
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

