from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from django.urls import reverse_lazy

class MarcasListView(ListView):
    model = models.Marcas
    template_name = 'marcaslistas.html'
    context_object_name = 'marcas'
    paginate_by = 5

    def get_queryset(self):
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

class MarcasDetailView(DetailView):
    model = models.Marcas
    template_name = 'marcasdetalhe.html'


class MarcasUpdateView(UpdateView):
    model = models.Marcas
    template_name = 'marcaseditar.html'
    form_class = forms.Marcas
    success_url = reverse_lazy('marcaslistas')



class MarcasDeleteView(DeleteView):
    model = models.Marcas
    template_name = 'marcasexcluir.html'
    success_url = reverse_lazy('marcaslistas')




    
