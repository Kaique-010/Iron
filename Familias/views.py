from django.db import IntegrityError, connections
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


def set_empresa_database(empresa):
    db_alias = empresa.database  
    if db_alias not in connections:
        raise IntegrityError(f"Banco de dados {db_alias} não configurado.")
    connections['default'] = connections[db_alias]


class FamiliasListView(ListView):
    model = models.Familia
    template_name = 'familiaslistas.html'
    context_object_name = 'familias'
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



class FamiliaCreateView(CreateView):
    model = models.Familia
    template_name = 'familiascriar.html'
    form_class = forms.Familias
    success_url = reverse_lazy('familiaslistas')

    def form_valid(self, form):
        # Verifica se o usuário está autenticado
        if not self.request.user.is_authenticated:
            return redirect('login')  # Ou redirecionar para a página desejada
        
        # Verifica se o usuário tem uma empresa associada
        if not hasattr(self.request.user, 'empresa') or not self.request.user.empresa:
            raise PermissionDenied("Usuário não associado a uma empresa.")
        
        # Configura a empresa para o formulário
        set_empresa_database(self.request.user.empresa)
        form.instance.empresa = self.request.user.empresa
        
        return super().form_valid(form)

class FamiliaDetailView(DetailView):
    model = models.Familia
    template_name = 'familiasdetalhe.html'

    def get_object(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        return super().get_object()


class FamiliaUpdateView(UpdateView):
    model = models.Familia
    template_name = 'familiaseditar.html'
    form_class = forms.Familias
    success_url = reverse_lazy('familiaslistas')

    def form_valid(self, form):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  
        form.empresa = self.request.user.empresa
        return super().form_valid(form)


class FamiliaDeleteView(DeleteView):
    model = models.Familia
    template_name = 'familiasexcluir.html'
    success_url = reverse_lazy('listas')

    def get_object(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        return super().get_object()
