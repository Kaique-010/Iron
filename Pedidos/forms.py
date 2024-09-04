from django import forms
from .models import Pedido, ItemPedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['numero_pedido','cliente', 'data', 'status', 'observacoes','vendedor', 'financeiro']
        widgets = {
            'numero_pedido':forms.TextInput(),
            'cliente': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Cliente'}),
            'data': forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Data do Pedido', 'type': 'datetime-local'},format='%Y-%m-%dT%H:%M'),
            'status': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Status'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações', 'rows': 2}),
            

        }

    def clean_observacoes(self):
        data = self.cleaned_data.get('observacoes')
        return data.upper() if data else data
    
    def clean_numero_pedido(self):
        data = self.cleaned_data.get('numero_pedido')
        return data.upper() if data else data


class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['produto', 'quantidade', 'preco_unitario']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Produto'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade', 'min': 1}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço Unitário', 'step': '0.01'}),
        }

    def clean_produto(self):
        data = self.cleaned_data.get('produto')
        return data

    def clean_quantidade(self):
        data = self.cleaned_data.get('quantidade')
        if data <= 0:
            raise forms.ValidationError("A quantidade deve ser maior que zero.")
        return data
    
