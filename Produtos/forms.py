from django import forms
from . import models

class Produtos(forms.ModelForm):
    class Meta:
        model = models.Produtos
        fields = ['nome', 'unidade_medida', 'ncm','localidade', 'familia', 'grupo', 'marca', 'tamanho', 'peso', 'quantidade', 'descricao', 'imagem', 'ativo', 'tipo_produto']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome Produto'}),
            'unidade_medida': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Unidade de medida'}),
            'ncm': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NCM'}),
            'localidade': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Localidade'}),
            'familia': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Familia'}),
            'grupo': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Grupo'}),
            'marca': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Marca'}),
            'tamanho': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tamanho', 'maxlength': '6'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade', 'maxlength': '6'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição', 'rows': 2}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'ativo': forms.NullBooleanSelect(),
            'tipo_produto': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tipo Produto'}),
        }

    def clean_nome(self):
        data = self.cleaned_data.get('nome')
        return data.upper() if data else data


    def clean_descricao(self):
        data = self.cleaned_data.get('descricao')
        return data.upper() if data else data
    


class PrecosForm(forms.ModelForm):
    class Meta:
        model = models.Precos
        fields = ['preco_compra', 'preco_venda_vista', 'preco_venda_prazo', 'percentual_venda_vista', 'percentual_venda_prazo']
        widgets = {
            'preco_compra': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço de Compra'}),
            'preco_venda_vista': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço de Venda à Vista'}),
            'preco_venda_prazo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço de Venda a Prazo'}),
            'percentual_venda_vista': forms.NumberInput(attrs={'class': 'form-control'}),
            'percentual_venda_prazo': forms.NumberInput(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['percentual_venda_vista'].widget.attrs['readonly'] = True
        self.fields['percentual_venda_prazo'].widget.attrs['readonly'] = True

class Unidades(forms.ModelForm):
    class Meta:
        model = models.UnidadeMedida
        fields = ['descricao', 'sigla']
        widgets = {
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição', 'rows': 2}),
            'sigla': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição', 'rows': 2}),
        }
