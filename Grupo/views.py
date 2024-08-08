from rest_framework import generics
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms, serializers
from django.urls import reverse_lazy

class GruposListView(ListView):
    model = models.Grupo
    template_name = 'gruposlistas.html'
    context_object_name = 'Grupos'
    paginate_by = 5

    def get_queryset(self):
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

class GruposDetailView(DetailView):
    model = models.Grupo
    template_name = 'gruposdetalhe.html'


class GruposUpdateView(UpdateView):
    model = models.Grupo
    template_name = 'gruposeditar.html'
    form_class = forms.Grupos
    success_url = reverse_lazy('gruposlistas')



class GruposDeleteView(DeleteView):
    model = models.Grupo
    template_name = 'gruposexcluir.html'
    success_url = reverse_lazy('gruposlistas')


class GruposCreateListAPIView(generics.ListCreateAPIView):
    queryset = models.Grupo.objects.all()
    serializer_class = serializers.GruposSerializer


class GruposRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Grupo.objects.all()
    serializer_class = serializers.GruposSerializer




    
