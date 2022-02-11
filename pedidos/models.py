from django.db import models

# Create your models here.
class Pedidos(models.Model):
    cliente = models.CharField(max_length=255)
    produto = models.CharField(max_length=255)
    valor = models.FloatField()
    entregue = models.BooleanField()
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cliente + ' ' + self.produto
