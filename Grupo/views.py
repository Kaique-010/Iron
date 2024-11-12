from django.db import IntegrityError, connections
from rest_framework import generics
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms, serializers
from django.urls import reverse_lazy



def set_empresa_database(empresa):
    db_alias = empresa.database  
    if db_alias not in connections:
        raise IntegrityError(f"Banco de dados {db_alias} não configurado.")
    connections['default'] = connections[db_alias]


class GruposListView(ListView):
    model = models.Grupo
    template_name = 'gruposlistas.html'
    context_object_name = 'Grupos'
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

class GruposCreateView(CreateView):
    model = models.Grupo
    template_name = 'gruposcriar.html'
    form_class = forms.Grupos
    success_url = reverse_lazy('gruposlistas')
    
    def form_valid(self, form):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

class GruposDetailView(DetailView):
    model = models.Grupo
    template_name = 'gruposdetalhe.html'
    
    def get_object(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        return super().get_object()


class GruposUpdateView(UpdateView):
    model = models.Grupo
    template_name = 'gruposeditar.html'
    form_class = forms.Grupos
    success_url = reverse_lazy('gruposlistas')

    
    def form_valid(self, form):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        form.empresa = self.request.user.empresa
        return super().form_valid(form)


class GruposDeleteView(DeleteView):
    model = models.Grupo
    template_name = 'gruposexcluir.html'
    success_url = reverse_lazy('gruposlistas')
    
    def get_object(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
        set_empresa_database(self.request.user.empresa)  # Configura o banco de dados
        
        return super().get_object()


class GruposCreateListAPIView(generics.ListCreateAPIView):
    queryset = models.Grupo.objects.all()
    serializer_class = serializers.GruposSerializer


class GruposRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Grupo.objects.all()
    serializer_class = serializers.GruposSerializer




    
