from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
import openpyxl
from . import models, forms
from django.urls import reverse_lazy
from Pessoas.models import Pessoas

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

    def form_valid(self, form):
        # Chama a função de busca de CEP
        cep = form.cleaned_data.get('cep')
        dados_endereco = buscar_cep(cep)
        
        if dados_endereco and 'erro' not in dados_endereco:
            # Preenche os campos de endereço no formulário
            form.instance.logradouro = dados_endereco.get('logradouro')
            form.instance.bairro = dados_endereco.get('bairro')
            form.instance.cidade = dados_endereco.get('localidade')
            form.instance.estado = dados_endereco.get('uf')

        return super().form_valid(form)

class PessoasDetailView(DetailView):
    model = models.Pessoas
    template_name = 'pessoasdetalhe.html'


class PessoasUpdateView(UpdateView):
    model = models.Pessoas
    template_name = 'pessoaseditar.html'
    form_class = forms.Pessoas
    success_url = reverse_lazy('pessoaslistas')

    def form_valid(self, form):

        cep = form.cleaned_data.get('cep')
        dados_endereco = buscar_cep(cep)
        
        if dados_endereco and 'erro' not in dados_endereco:
            # Preenche os campos de endereço no formulário
            form.instance.logradouro = dados_endereco.get('logradouro')
            form.instance.bairro = dados_endereco.get('bairro')
            form.instance.cidade = dados_endereco.get('localidade')
            form.instance.estado = dados_endereco.get('uf')

        return super().form_valid(form)



class PessoasDeleteView(DeleteView):
    model = models.Pessoas
    template_name = 'pessoasexcluir.html'
    success_url = reverse_lazy('pessoaslistas')



def exportar_pessoas_excel(request):
    # Cria uma planilha do Excel
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Pessoas'

    # Define o cabeçalho
    columns = ['ID',
               'Nome', 'RG', 'CPF', 'CNPJ', 'IE', 'Telefone', 'Classificação']
    worksheet.append(columns)

    # Adiciona os dados
    pessoas = Pessoas.objects.all()  # Corrigido para obter todas as instâncias de Pessoas
    for pessoa in pessoas:  # Corrigido para iterar sobre instâncias de Pessoas
        worksheet.append([
            pessoa.id,
            pessoa.nome,
            pessoa.rg,
            pessoa.cpf,
            pessoa.cnpj,
            pessoa.ie,
            pessoa.telefone,
            pessoa.classificacao,
        ])
   
    # Salva a planilha em um buffer
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    # Prepara a resposta HTTP
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=pessoas.xlsx'
    return response


import requests

def buscar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
