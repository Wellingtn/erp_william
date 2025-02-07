from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'quantidade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'w-full p-2 border border-purple-300 rounded'}),
            'descricao': forms.Textarea(attrs={'class': 'w-full p-2 border border-purple-300 rounded', 'rows': 3}),
            'preco': forms.NumberInput(attrs={'class': 'w-full p-2 border border-purple-300 rounded', 'step': '0.01'}),
            'quantidade': forms.NumberInput(attrs={'class': 'w-full p-2 border border-purple-300 rounded'}),
        }

