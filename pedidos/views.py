from itertools import product
from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import Sum, Count
from django.core import serializers
from django.forms.models import model_to_dict
import json
import os
from datetime import date, datetime

from .models import Pedido
from .forms import PedidoForm
from .manipularjson import ManipularJson

manipulador = None

#view que lista todos os pedidos
def listar_pedidos(request):
    global manipulador
    if manipulador is None:
        manipulador = ManipularJson()
    
    pedidos = Pedido.objects.all()

    return render(request, 'pedidos.html', {'pedidos': pedidos})

#view que cria um novo pedido
def criar_pedido(request):
    global manipulador
    if manipulador is None:
        manipulador = ManipularJson()
    
    form = PedidoForm(request.POST or None)

    if form.is_valid():
        try:
            form.save()
            manipulador.adicionar()
            manipulador.escrever()
        except:
           raise Http404(f"Não foi possível criar o pedido")
        
        return redirect('listar_pedidos')

    return render(request, 'pedidos-form.html', {'form': form})

#view que atualiza um pedido já existente pelo seu id
def atualizar_pedido(request, id):
    global manipulador
    if manipulador is None:
        manipulador = ManipularJson()
    
    try:
        pedido = Pedido.objects.get(id=id)
    except Pedido.DoesNotExist:
        raise Http404(f"O pedido com id: {id} não existe")

    form = PedidoForm(request.POST or None, instance=pedido)

    if form.is_valid():
        try:
            form.save()
            manipulador.atualizar(id)
            manipulador.escrever()
        except Exception as e:
            print(e)
            raise Http404("Não foi possível atualizar o pedido")
        return redirect('listar_pedidos')
        
    return render(request, 'pedidos-form.html', {'form': form, 'pedido': pedido})

#view que apaga um pedido existente pelo seu id
def apagar_pedido(request, id):
    global manipulador
    if manipulador is None:
        manipulador = ManipularJson()
    
    try:
        pedido = Pedido.objects.get(id=id)
    except Pedido.DoesNotExist:
        raise Http404(f"O pedido com id: {id} não existe")     

    if request.method == 'POST':
        try:
            print("apagando")
            manipulador.apagar(id)
            print("escrevendo")
            manipulador.escrever()
            print("deletando")
            pedido.delete()
        except Exception as e:
            print(e)
            raise Http404("Não foi possível apagar o pedido")
        
        return redirect('listar_pedidos')

    return render(request, 'confirmar-delete.html', {'pedido': pedido})

#view que calcula o valor total de pedidos entregues de um cliente
def valor_total_por_cliente(request, cliente):
    try:
        pedidos = Pedido.objects.filter(cliente=cliente)
    except Pedido.DoesNotExist:
        raise Http404(f"Cliente não encontrado")

    contador = pedidos.count()
    valor = pedidos.filter(entregue=True)
    contador_entregue = valor.count()
    valor = valor.aggregate(Sum('valor'))['valor__sum']
    if valor == None:
        valor = 0

    return render(request, 'pedidos-cliente.html', {'pedidos': pedidos, 'contador': contador, 'contador_entregue': contador_entregue, 'valor':valor, 'cliente':cliente})

#view que calcula o valor total de pedidos entregues de um produto
def valor_total_por_produto(request, produto):
    try:
        pedidos = Pedido.objects.filter(produto=produto)
    except Pedido.DoesNotExist:
        raise Http404(f"Produto não encontrado")

    contador = pedidos.count()
    valor = pedidos.filter(entregue=True)
    contador_entregue = valor.count()
    valor = valor.aggregate(Sum('valor'))['valor__sum']
    if valor == None:
        valor = 0

    return render(request, 'pedidos-produto.html', {'pedidos': pedidos, 'contador': contador, 'contador_entregue': contador_entregue, 'valor':valor, 'produto':produto})

#view lista em ordem decrescente os pedidos entregues mais vendidos
def mais_vendidos(request):
    pedidos = Pedido.objects.values('produto')
    pedidos = pedidos.filter(entregue=True)
    pedidos = pedidos.annotate(pcount=Count('produto')).order_by('-pcount')

    return render(request, 'produtos.html', {'pedidos': pedidos})