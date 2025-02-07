from django import forms
from .models import Venda, ItemVenda
from estoque.models import Produto

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente']

class ItemVendaForm(forms.ModelForm):
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.filter(quantidade__gt=0),
        empty_label="Selecione um produto",
        widget=forms.Select(attrs={'class': 'w-full p-2 border border-purple-300 rounded produto-select'})
    )
    quantidade = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'w-full p-2 border border-purple-300 rounded'})
    )
    preco_unitario = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'w-full p-2 border border-purple-300 rounded', 'readonly': 'readonly'})
    )

    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade', 'preco_unitario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produto'].queryset = Produto.objects.filter(quantidade__gt=0)

ItemVendaFormSet = forms.inlineformset_factory(
    Venda, ItemVenda, form=ItemVendaForm,
    extra=1, can_delete=True,
    min_num=1, validate_min=True
)

