from xml.etree.ElementInclude import include
from django.urls import path

from rest_framework import routers

from pedidos.api import viewsets

app_name = "pedidos"

router = routers.DefaultRouter()

router.register(r'pedidos', viewsets.PedidosViewSet)

urlpatterns = router.urls