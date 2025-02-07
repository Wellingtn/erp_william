from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'w-full p-2 border border-purple-300 rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border border-purple-300 rounded'}),
            'telefone': forms.TextInput(attrs={'class': 'w-full p-2 border border-purple-300 rounded'}),
            'endereco': forms.Textarea(attrs={'class': 'w-full p-2 border border-purple-300 rounded', 'rows': 3}),
        }

