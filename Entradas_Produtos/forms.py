from django import forms
from . import models

class Entradas(forms.ModelForm):
    class Meta:    
        model = models.Entrada_Produtos
        fields = ['pessoa', 'produto', 'quantidade', 'documento', 'observacoes']
        widgets = {
            'pessoa': forms.Select(attrs={'class': 'form-control'}),
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'documento': forms.NumberInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
