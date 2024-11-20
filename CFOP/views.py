# views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import CFOP
from .forms import CFOPForm


class CFOPCreateView(CreateView):
    model = CFOP
    form_class = CFOPForm
    template_name = 'cadastrar_cfop.html'
    success_url = reverse_lazy('cfop_lista')  
    
    def form_valid(self, form):
        
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)


class CFOPListView(ListView):
    model = CFOP
    template_name = 'cfop_lista.html'
    context_object_name = 'cfops'

    def get_queryset(self):
        
        return CFOP.objects.filter(empresa=self.request.user.empresa)


class CFOPUpdateView(UpdateView):
    model = CFOP
    form_class = CFOPForm
    template_name = 'cadastrar_cfop.html'
    success_url = reverse_lazy('cfop_lista')

    def form_valid(self, form):
        # Garante que a empresa não seja alterada
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)


class CFOPDeleteView(DeleteView):
    model = CFOP
    template_name = 'cfop_confirm_delete.html'
    success_url = reverse_lazy('cfop_lista')