from django import forms
from .models import ContaAPagar, ContaAReceber, FormasPagamento, FormasRecebimento, Categorias
from .models import GerarParcela

class ContaAPagarForm(forms.ModelForm):
    class Meta:
        model = ContaAPagar
        fields = [ 'status_pagamento','documento', 'descricao', 'parcela', 'valor',
                   'data_emissao', 'data_vencimento', 'data_pagamento', 'pessoas',
                   'categorias', 'observacoes',  'forma_pagamento']
        widgets = {
            'documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Documento'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'parcela': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Parcelas'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor'}),
            'data_emissao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'data_pagamento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'pessoas': forms.Select(attrs={'class': 'form-control'}),
            'categorias': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações','rows': 3}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-control'}),
        }

class ContaAReceberForm(forms.ModelForm):
    class Meta:
        model = ContaAReceber
        fields = [ 'status_recebimento','documento', 'descricao', 'parcela', 'valor','data_emissao',
                  'data_vencimento', 'data_recebimento','pessoas', 'categorias', 'observacoes',
                  'forma_recebimento']
        
        widgets = {
            'documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Documento'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'parcela': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Parcelas'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor'}),
            'data_emissao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'data_recebimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'pessoas': forms.Select(attrs={'class': 'form-control'}),
            'categorias': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações'}),
            'forma_recebimento': forms.Select(attrs={'class': 'form-control'}),
        }

class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='Data Inicial', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='Data Final', widget=forms.DateInput(attrs={'type': 'date'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].input_formats = ['%Y-%m-%d']
        self.fields['end_date'].input_formats = ['%Y-%m-%d']    






class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categorias
        fields = ['descricao'] 

    
    descricao = forms.CharField(max_length=255, required=False, label='Descrição', widget=forms.Textarea(attrs={'class': 'form-control'}))

    def clean_nome(self):
        nome = self.cleaned_data['descricao']
        if Categorias.objects.filter(descricao='descricao').exists():
            raise forms.ValidationError("Esta categoria já existe.")
        return nome


class FormasRecebimentoForm(forms.ModelForm):
    class Meta:
        model = FormasRecebimento
        fields = ['descricao']  

    descricao = forms.CharField(max_length=255, label='Descrição', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_descricao(self):
        descricao = self.cleaned_data['descricao']
        if FormasRecebimento.objects.filter(descricao=descricao).exists():
            raise forms.ValidationError("Esta forma de recebimento já existe.")
        return descricao




class FormasPagamentoForm(forms.ModelForm):
    class Meta:
        model = FormasPagamento
        fields = ['descricao']  

    descricao = forms.CharField(max_length=255, label='Descrição', widget=forms.TextInput(attrs={'class': 'form-control'}))
    

    def clean_descricao(self):
        descricao = self.cleaned_data['descricao']
        if FormasPagamento.objects.filter(descricao=descricao).exists():
            raise forms.ValidationError("Esta forma de pagamento já existe.")
        return descricao



class GerarParcelasForm(forms.ModelForm):
    class Meta:
        model = GerarParcela
        fields = [
            "valor",
            "vencimento_inicial",
            "tipo",
            "documento",
            "total_parcelas",
            "descricao",
            "quitacao",
            "responsavel",
            "pagamento_total",
            "pagamento_parcial",
            "valor_pago"
        ]
        widgets = {
            "valor": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Valor total"}),
            "vencimento_inicial": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "documento": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Número do documento"}),
            "total_parcelas": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Total de parcelas"}),
            "descricao": forms.TextInput(attrs={"class": "form-control", "placeholder": "Descrição (opcional)"}),
            "quitacao": forms.Select(attrs={"class": "form-control"}),
            "responsavel": forms.Select(attrs={"class": "form-control"}),
            "pagamento_total": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "pagamento_parcial": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "valor_pago": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Valor Pago"}),
        }