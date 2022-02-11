from django.contrib import admin

from .models import Pedidos

# Register your models here.
@admin.register(Pedidos)
class PedidosAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "produto", "valor", "entregue", "timestamp")
