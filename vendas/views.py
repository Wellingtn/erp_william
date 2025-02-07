from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Venda, ItemVenda
from .forms import VendaForm, ItemVendaFormSet
from estoque.models import Produto
from decimal import Decimal
import logging
import json

# Configurar logging
logger = logging.getLogger(__name__)

def lista_vendas(request):
    vendas = Venda.objects.all().order_by('-data')
    return render(request, 'vendas/lista_vendas.html', {'vendas': vendas})

@transaction.atomic
def nova_venda(request):
    if request.method == 'POST':
        form = VendaForm(request.POST)
        formset = ItemVendaFormSet(request.POST)
        logger.debug(f"POST data: {request.POST}")
        
        if form.is_valid() and formset.is_valid():
            logger.debug("Form and formset are valid")
            
            venda = form.save(commit=False)
            venda.total = Decimal('0.00')
            venda.save()
            logger.debug(f"Venda saved with id: {venda.id}")
            
            formset.instance = venda
            logger.debug(f"Formset before saving: {formset.forms}")
            
            itens = formset.save(commit=False)
            logger.debug(f"Itens before saving: {itens}")
            
            total = Decimal('0.00')
            for item in itens:
                item.venda = venda
                produto = item.produto
                if produto.quantidade >= item.quantidade:
                    produto.quantidade -= item.quantidade
                    produto.save()
                    item.save()
                    total += item.quantidade * item.preco_unitario
                    logger.debug(f"Item saved: {item.id}, produto: {item.produto}, quantidade: {item.quantidade}, preço: {item.preco_unitario}")
                else:
                    messages.error(request, f'Quantidade insuficiente para o produto {produto.nome}')
                    venda.delete()
                    return render(request, 'vendas/form_venda.html', {'form': form, 'formset': formset})
            
            venda.total = total
            venda.save()
            logger.debug(f"Venda updated with total: {venda.total}")
            
            messages.success(request, 'Venda registrada com sucesso!')
            return redirect('vendas:lista_vendas')
        else:
            logger.error(f"Form errors: {form.errors}")
            logger.error(f"Formset errors: {formset.errors}")
            messages.error(request, 'Erro ao registrar a venda. Por favor, verifique os dados.')
    else:
        form = VendaForm()
        formset = ItemVendaFormSet()
    
    produtos = Produto.objects.filter(quantidade__gt=0)
    produtos_json = json.dumps({str(p.id): str(p.preco) for p in produtos})
    return render(request, 'vendas/form_venda.html', {
        'form': form,
        'formset': formset,
        'produtos': produtos,
        'produtos_json': produtos_json
    })

def detalhe_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    itens = ItemVenda.objects.filter(venda=venda)
    return render(request, 'vendas/detalhe_venda.html', {'venda': venda, 'itens': itens})

@transaction.atomic
def editar_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    if request.method == 'POST':
        form = VendaForm(request.POST, instance=venda)
        formset = ItemVendaFormSet(request.POST, instance=venda)
        if form.is_valid() and formset.is_valid():
            venda = form.save(commit=False)
            
            # Dicionário para armazenar todos os itens
            itens_venda = {}
            
            # Processar os itens do formset
            for form in formset:
                if form.is_valid() and form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    item = form.save(commit=False)
                    produto_id = str(item.produto.id)
                    
                    if produto_id in itens_venda:
                        itens_venda[produto_id]['quantidade'] += item.quantidade
                    else:
                        itens_venda[produto_id] = {
                            'produto': item.produto,
                            'quantidade': item.quantidade,
                            'preco_unitario': item.preco_unitario
                        }
            
            # Verificar estoque e salvar itens
            for item_data in itens_venda.values():
                produto = item_data['produto']
                quantidade = item_data['quantidade']
                preco_unitario = item_data['preco_unitario']
                
                if produto.quantidade >= quantidade:
                    produto.quantidade -= quantidade
                    produto.save()
                    
                    item_venda, created = ItemVenda.objects.update_or_create(
                        venda=venda,
                        produto=produto,
                        defaults={
                            'quantidade': quantidade,
                            'preco_unitario': preco_unitario
                        }
                    )
                else:
                    messages.error(request, f'Quantidade insuficiente para o produto {produto.nome}')
                    return render(request, 'vendas/form_venda.html', {'form': form, 'formset': formset, 'venda': venda})
            
            # Remover itens que foram excluídos
            for obj in formset.deleted_objects:
                obj.produto.quantidade += obj.quantidade
                obj.produto.save()
                obj.delete()
            
            venda.save()
            venda.calcular_total()
            messages.success(request, 'Venda atualizada com sucesso!')
            return redirect('vendas:lista_vendas')
        else:
            messages.error(request, 'Erro ao atualizar a venda. Por favor, verifique os dados.')
    else:
        form = VendaForm(instance=venda)
        formset = ItemVendaFormSet(instance=venda)
    
    produtos = Produto.objects.filter(quantidade__gt=0)
    produtos_json = json.dumps({str(p.id): str(p.preco) for p in produtos})
    return render(request, 'vendas/form_venda.html', {
        'form': form,
        'formset': formset,
        'venda': venda,
        'produtos': produtos,
        'produtos_json': produtos_json
    })

def excluir_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    if request.method == 'POST':
        venda.delete()
        messages.success(request, 'Venda excluída com sucesso!')
        return redirect('vendas:lista_vendas')
    return render(request, 'vendas/confirmar_exclusao.html', {'venda': venda})

