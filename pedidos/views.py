from itertools import product
from django.shortcuts import render, redirect
from .models import Pedido
from .forms import PedidoForm

# Create your views here.
def listar_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedidos.html', {'pedidos': pedidos})

def criar_pedido(request):
    form = PedidoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('listar_pedidos')

    return render(request, 'pedidos-form.html', {'form': form})

def atualizar_pedido(request, id):
    pedido = Pedido.objects.get(id=id)
    form = PedidoForm(request.POST or None, instance=pedido)

    if form.is_valid():
        form.save()
        return redirect('listar_pedidos')

    return render(request, 'pedidos-form.html', {'form': form, 'pedido': pedido})

def apagar_pedido(request, id):
    pedido = Pedido.objects.get(id=id)

    if request.method == 'POST':
        pedido.delete()
        return redirect('listar_pedidos')

    return render(request, 'confirmar-delete.html', {'pedido': pedido})