from django import forms
from .models import Vendedora, EstoqueVendedora

class VendedoraForm(forms.ModelForm):
    class Meta:
        model = Vendedora
        fields = ['nome', 'telefone']

class EstoqueVendedoraForm(forms.ModelForm):
    class Meta:
        model = EstoqueVendedora
        fields = ['produto', 'quantidade']

