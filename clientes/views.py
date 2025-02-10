from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Cliente
from .forms import ClienteForm
from vendas.models import Venda
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def lista_clientes(request):
    search_query = request.GET.get('search', '')
    if search_query:
        clientes_list = Cliente.objects.filter(
            Q(nome__icontains=search_query) |
            Q(cpf__icontains=search_query) |
            Q(telefone1__icontains=search_query) |
            Q(telefone2__icontains=search_query)
        ).order_by('nome')
    else:
        clientes_list = Cliente.objects.all().order_by('nome')

    paginator = Paginator(clientes_list, 9)  # Mostrar 9 clientes por página
    page = request.GET.get('page')
    try:
        clientes = paginator.page(page)
    except PageNotAnInteger:
        clientes = paginator.page(1)
    except EmptyPage:
        clientes = paginator.page(paginator.num_pages)

    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})



def adicionar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('clientes:lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/adicionar_cliente.html', {'form': form})



def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('clientes:lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/form_cliente.html', {'form': form, 'cliente': cliente})

def detalhe_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    vendas = Venda.objects.filter(cliente=cliente).order_by('-data')
    
    paginator = Paginator(vendas, 9)  # Mostrar 10 vendas por página
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Se a página não for um inteiro, exiba a primeira página
        page_obj = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo (por exemplo, 9999), exiba a última página
        page_obj = paginator.page(paginator.num_pages)
    
    return render(request, 'clientes/detalhe_cliente.html', {
        'cliente': cliente,
        'page_obj': page_obj,
    })


def vendas_cliente(request, pk):
    cliente = get_object_or_404(Cliente, id=pk)
    vendas = Venda.objects.filter(cliente=cliente).order_by('-data')
    
    paginator = Paginator(vendas, 9)  # Mostrar 10 vendas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    vendas_data = []
    for venda in page_obj:
        vendas_data.append({
            'id': venda.id,
            'data': venda.data.strftime('%d/%m/%Y'),
            'total': str(venda.total),
            'finalizada': venda.finalizada,
            'itens': [
                {
                    'produto_nome': item.produto.nome,
                    'quantidade': item.quantidade,
                    'subtotal': str(item.subtotal)
                } for item in venda.itens.all()
            ]
        })
    
    return JsonResponse({
        'vendas': vendas_data,
        'has_next': page_obj.has_next(),
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
    })

