from django import forms
from .models import OrdemProducao, EtapaProducao, MateriaPrimaConsumida

class OrdemProducaoForm(forms.ModelForm):
    class Meta:
        model = OrdemProducao
        fields = ['numero_ordem', 'cliente',  'produto', 'quantidade','unidade_medida', 'data_criacao', 'data_prevista_finalizacao', 'status', 'responsavel_atual']
        widgets = {
            'numero_ordem':forms.NumberInput(attrs={'type': 'form_control', 'placeholder':'Nº Ordem'}),
            'cliente':forms.Select(attrs={'type': 'form_control', 'placeholder':'Interessado à Ordem'}),
            'data_prevista_finalizacao': forms.DateInput(attrs={'type': 'date'}),
            'data_criacao': forms.DateInput(attrs={'type': 'date'}),
            'produto':forms.Select(attrs={'type': 'form_control', 'placeholder':'Produto Acabado'}),
            'quantidade':forms.NumberInput(attrs={'type': 'form_control', 'placeholder':'Quantidade'}),
            'unidade_medida':forms.Select(attrs={'type': 'form_control', 'placeholder':'Unidade de medida'}),
            'status':forms.Select(attrs={'type': 'form_control', 'placeholder':'Status da Ordem'}),
            'responsavel_atual':forms.Select(attrs={'type': 'form_control', 'placeholder':'Responsável atual'}),
        }


class EtapaProducaoUpdateForm(forms.ModelForm):
    class Meta:
        model = EtapaProducao
        fields = [
            'etapa', 'status', 'responsavel', 'data_inicio', 'data_conclusao',
            'materias_primas_consumidas', 'observacoes'
        ]
        widgets = {
            'etapa': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'responsavel': forms.Select(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_conclusao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'materias_primas_consumidas': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class MateriaPrimaConsumidaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrimaConsumida
        fields = ['materia_prima', 'quantidade_usada']
        widgets = {
            'materia_prima': forms.Select(attrs={'class': 'form-control'}),
            'quantidade_usada': forms.NumberInput(attrs={'class': 'form-control'}),
        }