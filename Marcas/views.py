from django.db import IntegrityError, connections
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from django.urls import reverse_lazy



def set_empresa_database(empresa):
    db_alias = empresa.database  
    if db_alias not in connections:
        raise IntegrityError(f"Banco de dados {db_alias} não configurado.")
    connections['default'] = connections[db_alias]
    
    
class MarcasListView(ListView):
    model = models.Marcas
    template_name = 'marcaslistas.html'
    context_object_name = 'marcas'
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

class MarcasCreateView(CreateView):
    model = models.Marcas
    template_name = 'marcascriar.html'
    form_class = forms.Marcas
    success_url = reverse_lazy('marcaslistas')
    
    def form_valid(self, form):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

class MarcasDetailView(DetailView):
    model = models.Marcas
    template_name = 'marcasdetalhe.html'

    def get_object(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        return super().get_object()



class MarcasUpdateView(UpdateView):
    model = models.Marcas
    template_name = 'marcaseditar.html'
    form_class = forms.Marcas
    success_url = reverse_lazy('marcaslistas')
    
    def form_valid(self, form):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  
        form.empresa = self.request.user.empresa
        return super().form_valid(form)



class MarcasDeleteView(DeleteView):
    model = models.Marcas
    template_name = 'marcasexcluir.html'
    success_url = reverse_lazy('marcaslistas')


    def get_object(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        return super().get_object()



    
