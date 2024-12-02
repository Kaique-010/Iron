from django import forms
from Empresas.models import Empresa
from Financeiro.models import FormasRecebimento
from .models import Pedido, ItemPedido
from Pessoas.models import Pessoas


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['data', 'status', 'cliente', 'vendedor', 'financeiro', 'observacoes']
        widgets = {
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'vendedor': forms.Select(attrs={'class': 'form-control'}),
            'financeiro': forms.Select(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    # Validações customizadas
    def clean_cliente(self):
        cliente = self.cleaned_data.get('cliente')
        if not cliente:
            raise forms.ValidationError("Selecione um cliente.")
        return cliente


class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['produto', 'quantidade', 'preco_unitario']
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Verifique se a instância do formulário já tem um produto associado
        if self.instance and hasattr(self.instance, 'produto') and self.instance.produto:
            # Se já existe um produto no pedido
            preco_unitario_produto = self.instance.produto.precos.first()
            if preco_unitario_produto:
                # Define o valor inicial para o campo preco_unitario
                self.fields['preco_unitario'].initial = preco_unitario_produto.preco_venda_vista
    
    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        produto = self.cleaned_data.get('produto')
        if quantidade > produto.quantidade:
            raise forms.ValidationError(f"Estoque insuficiente para o produto {produto}.")
        return quantidade

    def clean_preco_unitario(self):
        preco_unitario = self.cleaned_data.get('preco_unitario')
        produto = self.cleaned_data.get('produto')

        if produto:
            # Acesse o primeiro preço de venda relacionado ao produto
            preco_unitario_produto = produto.precos.first().preco_venda_vista  # Produto -> Precos -> preco_venda_vista
            if preco_unitario != preco_unitario_produto:
                raise forms.ValidationError(f'O preço unitário deve ser {preco_unitario_produto}')
        
        return preco_unitario



class CRMForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("A data de início não pode ser posterior à data de término.")

        return cleaned_data


class DateRangeForm(forms.Form):
    dias = forms.IntegerField(label="Período de Inatividade (em dias)", required=False, initial=180)
