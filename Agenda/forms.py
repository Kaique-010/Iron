from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'data_inicio', 'data_fim', 'horario', 'local', 'descricao', 'responsavel']  
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'data_fim': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'horario': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'responsavel': forms.Select(attrs={'class': 'form-control', 'placeholder':'Responsável'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Não associamos a empresa aqui, pois isso deve ser feito na view.
        if commit:
            instance.save()
        return instance
