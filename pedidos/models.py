from django.db import models
import json

# Create your models here.
class Pedido(models.Model):
    cliente = models.CharField(max_length=255)
    produto = models.CharField(max_length=255)
    valor = models.FloatField()
    entregue = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id + '-' + self.cliente + '-' + self.produto
