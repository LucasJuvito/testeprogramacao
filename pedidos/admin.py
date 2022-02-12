from django.contrib import admin

from .models import Pedido

# Register your models here.
@admin.register(Pedido)
class PedidosAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "produto", "valor", "entregue", "timestamp")
