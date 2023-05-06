## CINtofome - Sistema de Pedidos de Restaurante

CINtofome é um sistema simples de gerenciamento de pedidos de restaurante, implementado em Python. Ele permite que os clientes façam pedidos, consultem o cardápio, visualizem suas contas individuais e a conta da mesa, e efetuem o pagamento.

### Requisitos

- Python 3.7 ou superior

### Instalação

1. Clone o repositório ou baixe o arquivo ZIP e descompacte-o.
2. Navegue até o diretório do projeto no terminal ou prompt de comando.
3. Execute o servidor com `python server.py`.
4. Em outra janela do terminal, execute o cliente com `python client.py`.

### Como usar

1. Inicie o servidor e o cliente conforme descrito na seção de instalação.
2. No cliente, digite "chefia" para iniciar o sistema.
3. Siga as instruções exibidas no cliente para interagir com o sistema.

## Documentação

### Estrutura do projeto

O projeto consiste em dois arquivos principais:

- `server.py`: Contém o código do servidor, responsável por gerenciar as mesas, pedidos e contas.
- `client.py`: Contém o código do cliente, que interage com o servidor para realizar ações, como fazer pedidos e pagar a conta.

### Classes

- `Rdt`: Classe que abstrai a conexão entre o servidor e o cliente, usando os princípios de RDT 3.0.
- `ContaIndividual`: Classe que representa a conta individual de um cliente.
- `Mesa`: Classe que representa uma mesa no restaurante e contém uma lista de `ContaIndividual`.

### Funções

- `get_time()`: Retorna a hora atual formatada como HH:MM.
- `table_bill(mesa)`: Gera a conta da mesa no formato de uma string.
- `individual_bill(index, nome)`: Gera a conta individual de um cliente no formato de uma string.
- `bill_verify(valor, mesa, nome)`: Verifica se um valor de pagamento é suficiente para cobrir a conta de um cliente.
- `save_request(mesa: dict, nome: str, pedido: str)`: Salva um pedido na conta de um cliente.
- `sum_bill(nome, mesa)`: Calcula a soma das contas individuais e da mesa.
- `main()`: Função principal que inicia o servidor e lida com as interações com o cliente.

### Variáveis e constantes

- `opcoes`: Texto com as opções disponíveis para o cliente.
- `respostasPorExtenso`: Lista com as opções de resposta por extenso.
- `cardapio`: Texto com o cardápio do restaurante.
- `cardapioPorExtenso`: Lista com os itens do cardápio por extenso.
- `negacoes`: Lista com as negações possíveis.

### Fluxo do programa

1. O servidor é iniciado e aguarda a conexão do cliente.
2. O cliente se conecta ao servidor e inicia a interação.
3. O cliente envia comandos para o servidor, que processa as solicitações e retorna os resultados.
4. O cliente e o servidor continuam interagindo até que o cliente decida sair.

## Equipe

- José Daniel da Silva Carmo
- Marcelo Vinícius Bastos Santos
- Giovanny Lira de Araújo Cunha
- João Pedro de Albuquerque Maranhão Marinho
- Antônio Gabriel dos Santos Clemente
