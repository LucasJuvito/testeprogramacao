from django.db import models
import json

# Create your models here.
""" class manipularjson:

    nextId = 0
    pedidos = []

    def lerjson(self, path):
        f = open(path, 'r')
        data = f.read()
        data = json.loads(data)
        self.__class__.nextId = data["nextId"]
        self.__class__.pedidos = data["pedidos"]
        f.close
        return data

    def escreverjson(path, data):
        f = open(path, "w")
        f.write(str(json.dumps(data)))
        f.close
        return data """

class Pedido(models.Model):
    cliente = models.CharField(max_length=255)
    produto = models.CharField(max_length=255)
    valor = models.FloatField()
    entregue = models.BooleanField()
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.id + '-' + self.cliente + '-' + self.produto

