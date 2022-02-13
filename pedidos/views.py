from itertools import product
from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import Sum, Count
from django.core import serializers
from django.forms.models import model_to_dict
import json
import os

from .models import Pedido
from .forms import PedidoForm

# Create your views here.
class Manipularjson:
    def __init__(self):
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'pedidos.json')
    
        f = open(file_path, 'r')    #abrir json
        data = f.read()             #ler json
        f.close()
        data = json.loads(data)     #transferir para o formato de dicionário
        self.nextId = data["nextId"]
        self.pedidos = data["pedidos"]
        
        for i in self.pedidos:           #para cada pedido criar um objeto
            if i != None:
                pedido = Pedido(**i)
                pedido.save()
        

    # def escreverjson(self, data):
    #     f = open(path, "w")
    #     f.write(str(json.dumps(data)))
    #     f.close
    #     return data

    def getNextId(self):
        return self.__class__.nextId

    def getPedidos(self):
        return self.__class__.pedidos

def listar_pedidos(request):
    """ module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'pedidos.json')
    
    f = open(file_path, 'r')    #abrir json
    data = f.read()             #ler json
    f.close()
    data = json.loads(data)     #transferir para o formato de dicionário
    data = data['pedidos']      #pegar somente os pedidos
    
    for i in data:           #para cada pedido criar um objeto
        if i != None:
            pedido = Pedido(**i)
            pedido.save() """
    
    json_file = Manipularjson()

    pedidos = Pedido.objects.all()

    return render(request, 'pedidos.html', {'pedidos': pedidos})

from itertools import chain

def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data

def criar_pedido(request):
    form = PedidoForm(request.POST or None)

    if form.is_valid():
        form.save()

        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'pedidos.json')
    
        pedidos = Pedido.objects.all()

        data = []

        for pedido in pedidos:
            data.append(to_dict(pedido))

        with open(file_path, 'w', encoding='utf8') as json_file:
            json_file.write("{\"pedidos\": ")

        with open(file_path, 'a', encoding='utf8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, default=str)
            json_file.write("}")
        
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