from django import forms
from . import models
from django.core.exceptions import ValidationError

class Saidas(forms.ModelForm):
    class Meta:
        model = models.Saida_Produtos
        fields = ['pessoa', 'produto', 'quantidade', 'documento', 'observacoes']
        widgets = {
            'pessoa': forms.Select(attrs={'class': 'form-control'}),
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'documento': forms.NumberInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        produto = self.cleaned_data.get('produto')

        if produto and quantidade > produto.quantidade:
            raise ValidationError(
                f'A quantidade disponível em estoque para o produto {produto.nome} é de {produto.quantidade} unidades.'
            )
        return quantidade
