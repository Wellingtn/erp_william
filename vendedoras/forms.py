from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Vendedora, Acerto

class VendedoraForm(forms.ModelForm):
    class Meta:
        model = Vendedora
        fields = ['nome', 'telefone']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'w-full p-2 border border-purple-300 rounded'}),
            'telefone': forms.TextInput(attrs={'class': 'w-full p-2 border border-purple-300 rounded'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("As senhas não coincidem.")

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        vendedora = super().save(commit=False)
        vendedora.user = user
        if commit:
            vendedora.save()
        return vendedora

class AcertoForm(forms.ModelForm):
    class Meta:
        model = Acerto
        fields = ['total_vendas', 'comissao']
        widgets = {
            'total_vendas': forms.NumberInput(attrs={'class': 'w-full p-2 border border-purple-300 rounded', 'step': '0.01'}),
            'comissao': forms.NumberInput(attrs={'class': 'w-full p-2 border border-purple-300 rounded', 'step': '0.01'}),
        }


class VendedoraUpdateForm(forms.ModelForm):
    class Meta:
        model = Vendedora
        fields = ['nome', 'telefone']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'w-full p-2 border border-purple-300 rounded'}),
            'telefone': forms.TextInput(attrs={'class': 'w-full p-2 border border-purple-300 rounded'}),
        }

