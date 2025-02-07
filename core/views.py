from django.shortcuts import render, redirect
from django.db.models import Sum, Count
from estoque.models import Produto
from vendas.models import Venda
from vendedoras.models import Vendedora
from clientes.models import Cliente
from django.contrib.auth import logout


def dashboard(request):
    total_produtos = Produto.objects.count()
    total_vendas = Venda.objects.count()
    total_vendedoras = Vendedora.objects.count()
    total_clientes = Cliente.objects.count()
    
    valor_total_vendas = Venda.objects.aggregate(total=Sum('total'))['total'] or 0
    
    produtos_baixo_estoque = Produto.objects.filter(quantidade__lt=10).count()
    
    context = {
        'total_produtos': total_produtos,
        'total_vendas': total_vendas,
        'total_vendedoras': total_vendedoras,
        'total_clientes': total_clientes,
        'valor_total_vendas': valor_total_vendas,
        'produtos_baixo_estoque': produtos_baixo_estoque,
    }
    
    return render(request, 'core/dashboard.html', context)


def logout_view(request):
    logout(request)
    return redirect('core:dashboard')
