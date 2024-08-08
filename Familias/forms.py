from django import forms
from . import models

class Familias(forms.ModelForm):
    class Meta:    
        model = models.Familia
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_nome(self):
        data = self.cleaned_data.get('nome')
        return data.upper() if data else data
    
    def clean_descricao(self):
        data = self.cleaned_data.get('descricao')
        return data.upper() if data else data
