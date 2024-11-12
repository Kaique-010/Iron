from django.db import IntegrityError, connections
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from django.urls import reverse_lazy


# Função para configurar o banco de dados com base na empresa
def set_empresa_database(empresa):
    db_alias = empresa.database  
    if db_alias not in connections:
        raise IntegrityError(f"Banco de dados {db_alias} não configurado.")
    connections['default'] = connections[db_alias]


class EntradasListView(ListView):
    model = models.Entrada_Produtos
    template_name = 'entradaslistas.html'
    context_object_name = 'entradas'
    paginate_by = 5

    def get_queryset(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        
        queryset = super().get_queryset()
        produto = self.request.GET.get('produto')
    
        if produto:
            queryset = queryset.filter(produto__nome__icontains=produto)
        
        return queryset


class EntradasCreateView(CreateView):
    model = models.Entrada_Produtos
    template_name = 'entradascriar.html'
    form_class = forms.Entradas
    success_url = reverse_lazy('entradaslistas')

    def form_valid(self, form):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        return super().form_valid(form)


class EntradasDetailView(DetailView):
    model = models.Entrada_Produtos
    template_name = 'entradasdetalhe.html'

    def get_object(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        return super().get_object()


class EntradasUpdateView(UpdateView):
    model = models.Entrada_Produtos
    template_name = 'entradaseditar.html'
    form_class = forms.Entradas
    success_url = reverse_lazy('entradaslistas')

    def form_valid(self, form):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        return super().form_valid(form)


class EntradasDeleteView(DeleteView):
    model = models.Entrada_Produtos
    template_name = 'entradasexcluir.html'
    success_url = reverse_lazy('entradaslistas')

    def get_object(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        return super().get_object()
