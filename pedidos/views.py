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

nextIdG = 0
pedidosG = []
json_fileG = None
file_pathG = ''

# Create your views here.
class Manipularjson:
    def __init__(self):
        global nextIdG, pedidosG, file_pathG
        self.module_dir = os.path.dirname(__file__)  # get current directory
        self.file_path = os.path.join(self.module_dir, 'pedidos.json')
        file_pathG = self.file_path

        f = open(self.file_path, 'r')    #abrir json
        data = f.read()             #ler json
        f.close()
        data = json.loads(data)     #transferir para o formato de dicionário

        nextIdG = data["nextId"]
        pedidosG = data["pedidos"]

        
        for i in pedidosG:           #para cada pedido criar um objeto
            if i != None:
                pedido = Pedido(**i)
                pedido.save()
        
    def escrever():
        global nextIdG, pedidosG, json_fileG, file_pathG
       
        with open(file_pathG, 'w', encoding='utf8') as json_file:
            json_file.write("{ \"nextId\": ")
            json_file.write(f"{nextIdG}, ")
            json_file.write("\"pedidos\": ")

        with open(file_pathG, 'a', encoding='utf8') as json_file:
            data = []
            """ for i in pedidosG:
                i["timestamp"] = datetime.fromtimestamp(i["timestamp"]) """
            json.dump(pedidosG, json_file, ensure_ascii=False, default=str)
            json_file.write("}") 

    def adicionar():
        global nextIdG, pedidosG, json_fileG
        data = Pedido.objects.last()                            #pega o último objeto salvo de Pedido
        data = Pedido.objects.filter(id=data.id).values()[0]    #transforma o objeo em um dicionário

        nextIdG += 1
        pedidosG.append(data) #adiciona no final da lista de pedidos
        #self.escrever() #chama a função para escrever no jason

    def atualizar(id):
        global nextIdG, pedidosG, json_fileG
        data = Pedido.objects.get(id=id)                        #pega o último objeto salvo de Pedido
        data = Pedido.objects.filter(id=data.id).values()[0]    #transforma o objeo em um dicionário

        for i, item in enumerate(pedidosG):
            if item["id"] == id:
                pedidosG[i] = data #adiciona na lista de pedidos
                break
        #self.escrever() #chama a função para escrever no jason    

    def apagar(id):
        global nextIdG, pedidosG, json_fileG
        data = Pedido.objects.get(id=id)                        #pega o último objeto salvo de Pedido
        data = Pedido.objects.filter(id=data.id).values()[0]    #transforma o objeo em um dicionário

        for i, item in enumerate(pedidosG):
            if item["id"] == id:
                pedidosG.pop(i) #adiciona na lista de pedidos
                break
        #self.escrever() #chama a função para escrever no jason    
    

    def getNextId(self):
        return self.nextId

    def getPedidos(self):
        return self.pedidos



def listar_pedidos(request):
    global json_fileG
    json_fileG = Manipularjson()
    pedidos = Pedido.objects.all()

    return render(request, 'pedidos.html', {'pedidos': pedidos})

def criar_pedido(request):
    global json_fileG
    form = PedidoForm(request.POST or None)

    if form.is_valid():
        try:
            form.save()
            Manipularjson.adicionar()
            Manipularjson.escrever()
        except:
           raise Http404(f"Não foi possível criar o pedido")
        
        return redirect('listar_pedidos')

    return render(request, 'pedidos-form.html', {'form': form})

def atualizar_pedido(request, id):
    try:
        pedido = Pedido.objects.get(id=id)
    except Pedido.DoesNotExist:
        raise Http404(f"O pedido com id: {id} não existe")

    form = PedidoForm(request.POST or None, instance=pedido)

    if form.is_valid():
        try:
            form.save()
            Manipularjson.atualizar(id)
            Manipularjson.escrever()
        except:
           raise Http404("Não foi possível atualizar o pedido")
        return redirect('listar_pedidos')
        

    return render(request, 'pedidos-form.html', {'form': form, 'pedido': pedido})

def apagar_pedido(request, id):
    try:
        pedido = Pedido.objects.get(id=id)
    except Pedido.DoesNotExist:
        raise Http404(f"O pedido com id: {id} não existe")
        

    if request.method == 'POST':
        try:
            Manipularjson.apagar(id)
            Manipularjson.escrever()
            pedido.delete()
        except:
            raise Http404("Não foi possível apagar o pedido")
        
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