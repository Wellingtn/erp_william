from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Venda, ItemVenda
from estoque.models import Produto
from clientes.models import Cliente
from decimal import Decimal

# from django.contrib.auth.decorators import login_required

def lista_produtos(request):
    produtos = Produto.objects.filter(quantidade__gt=0)
    return render(request, 'vendas/lista_produtos.html', {'produtos': produtos})

def iniciar_venda(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        cliente = get_object_or_404(Cliente, id=cliente_id)
        venda = Venda.objects.create(cliente=cliente)
        return redirect('vendas:adicionar_produto', venda_id=venda.id)
    clientes = Cliente.objects.all()
    return render(request, 'vendas/iniciar_venda.html', {'clientes': clientes})

# Continue removendo @login_required de todas as outras funções...

def adicionar_produto(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id, finalizada=False)
    if request.method == 'POST':
        produto_id = request.POST.get('produto')
        quantidade = int(request.POST.get('quantidade', 1))
        produto = get_object_or_404(Produto, id=produto_id)
        
        if produto.quantidade >= quantidade:
            venda.adicionar_item(produto, quantidade)
            produto.quantidade -= quantidade
            produto.save()
            messages.success(request, f"{quantidade}x {produto.nome} adicionado à venda.")
        else:
            messages.error(request, f"Estoque insuficiente para {produto.nome}.")
        
        return redirect('vendas:adicionar_produto', venda_id=venda.id)
    
    produtos = Produto.objects.filter(quantidade__gt=0)
    return render(request, 'vendas/adicionar_produto.html', {'venda': venda, 'produtos': produtos})

def finalizar_venda(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id, finalizada=False)
    if request.method == 'POST':
        venda.finalizada = True
        venda.save()
        messages.success(request, f"Venda {venda.id} finalizada com sucesso!")
        return redirect('vendas:detalhe_venda', venda_id=venda.id)
    return render(request, 'vendas/finalizar_venda.html', {'venda': venda})

def detalhe_venda(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)
    return render(request, 'vendas/detalhe_venda.html', {'venda': venda})



def lista_vendas(request):
    vendas = Venda.objects.all().order_by('-data')
    return render(request, 'vendas/lista_vendas.html', {'vendas': vendas})

