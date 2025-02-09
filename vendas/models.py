from django.db import models
from clientes.models import Cliente
from estoque.models import Produto
from decimal import Decimal

class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    data = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    finalizada = models.BooleanField(default=False)

    def __str__(self):
        return f"Venda {self.id} para {self.cliente.nome}"

    def adicionar_item(self, produto, quantidade):
        item, created = ItemVenda.objects.get_or_create(
            venda=self,
            produto=produto,
            defaults={'quantidade': quantidade, 'preco_unitario': produto.preco}
        )
        if not created:
            item.quantidade += quantidade
            item.save()
        self.atualizar_total()

    def atualizar_total(self):
        self.total = sum(item.subtotal for item in self.itens.all())
        self.save()

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} na Venda {self.venda.id}"

