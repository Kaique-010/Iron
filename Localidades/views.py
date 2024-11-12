from django.db import IntegrityError, connections
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from django.urls import reverse_lazy


def set_empresa_database(empresa):
    db_alias = empresa.database  
    if db_alias not in connections:
        raise IntegrityError(f"Banco de dados {db_alias} não configurado.")
    connections['default'] = connections[db_alias]

class LocalidadesListView(ListView):
    model = models.Localidade
    template_name = 'localidadeslistas.html'
    context_object_name = 'localidades'
    paginate_by = 5

    def get_queryset(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  
        
        queryset = super().get_queryset()
        nome = self.request.GET.get('nome')

        if nome:
            queryset = queryset.filter(nome__icontains=nome)

        return queryset

class LocalidadesCreateView(CreateView):
    model = models.Localidade
    template_name = 'localidadescriar.html'
    form_class = forms.Localidades
    success_url = reverse_lazy('localidadeslistas')
    
    def form_valid(self, form):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        return super().form_valid(form)

class LocalidadesDetailView(DetailView):
    model = models.Localidade
    template_name = 'localidadesdetalhe.html'

    def get_object(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        return super().get_object()

class LocalidadesUpdateView(UpdateView):
    model = models.Localidade
    template_name = 'localidadeseditar.html'
    form_class = forms.Localidades
    success_url = reverse_lazy('localidadeslistas')

    def form_valid(self, form):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        return super().form_valid(form)

class LocalidadesDeleteView(DeleteView):
    model = models.Localidade
    template_name = 'localidadesexcluir.html'
    success_url = reverse_lazy('localidadeslistas')

    def get_object(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        return super().get_object()



    
