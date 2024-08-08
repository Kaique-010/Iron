from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from django.urls import reverse_lazy

class LocalidadesListView(ListView):
    model = models.Localidade
    template_name = 'localidadeslistas.html'
    context_object_name = 'localidades'
    paginate_by = 5

    def get_queryset(self):
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

class LocalidadesDetailView(DetailView):
    model = models.Localidade
    template_name = 'localidadesdetalhe.html'


class LocalidadesUpdateView(UpdateView):
    model = models.Localidade
    template_name = 'localidadeseditar.html'
    form_class = forms.Localidades
    success_url = reverse_lazy('localidadeslistas')



class LocalidadesDeleteView(DeleteView):
    model = models.Localidade
    template_name = 'localidadesexcluir.html'
    success_url = reverse_lazy('localidadeslistas')




    
