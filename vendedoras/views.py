from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Vendedora, EstoqueVendedora
from .forms import VendedoraForm, EstoqueVendedoraForm
from django.core.paginator import Paginator
from django.db.models import Q

def lista_vendedoras(request):
    search_query = request.GET.get('search', '')
    vendedoras = Vendedora.objects.all()

    if search_query:
        vendedoras = vendedoras.filter(
            Q(nome__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(cpf__icontains=search_query)
        )

    paginator = Paginator(vendedoras, 12)  # Mostrar 12 vendedoras por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'vendedoras': page_obj,
        'search_query': search_query,
    }
    return render(request, 'vendedoras/lista_vendedoras.html', context)

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
    estoque = EstoqueVendedora.objects.filter(vendedora=vendedora)
    return render(request, 'vendedoras/detalhe_vendedora.html', {'vendedora': vendedora, 'estoque': estoque})

def adicionar_estoque_vendedora(request, pk):
    vendedora = get_object_or_404(Vendedora, pk=pk)
    if request.method == 'POST':
        form = EstoqueVendedoraForm(request.POST)
        if form.is_valid():
            estoque = form.save(commit=False)
            estoque.vendedora = vendedora
            estoque.save()
            messages.success(request, 'Estoque atualizado com sucesso!')
            return redirect('vendedoras:detalhe_vendedora', pk=vendedora.pk)
    else:
        form = EstoqueVendedoraForm()
    return render(request, 'vendedoras/adicionar_estoque.html', {'form': form, 'vendedora': vendedora})

