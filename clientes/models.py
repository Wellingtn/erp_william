from django.db import models

class Cliente(models.Model):
    foto = models.ImageField(upload_to='clientes/', blank=True, null=True)
    nome = models.CharField(max_length=100, default='', blank=True, null=True)
    cpf = models.CharField(max_length=20, default='', blank=True, null=True)
    rua = models.CharField(max_length=100, default='', blank=True, null=True)
    numero = models.CharField(max_length=20, default='', blank=True, null=True)
    bairro = models.CharField(max_length=100, default='', blank=True, null=True)
    cidade = models.CharField(max_length=100, default='', blank=True, null=True)
    uf = models.CharField(max_length=2, default='', blank=True, null=True)
    telefone1 = models.CharField(max_length=20, default='', blank=True, null=True)
    telefone2 = models.CharField(max_length=20, default='', blank=True, null=True)
    obs = models.TextField(default='', blank=True, null=True)

    def __str__(self):
        return self.nome or ''

    class Meta:
        ordering = ['nome']
        constraints = [
            models.UniqueConstraint(fields=['cpf'], condition=models.Q(cpf__isnull=False), name='unique_non_null_cpf')
        ]

