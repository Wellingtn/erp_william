from django import forms
from django.forms import inlineformset_factory
from .models import Venda, ItemVenda
from estoque.models import Produto

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente']

class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade', 'preco_unitario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produto'].queryset = Produto.objects.filter(quantidade__gt=0)
        self.fields['produto'].widget.attrs.update({'class': 'select2 produto-select'})
        self.fields['quantidade'].widget.attrs.update({'class': 'quantidade-input', 'min': '1'})
        self.fields['preco_unitario'].widget.attrs.update({'class': 'preco-unitario-input', 'readonly': 'readonly'})

ItemVendaFormSet = inlineformset_factory(
    Venda, 
    ItemVenda, 
    form=ItemVendaForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)

