from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.db import IntegrityError, connections, transaction
from .models import Etapa, OrdemProducao, EtapaProducao, MateriaPrimaConsumida, Responsavel
from .forms import OrdemProducaoForm, EtapaProducaoUpdateForm
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import FormView
from django.forms import inlineformset_factory, modelformset_factory

EtapaProducaoFormSet = inlineformset_factory(
    OrdemProducao, 
    EtapaProducao, 
    fields=['etapa', 'status', 'responsavel', 'data_inicio', 'data_conclusao'],
    extra=1,
    can_delete=True
)

def set_empresa_database(empresa):
    db_alias = empresa.database  
    if db_alias not in connections:
        raise IntegrityError(f"Banco de dados {db_alias} não configurado.")
    connections['default'] = connections[db_alias]


class OrdemProducaoListView(ListView):
    model = OrdemProducao
    template_name = 'ordemproducao/ordem_list.html'
    context_object_name = 'ordens'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        # Verificar se o usuário está autenticado antes de continuar
        if not request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # A verificação de autenticação já foi feita no dispatch, então não precisa mais no get_queryset
        set_empresa_database(self.request.user.empresa)
        
        queryset = super().get_queryset()
        numero_ordem = self.request.GET.get('numero_ordem')

        if numero_ordem:
            queryset = queryset.filter(numero_ordem__icontains=numero_ordem)

        return queryset
    

class OrdemProducaoCreateView(CreateView):
    model = OrdemProducao
    form_class = OrdemProducaoForm
    template_name = 'ordemproducao/ordem_form.html'
    success_url = reverse_lazy('OrdemProducao:ordem_list')

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return redirect('login')
        
        if not self.request.user.empresa:
            raise PermissionDenied("Usuário não associado a uma empresa.")
        
        set_empresa_database(self.request.user.empresa)
        form.instance.empresa = self.request.user.empresa
        form.instance.responsavel_atual = self.request.user
        return super().form_valid(form)


class OrdemProducaoUpdateView(UpdateView):
    model = OrdemProducao
    form_class = OrdemProducaoForm
    template_name = 'ordemproducao/ordem_edit.html'
    success_url = reverse_lazy('OrdemProducao:ordem_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_empresa_database(self.request.user.empresa)

        if self.request.POST:
            context['etapa_formset'] = EtapaProducaoFormSet(self.request.POST, instance=self.object)
        else:
            context['etapa_formset'] = EtapaProducaoFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        etapa_formset = context['etapa_formset']

        if etapa_formset.is_valid():
            self.object = form.save()
            etapa_formset.instance = self.object
            etapa_formset.save()
            return redirect(self.success_url)

        return self.form_invalid(form)
    
class OrdemProducaoDetailView(DetailView):
    model = OrdemProducao
    template_name = 'ordemproducao/ordem_detail.html'
    context_object_name = 'ordem'

    def get_object(self):
        if not self.request.user.empresa:
            return redirect('login')
        
        set_empresa_database(self.request.user.empresa)
        return super().get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['etapas'] = self.object.etapas.all()  
        return context
    

class OrdemProducaoDeleteView(DeleteView):
    model = OrdemProducao
    template_name = 'ordemproducao/confirm_delete.html'
    context_object_name = 'ordem'

    def get_object(self):
        if not self.request.user.empresa:
            return redirect('login') 
        
        set_empresa_database(self.request.user.empresa)  
        return super().get_object()
    

class EtapaProducaoView(FormView):
    template_name = 'ordemproducao/etapas_form.html'
    form_class = EtapaProducaoFormSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ordem = get_object_or_404(OrdemProducao, pk=self.kwargs['pk'])
        set_empresa_database(self.request.user.empresa)
        context['ordem'] = ordem
        context['formset'] = self.form_class(instance=ordem)
        return context

    def form_valid(self, formset):
        ordem = get_object_or_404(OrdemProducao, pk=self.kwargs['pk'])
        set_empresa_database(self.request.user.empresa)
        formset.instance = ordem
        formset.save()
        return redirect('OrdemProducao:ordem_detail', pk=ordem.pk)
    

class EtapaListView(ListView):
    model = Etapa
    template_name = 'ordemproducao/etapa_list.html'
    context_object_name = 'etapas'

class ResponsavelListView(ListView):
    model = Responsavel
    template_name = 'ordemproducao/responsavel_list.html'
    context_object_name = 'responsaveis'
    

class EtapaCreateView(CreateView):
    model = Etapa
    fields = ['nome', 'descricao']
    template_name = 'ordemproducao/etapa_form.html'
    success_url = reverse_lazy('OrdemProducao:etapa_list')

class ResponsavelCreateView(CreateView):
    model = Responsavel
    fields = ['nome', 'cargo']
    template_name = 'ordemproducao/responsavel_form.html'
    success_url = reverse_lazy('OrdemProducao:responsavel_list')
