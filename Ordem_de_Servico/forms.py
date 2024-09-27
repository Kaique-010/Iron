from django import forms
from .models import OrdemServico, ItensOs



class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = ['numero_os', 'cliente', 'data_abertura', 'data_fechamento']
        widgets = {
            'numero_os': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'data_abertura': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Data do Pedido', 'type': 'datetime-local'},format='%Y-%m-%dT%H:%M'),
            'data_fechamento': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Data do Pedido', 'type': 'datetime-local'},format='%Y-%m-%dT%H:%M'),
        }

    def clean_numero_os(self):
        data = self.cleaned_data.get('numero_os')
        return data.upper() if data else data

class ItensOsForm(forms.ModelForm):
    class Meta:
        model = ItensOs
        fields = ['numero_os', 'item_numero', 'peca', 'servico', 'peca_quantidade', 'peca_unitario', 'peca_desconto', 'peca_total']
        widgets = {
            'numero_os': forms.Select(attrs={'class': 'form-control'}),
            'item_numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'peca': forms.Select(attrs={'class': 'form-control'}),
            'servico': forms.Select(attrs={'class': 'form-control'}),
            'peca_quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'peca_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'peca_desconto': forms.NumberInput(attrs={'class': 'form-control'}),
            'peca_total': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_item_numero(self):
        data = self.cleaned_data.get('item_numero')
        return data if data >= 0 else None

    def clean_peca_quantidade(self):
        data = self.cleaned_data.get('peca_quantidade')
        return data if data >= 0 else None

    def clean_peca_unitario(self):
        data = self.cleaned_data.get('peca_unitario')
        return data if data >= 0 else None

    def clean_peca_desconto(self):
        peca_desconto = self.cleaned_data.get('peca_desconto')
        if peca_desconto is not None and peca_desconto < 0:
            raise forms.ValidationError("O desconto da peça não pode ser negativo.")
        return peca_desconto

    def clean_peca_total(self):
        data = self.cleaned_data.get('peca_total')
        return data if data >= 0 else None
