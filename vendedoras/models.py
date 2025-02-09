from django.db import models
from estoque.models import Produto

class Vendedora(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nome

class EstoqueVendedora(models.Model):
    vendedora = models.ForeignKey(Vendedora, on_delete=models.CASCADE, related_name='estoque')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)

    class Meta:
        unique_together = ('vendedora', 'produto')

    def __str__(self):
        return f"{self.vendedora.nome} - {self.produto.nome}: {self.quantidade}"

