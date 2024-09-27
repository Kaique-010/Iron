from django import forms
from .models import Pedido, ItemPedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['id', 'data', 'status', 'cliente', 'vendedor', 'financeiro', 'observacoes']
        widgets = {
           
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'vendedor': forms.Select(attrs={'class': 'form-control'}),
            'financeiro': forms.Select(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        

    def clean_numero_pedido(self):
        data = self.cleaned_data.get('id')
        if Pedido.objects.filter(id=data).exists():
            raise forms.ValidationError("Número do pedido já existe.")
        return data


class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['produto', 'quantidade', 'preco_unitario']
        widgets = {
            'produto': forms.Select(),
            'quantidade': forms.NumberInput(attrs={'min': 1}),
            'preco_unitario': forms.NumberInput(attrs={'min': 0}),
        }


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
