import os
import json
from .models import Pedido

# classe com funções para manipular o json
class ManipularJson:
    nextId = 0
    pedidos = []
    file_path = ''
    
    def __init__(self):
        module_dir = os.path.dirname(__file__)                     # pega o diretório atual
        self.file_path = os.path.join(module_dir, 'pedidos.json')  # salva o caminho do arquivo json

        f = open(self.file_path, 'r')   #abrir json
        data = f.read()                 #ler json
        f.close()
        data = json.loads(data)         #transferir para o formato de dicionário

        self.nextId = data["nextId"]
        self.pedidos = data["pedidos"]

        for i in self.pedidos:              #para cada pedido criar um objeto
            bandeira = True
            if i != None:
                for key in ["id", "cliente", "produto", "valor", "entregue", "timestamp"]:
                    if key not in i or i[key] == None:
                        bandeira = False
                
                if bandeira:
                    pedido = Pedido(**i)
                    pedido.save()
    
    #função para escrever o json após alterações
    def escrever(self):        
        with open(self.file_path, 'w', encoding='utf8') as json_file:
            json_file.write("{ \"nextId\": ")
            json_file.write(f"{self.nextId}, ")
            json_file.write("\"pedidos\": ")

        with open(self.file_path, 'a', encoding='utf8') as json_file:
            json.dump(self.pedidos, json_file, ensure_ascii=False, default=str)
            json_file.write("}") 

    #função para adicionar novos pedidos na lista que irá para o json
    def adicionar(self):
        data = Pedido.objects.last()                            #pega o último objeto salvo de Pedido
        data = Pedido.objects.filter(id=data.id).values()[0]    #transforma o objeto em um dicionário

        self.nextId += 1            #incrementa o nextId
        self.pedidos.append(data)   #adiciona no final da lista de pedidos

    #função para atualizar um pedido na lista de pedidos que irá para o json
    def atualizar(self, id):
        data = Pedido.objects.get(id=id)                        #pega o objeto com id passado
        data = Pedido.objects.filter(id=data.id).values()[0]    #transforma o objeto em um dicionário

        for i, item in enumerate(self.pedidos):     #adiciona na lista de pedidos no local do antigo
            if item == None:
                continue
            if item["id"] == id:
                self.pedidos[i] = data 
                break

    #função para apagar um pedido na lista de pedidos que irá para o json
    def apagar(self, id):

        for i, item in enumerate(self.pedidos):     #Deleta da lista de pedidos
            if item == None:
                continue
            if item["id"] == id:
                self.pedidos.pop(i)
                break
