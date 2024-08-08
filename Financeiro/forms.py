from django import forms
from .models import ContaAPagar, ContaAReceber, FormasPagamento, FormasRecebimento, Categorias

class ContaAPagarForm(forms.ModelForm):
    class Meta:
        model = ContaAPagar
        fields = [ 'status_pagamento','documento', 'descricao', 'parcela', 'valor',
                   'data_emissao', 'data_vencimento', 'data_pagamento', 'pessoas', 'categorias', 'observacoes', 'usuario', 'forma_pagamento']
        widgets = {
            'documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Documento'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'parcela': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Parcelas'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor'}),
            'data_emissao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_vencimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_pagamento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pessoas': forms.Select(attrs={'class': 'form-control'}),
            'categorias': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações','rows': 3}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-control'}),
        }

class ContaAReceberForm(forms.ModelForm):
    class Meta:
        model = ContaAReceber
        fields = [ 'status_recebimento','documento', 'descricao', 'parcela', 'valor',
                   'data_emissao', 'data_vencimento', 'data_recebimento','pessoas', 'categorias', 'observacoes', 'usuario', 'forma_recebimento']
        widgets = {
            'documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Documento'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'parcela': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Parcelas'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor'}),
            'data_emissao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_vencimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_recebimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pessoas': forms.Select(attrs={'class': 'form-control'}),
            'categorias': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações'}),
            'forma_recebimento': forms.Select(attrs={'class': 'form-control'}),
        }

class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='Data Inicial', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='Data Final', widget=forms.DateInput(attrs={'type': 'date'}))
