from django import forms
from . import models

class Pessoas(forms.ModelForm):
    class Meta:    
        model = models.Pessoas
        fields = ['classificacao','nome', 'cpf', 'rg', 'email', 'cnpj', 'ie', 'telefone', 'obs', 'foto']
        widgets = {
            'classificacao': forms.Select(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF', 'maxlength': '14'}),
            'rg': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RG'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ', 'maxlength': '18'}),
            'ie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inscrição Estadual'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone', 'maxlength': '15'}),
            'obs': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações', 'rows': 4}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_nome(self):
        data = self.cleaned_data.get('nome')
        return data.upper() if data else data

    def clean_cpf(self):
        data = self.cleaned_data.get('cpf')
        return data.upper() if data else data

    def clean_rg(self):
        data = self.cleaned_data.get('rg')
        return data.upper() if data else data

    def clean_email(self):
        data = self.cleaned_data.get('email')
        return data.upper() if data else data

    def clean_cnpj(self):
        data = self.cleaned_data.get('cnpj')
        return data.upper() if data else data

    def clean_ie(self):
        data = self.cleaned_data.get('ie')
        return data.upper() if data else data

    def clean_telefone(self):
        data = self.cleaned_data.get('telefone')
        return data.upper() if data else data

    def clean_obs(self):
        data = self.cleaned_data.get('obs')
        return data.upper() if data else data
