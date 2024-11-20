# forms.py
from django import forms
from .models import CFOP

class CFOPForm(forms.ModelForm):
    class Meta:
        model = CFOP
        fields = [
            'cfop', 'descricao_fiscal', 'finalidade', 'aplica_icms', 'aplica_pis', 'aplica_cofins', 'aplica_ipi',
            'cst_icms', 'modalidade_calculo_icms', 'aliquota_icms', 'reducao_icms', 'mva',
            'cst_pis', 'aliquota_pis', 'cst_cofins', 'aliquota_cofins', 'cst_ipi', 'aliquota_ipi'
        ]
        widgets = {
            'descricao_fiscal': forms.TextInput(attrs={'class': 'form-control'}),
            'cfop': forms.Select(attrs={'class': 'form-control'}),
            'finalidade': forms.Select(attrs={'class': 'form-control'}),
            'aplica_icms': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'aplica_pis': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'aplica_cofins': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'aplica_ipi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cst_icms': forms.Select(attrs={'class': 'form-control'}),
            'modalidade_calculo_icms': forms.TextInput(attrs={'class': 'form-control'}),
            'aliquota_icms': forms.NumberInput(attrs={'class': 'form-control'}),
            'reducao_icms': forms.NumberInput(attrs={'class': 'form-control'}),
            'mva': forms.NumberInput(attrs={'class': 'form-control'}),
            'cst_pis': forms.Select(attrs={'class': 'form-control'}),
            'aliquota_pis': forms.NumberInput(attrs={'class': 'form-control'}),
            'cst_cofins': forms.Select(attrs={'class': 'form-control'}),
            'aliquota_cofins': forms.NumberInput(attrs={'class': 'form-control'}),
            'cst_ipi': forms.Select(attrs={'class': 'form-control'}),
            'aliquota_ipi': forms.NumberInput(attrs={'class': 'form-control'}),
        }
