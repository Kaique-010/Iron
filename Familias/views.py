from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from django.urls import reverse_lazy

class FamiliasListView(ListView):
    model = models.Familia
    template_name = 'familiaslistas.html'
    context_object_name = 'familias'
    paginate_by = 5

    def get_queryset(self):
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

class FamiliaDetailView(DetailView):
    model = models.Familia
    template_name = 'familiasdetalhe.html'


class FamiliaUpdateView(UpdateView):
    model = models.Familia
    template_name = 'familiaseditar.html'
    form_class = forms.Familias
    success_url = reverse_lazy('familiaslistas')



class FamiliaDeleteView(DeleteView):
    model = models.Familia
    template_name = 'familiasexcluir.html'
    success_url = reverse_lazy('listas')




    
