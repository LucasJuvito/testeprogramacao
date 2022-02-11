from rest_framework import serializers
from pedidos import models

class PedidosSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pedidos
        fields = '__all__'
