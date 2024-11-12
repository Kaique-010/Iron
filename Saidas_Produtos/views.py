from django.db import IntegrityError, connections
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from django.urls import reverse_lazy


def set_empresa_database(empresa):
    db_alias = empresa.database  
    if db_alias not in connections:
        raise IntegrityError(f"Banco de dados {db_alias} não configurado.")
    connections['default'] = connections[db_alias]


class SaidasListView(ListView):
    model = models.Saida_Produtos
    template_name = 'saidaslistas.html'
    context_object_name = 'saidas'
    paginate_by = 10

    def get_queryset(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  
        
        queryset = super().get_queryset()
        produto = self.request.GET.get('produto')

        if produto:
            queryset = queryset.filter(produto__nome__icontains=produto)

        return queryset

class SaidasCreateView(CreateView):
    model = models.Saida_Produtos
    template_name = 'saidascriar.html'
    form_class = forms.Saidas
    success_url = reverse_lazy('saidaslistas')
    
    def form_valid(self, form):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa) 
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

class SaidasDetailView(DetailView):
    model = models.Saida_Produtos
    template_name = 'saidasdetalhe.html'

    def get_object(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        return super().get_object()

class SaidasUpdateView(UpdateView):
    model = models.Saida_Produtos
    template_name = 'saidaseditar.html'
    form_class = forms.Saidas
    success_url = reverse_lazy('saidaslistas')
    
    def form_valid(self, form):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)



class SaidasDeleteView(DeleteView):
    model = models.Saida_Produtos
    template_name = 'saidasexcluir.html'
    success_url = reverse_lazy('saidaslistas')


    def get_object(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        return super().get_object()



    
