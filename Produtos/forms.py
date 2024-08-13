from django import forms
from . import models

class Produtos(forms.ModelForm):
    class Meta:
        model = models.Produtos
        fields = ['nome', 'localidade', 'familia', 'grupo', 'marca', 'tamanho', 'peso', 'quantidade', 'descricao', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome Produto'}),
            'localidade': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Localidade'}),
            'familia': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Familia'}),
            'grupo': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Grupo'}),
            'marca': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Marca'}),
            'tamanho': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tamanho', 'maxlength': '6'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade', 'maxlength': '6'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição', 'rows': 2}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_nome(self):
        data = self.cleaned_data.get('nome')
        return data.upper() if data else data


    def clean_descricao(self):
        data = self.cleaned_data.get('descricao')
        return data.upper() if data else data
    

