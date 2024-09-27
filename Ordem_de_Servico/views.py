from io import BytesIO
from django.forms import ValidationError, inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.core import serializers
import openpyxl
from Produtos.models import Produtos
from . import models, forms
from django.urls import reverse_lazy

ItensOsFormSet = inlineformset_factory(models.OrdemServico,models.ItensOs,form=forms.ItensOsForm,extra=1,can_delete=True)

class OsListView(ListView):
    model = models.OrdemServico
    template_name = 'Oslistas.html'
    context_object_name = 'Os'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        numero_os = self.request.GET.get('numero_os')

        if numero_os:
            queryset = queryset.filter(numero_os__icontains=numero_os)

        return queryset

class OsCreateView(CreateView):
    model = models.OrdemServico
    template_name = 'Oscriar.html'
    form_class = forms.OrdemServicoForm
    success_url = reverse_lazy('Oslistas')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ItensOsFormSet(self.request.POST, instance=self.object)
        else:
            data['formset'] = ItensOsFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
        
def nova_os(request):
    if request.method == 'POST':
        form = forms.OrdemServicoForm(request.POST)
        formset = ItensOsFormSet(request.POST, prefix='itens')
        if form.is_valid() and formset.is_valid():
            ordem_servico = form.save(commit=False)
            ordem_servico.save()  # Salva a instância de OrdemServico primeiro
            formset.instance = ordem_servico  # Associa a instância de OrdemServico aos itens
            formset.save()
            return redirect('Oslistas')
    else:
        form = forms.OrdemServicoForm()
        formset = ItensOsFormSet(prefix='itens')

    produtos = Produtos.objects.all()
    produtos_json = serializers.serialize('json', produtos, fields=('id', 'nome'))

    return render(request, 'Oscriar.html', {
        'form': form,
        'formset': formset,
        'produtos_json': produtos_json,
    })

        
class OsDetailView(DetailView):
    model = models.OrdemServico
    template_name = 'Osdetalhe.html'


class OsUpdateView(UpdateView):
    model = models.OrdemServico
    template_name = 'Oscriar.html'
    form_class = forms.OrdemServicoForm
    success_url = reverse_lazy('Oslistas')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ItensOsFormSet(self.request.POST, instance=self.object)
        else:
            data['formset'] = ItensOsFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())



class OsDeleteView(DeleteView):
    model = models.OrdemServico
    template_name = 'Osexcluir.html'
    success_url = reverse_lazy('Oslistas')



def exportar_os_excel(request):
    
    
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Ordens de Serviço'

    
    columns = ['Nº O.S', 'Data Abertura', 'Cliente',]
    worksheet.append(columns)

    
    ordens = models.OrdemServico.objects.all()
    for ordem in ordens:
        worksheet.append([
            ordem.numero_os,
            ordem.data_abertura.strftime('%d/%m/%Y') if ordem.data_abertura else '',
            str(ordem.cliente) if ordem.cliente else '', 
            
        ])
   
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=ordens_servico.xlsx'
    return response