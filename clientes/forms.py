from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['foto', 'nome', 'cpf', 'rua', 'numero', 'bairro', 'cidade', 'uf', 'telefone1', 'telefone2', 'obs']
        widgets = {
            'foto': forms.FileInput(attrs={'class': 'form-control-file'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXX.XXX.XXX-XX'}),
            'rua': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da rua'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'uf': forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Selecione UF')] + [(uf, uf) for uf in ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']]),
            'telefone1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX'}),
            'telefone2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX (opcional)'}),
            'obs': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações (opcional)'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cpf = ''.join(filter(str.isdigit, cpf))
            if len(cpf) != 11:
                raise forms.ValidationError("CPF deve conter 11 dígitos.")
        return cpf

    def clean_telefone1(self):
        telefone = self.cleaned_data.get('telefone1')
        if telefone:
            telefone = ''.join(filter(str.isdigit, telefone))
            if len(telefone) < 10 or len(telefone) > 11:
                raise forms.ValidationError("Telefone deve conter 10 ou 11 dígitos.")
        return telefone

    def clean_telefone2(self):
        telefone = self.cleaned_data.get('telefone2')
        if telefone:
            telefone = ''.join(filter(str.isdigit, telefone))
            if len(telefone) < 10 or len(telefone) > 11:
                raise forms.ValidationError("Telefone deve conter 10 ou 11 dígitos.")
        return telefone

