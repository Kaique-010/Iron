from django import forms
from . import models

class Localidades(forms.ModelForm):
    class Meta:    
        model = models.Localidade
        fields = ['nome', ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),

        }

    def clean_nome(self):
        data = self.cleaned_data.get('nome')
        return data.upper() if data else data
    

