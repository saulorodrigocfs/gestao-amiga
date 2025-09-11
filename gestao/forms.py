from django import forms
from .models import Loja

class LojaForm(forms.ModelForm):
    class Meta:
        model = Loja
        fields = ['nome', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
        }
        