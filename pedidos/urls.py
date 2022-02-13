""" from xml.etree.ElementInclude import include
from django.urls import path

from rest_framework import routers

from pedidos.api import viewsets

app_name = "pedidos"

router = routers.DefaultRouter()

router.register(r'pedidos', viewsets.PedidosViewSet)

urlpatterns = router.urls """

from django.urls import path
from .views import listar_pedidos, criar_pedido, atualizar_pedido, apagar_pedido, valor_total_por_cliente, valor_total_por_produto, mais_vendidos

urlpatterns = [
    path('', listar_pedidos, name='listar_pedidos'),
    path('novo', criar_pedido, name='criar_pedido'),
    path('atualizar/<int:id>/', atualizar_pedido, name='atualizar_pedido'),
    path('apagar/<int:id>/', apagar_pedido, name='apagar_pedido'),
    path('cliente/<str:cliente>/', valor_total_por_cliente, name="valor_total_por_cliente"),
    path('produto/<str:produto>/', valor_total_por_produto, name="valor_total_por_produto"),
    path('produtos/maisvendidos', mais_vendidos, name='mais_vendidos'),
]