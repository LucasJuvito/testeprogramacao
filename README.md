# delivery-api

Está é uma api para controle de pedidos feita em **python/django**. É a minha primeira experiência com **django** e com **docker** e o desafio foi grande, aprender algo novo em pouco tempo não é fácil! Mas apesar de tudo, estou ansioso para aprofundar nessa área.

## Como utilizar a api
### Primeiros passos
1. Faça o download dos arquivos deste repositório e os deixem juntos numa mesma pasta. 
2. Abra o terminal na pasta que estão os arquivos baixados.
3. Se você já tem o **docker** instalado basta usar o comando `docker-compose up` e esperar que a aplicação já estará rodando com tudo que é necessário. Caso não tenha o **docker** instalado você pode acessar o site  [docker.com/get-started](https://www.docker.com/get-started)  que irá guiar sua instalação.
4. Abra o navegador de sua preferência e acesse [localhost:8000](http://localhost:8000) e espere até que a página esteja completamente carregada.

### Interação
 1. Se você seguiu os passos corretamente, uma lista com vários pedidos irão aparecer na tela.
 2. Para criar um novo pedido procure por um botão chamado "Novo Pedido".
 3. Para interagir com um pedido basta clicar sobre ele.
 4. É possível alterar os campos visíveis, para salvar as alterações clique  em "salvar".
 5. É possível verificar todos os pedidos realizados pelo cliente que fez o pedido, para isso procure por um botão chamado "Buscar pedidos desde cliente".
 6. Também é possível verificar todos os pedidos feitos com esse produto, para isso procure por um botão chamado "Buscar pedidos com esse produto".
 7. Para apagar o pedido, procure por um botão chamado "Apagar".
 8. Para listar os produtos mais vendidos procure por um botão chamado "Mais vendidos".

### Observações
1. O arquivo "pedidos.json" na pasta pedidos contém os dados iniciais usados nesta api e toda alteração com o banco realizada na aplicação irá atualizar esse arquivo.
2. Caso algum problema aconteça durante a execução, um erro será lançado descrevendo qual o problema. 
3. Caso o problema esteja relacionado ao banco, verifique se o arquivo "pedidos.json" está correto. Antes de reiniciar a aplicação apague o arquivo "db.sqlite3" e qualquer outro que tenha surgido por causa dele como um "Journal", isso garantirá que não haverá conflitos entre o arquivo "pedidos.json" e o banco de dados.
