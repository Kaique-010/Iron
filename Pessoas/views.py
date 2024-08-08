from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from django.urls import reverse_lazy

class PessoasListView(ListView):
    model = models.Pessoas
    template_name = 'pessoaslistas.html'
    context_object_name = 'Pessoas'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.GET.get('nome')

        if nome:
            queryset = queryset.filter(nome__icontains=nome)

        return queryset

class PessoasCreateView(CreateView):
    model = models.Pessoas
    template_name = 'pessoascriar.html'
    form_class = forms.Pessoas
    success_url = reverse_lazy('pessoaslistas')

class PessoasDetailView(DetailView):
    model = models.Pessoas
    template_name = 'pessoasdetalhe.html'


class PessoasUpdateView(UpdateView):
    model = models.Pessoas
    template_name = 'pessoaseditar.html'
    form_class = forms.Pessoas
    success_url = reverse_lazy('pessoaslistas')



class PessoasDeleteView(DeleteView):
    model = models.Pessoas
    template_name = 'pessoasexcluir.html'
    success_url = reverse_lazy('pessoaslistas')




    
