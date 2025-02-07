from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Vendedora, Acerto, EstoqueVendedora
from .forms import VendedoraForm, AcertoForm
from estoque.models import Produto

def lista_vendedoras(request):
    vendedoras = Vendedora.objects.all()
    return render(request, 'vendedoras/lista_vendedoras.html', {'vendedoras': vendedoras})

def adicionar_vendedora(request):
    if request.method == 'POST':
        form = VendedoraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vendedora adicionada com sucesso!')
            return redirect('vendedoras:lista_vendedoras')
    else:
        form = VendedoraForm()
    return render(request, 'vendedoras/form_vendedora.html', {'form': form})

def editar_vendedora(request, pk):
    vendedora = get_object_or_404(Vendedora, pk=pk)
    if request.method == 'POST':
        form = VendedoraForm(request.POST, instance=vendedora)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vendedora atualizada com sucesso!')
            return redirect('vendedoras:lista_vendedoras')
    else:
        form = VendedoraForm(instance=vendedora)
    return render(request, 'vendedoras/form_vendedora.html', {'form': form, 'vendedora': vendedora})

def detalhe_vendedora(request, pk):
    vendedora = get_object_or_404(Vendedora, pk=pk)
    acertos = Acerto.objects.filter(vendedora=vendedora)
    estoque = EstoqueVendedora.objects.filter(vendedora=vendedora)
    return render(request, 'vendedoras/detalhe_vendedora.html', {
        'vendedora': vendedora, 
        'acertos': acertos,
        'estoque': estoque
    })

@transaction.atomic
def realizar_acerto(request, pk):
    vendedora = get_object_or_404(Vendedora, pk=pk)
    if request.method == 'POST':
        form = AcertoForm(request.POST)
        if form.is_valid():
            acerto = form.save(commit=False)
            acerto.vendedora = vendedora
            acerto.save()
            messages.success(request, 'Acerto realizado com sucesso!')
            return redirect('vendedoras:detalhe_vendedora', pk=vendedora.pk)
    else:
        form = AcertoForm()
    return render(request, 'vendedoras/form_acerto.html', {'form': form, 'vendedora': vendedora})

@transaction.atomic
def adicionar_estoque_vendedora(request, pk):
    vendedora = get_object_or_404(Vendedora, pk=pk)
    if request.method == 'POST':
        produto_id = request.POST.get('produto')
        quantidade = int(request.POST.get('quantidade', 0))
        produto = get_object_or_404(Produto, pk=produto_id)
        
        estoque, created = EstoqueVendedora.objects.get_or_create(
            vendedora=vendedora,
            produto=produto,
            defaults={'quantidade': 0}
        )
        estoque.quantidade += quantidade
        estoque.save()
        
        messages.success(request, f'{quantidade} unidades de {produto.nome} adicionadas ao estoque de {vendedora.nome}.')
        return redirect('vendedoras:detalhe_vendedora', pk=vendedora.pk)
    
    produtos = Produto.objects.all()
    return render(request, 'vendedoras/adicionar_estoque.html', {'vendedora': vendedora, 'produtos': produtos})

