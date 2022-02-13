from itertools import product
from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import Sum, Count
from .models import Pedido
from .forms import PedidoForm
import json

# Create your views here.
""" class Manipularjson:

    nextId = 0
    pedidos = []

    def lerjson(path):
        f = open(path, 'r')
        data = f.read()
        data = json.loads(data)
        #self.__class__.nextId = data["nextId"]
        #self.__class__.pedidos = data["pedidos"]
        
        for i in data["pedidos"]:
            i = Pedido(i)
        f.close
        return data

    def escreverjson(path, data):
        f = open(path, "w")
        f.write(str(json.dumps(data)))
        f.close
        return data

    def getNextId(self):
        return self.__class__.nextId

    def getPedidos(self):
        return self.__class__.pedidos
 """
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
    try:
        pedido = Pedido.objects.get(id=id)
    except Pedido.DoesNotExist:
        raise Http404(f"O pedido com id: {id} não existe")

    form = PedidoForm(request.POST or None, instance=pedido)

    if form.is_valid():
        form.save()
        return redirect('listar_pedidos')

    return render(request, 'pedidos-form.html', {'form': form, 'pedido': pedido})

def apagar_pedido(request, id):
    try:
        pedido = Pedido.objects.get(id=id)
    except Pedido.DoesNotExist:
        raise Http404(f"O pedido com id: {id} não existe")
        

    if request.method == 'POST':
        pedido.delete()
        return redirect('listar_pedidos')

    return render(request, 'confirmar-delete.html', {'pedido': pedido})

def valor_total_por_cliente(request, cliente):
    try:
        pedidos = Pedido.objects.filter(cliente=cliente)
    except Pedido.DoesNotExist:
        raise Http404(f"Cliente não encontrado")

    contador = pedidos.count()
    valor = pedidos.filter(entregue=True)
    valor = valor.aggregate(Sum('valor'))['valor__sum']
    if valor == None:
        valor = 0

    return render(request, 'pedidos-cliente.html', {'pedidos': pedidos, 'contador': contador, 'valor':valor, 'cliente':cliente})

def valor_total_por_produto(request, produto):
    try:
        pedidos = Pedido.objects.filter(produto=produto)
    except Pedido.DoesNotExist:
        raise Http404(f"Produto não encontrado")

    contador = pedidos.count()
    valor = pedidos.filter(entregue=True)
    valor = valor.aggregate(Sum('valor'))['valor__sum']
    if valor == None:
        valor = 0

    return render(request, 'pedidos-produto.html', {'pedidos': pedidos, 'contador': contador, 'valor':valor, 'produto':produto})

def mais_vendidos(request):
    pedidos = Pedido.objects.values('produto')
    pedidos = pedidos.filter(entregue=True)
    pedidos = pedidos.annotate(pcount=Count('produto')).order_by('-pcount')

    return render(request, 'produtos.html', {'pedidos': pedidos})