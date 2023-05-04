from rdt import *

cardapio = {"Churrasco Misto": 45.00, "Parmegiana": 20.00, "Filé Mignon": 30,\
             "Risoto de Camarão": 25, "Salmão Grelhado": 35, "Feijoada": 18, \
                "Lasanha": 22, "Picanha": 40, "Espaguete à Carbonara": 28, "Pizza Margherita": 25}

mesas = {"1": {"Vítor Azevedo": ["Parmegiana"], "Felipe Maltez": ["Lasanha"]}}

def table_bill(mesa):
    total_mesa = 0.0 # variável para armazenar o total da mesa
    
    # cabeçalho da conta
    saida = "\n"
    for nome_cliente in mesa:
        saida += "| {} |\n\n".format(nome_cliente)
    
    # itera pelos pedidos de cada cliente
    for nome_cliente, pedidos in mesa.items():
        saida += "{:<20}{:>10}\n".format("Item", "Preço")
        saida += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n"
        
        # itera pelos itens pedidos pelo cliente e calcula o total da conta dele
        total_cliente = 0.0
        for item in pedidos:
            preco = cardapio.get(item)
            if preco is not None:
                saida += "{:<20}{:>10.2f}\n".format(item, preco)
                total_cliente += preco
        saida += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n"
        
        # adiciona o total do cliente ao total da mesa
        saida += "Total - R$ {:,.2f}\n".format(total_cliente)
        saida += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n\n"
        total_mesa += total_cliente
    
    # total da mesa
    saida += "Total da mesa - R$ {:,.2f}\n".format(total_mesa)
    saida += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n"
    
    return saida

def individual_bill(mesa, nome):
    total = 0
    pedidos = mesa.get(nome, [])
    
    if not pedidos:
        return "Não foram encontrados pedidos para este cliente."
    
    linha = f"| {nome} |\n"
    for pedido in pedidos:
        preco = cardapio.get(pedido, 0)
        linha += f"{pedido} => R$ {preco:.2f}\n"
        total += preco
    
    linha += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-"
    linha += f"\nTotal - R$ {total:.2f}\n"
    linha += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-"
    
    return linha

def bill_verify(valor, mesa, nome):
    total = 0
    pedidos = mesa[nome]
    for pedido in pedidos:
        total += cardapio[pedido]
    if (valor >= total):
        mesa.pop(nome)
        return valor - total, True
    else:
        return total - valor, False

def save_request(mesa, nome, pedido):
    if nome in mesa:
        mesa[nome].append(pedido)
        print(f"Pedido {pedido} adicionado para {nome} na mesa.")

def isDigit(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def main():
    # Conexão foi abstraída para a classe Rdt
    servidor = Rdt('server')
    # No qual fornece uma conexão UDT com os príncipios de RDT3.0

    while True:
        print('Conexão estabelecida com o cliente')
        servidor.reset_num_seq()

        # Recebe uma mensagem do cliente
        clientMessage = servidor.rdt_rcv()['data']

        if (clientMessage.decode('utf-8') == 'chefia'):
            tableNumber = 'Recebe número.'
            print("Aguardando número do usuário.")
            # Verificar se a mensagem foi um número:
            while (isDigit(tableNumber)):
                servidor.rdt_send('Digite sua mesa'.encode('utf-8'))
                clientMessage = servidor.rdt_rcv()['data']
                tableNumber = clientMessage.decode('utf-8')
            
            servidor.rdt_send("Digite seu nome".encode('utf-8'))
            clientMessage = servidor.rdt_rcv()['data']
            name = clientMessage.decode('utf-8')

            if (mesas.get(tableNumber) == None):
                mesas.append({tableNumber: {name: []}})
            else:
                mesas[tableNumber].append({name: []})

            print("Mesa criada, usuário adicionado.")
            while (True):
                servidor.rdt_send(opcoes.encode('utf-8'))
                clientMessage = servidor.rdt_rcv()['data']
                options = clientMessage.decode('utf-8')

                table = mesas.get(tableNumber)

                if (options in respostasPorExtenso or (isDigit(options) and int(options) in range(1, 7))):
                    match(options):
                        case 'sair' | 'levantar' | '6':
                            print("Decidiu sair, verificando se pode sair...")
                            money, result = bill_verify(0, table, name)
                            if (result):
                                servidor.rdt_send('Volte sempre ^^'.encode('utf-8'))
                                mesas.get(tableNumber).update(table)
                                break
                            else: 
                                servidor.rdt_send('Você ainda não pagou sua conta'.encode('utf-8'))
                        case 'cardapio' | '1':
                            print("Enviando cardápio...")
                            servidor.rdt_send(cardapio.encode('utf-8'))
                            clientMessage = servidor.rdt_rcv()['data']

                        case 'pedido' | 'pedir' | '2':
                            servidor.rdt_send('Digite qual o primeiro item que gostaria (número ou por extenso)'.encode('utf-8'))
                            clientMessage = servidor.rdt_rcv()['data']
                            item = clientMessage.decode('utf-8')

                            print("Aguardando pedido existente...")

                            while (item in cardapioPorExtenso or (isDigit(item) and int(item) in range(0, 10)) or (item not in negacoes)):
                                save_request(item, mesas.get(tableNumber), name)

                                servidor.rdt_send('Gostaria de mais algum item? (número ou por extenso)'.encode('utf-8'))
                                clientMessage = servidor.rdt_rcv()['data']
                                item = clientMessage.decode('utf-8')

                            servidor.rdt_send('Pedido finalizado'.encode('utf-8'))

                        case 'conta individual' | '3':
                            print("Enviando conta individual...")
                            servidor.rdt_send(individual_bill(table, name).encode('utf-8'))

                        case 'conta da mesa' | '4':
                            print("Enviando conta da mesa...")
                            servidor.rdt_send(table_bill(table).encode('utf-8'))
                        
                        case 'pagar' | '5':
                            total_individual = sum(cardapio[p] for p in table[name])
                            total_mesa = sum(cardapio[p] for pedidos in table.values() for p in pedidos)

                            bill = f"Sua conta foi R$ {total_individual:.2f} e a da mesa R$ {total_mesa:.2f}. Digite o valor que deseja pagar"
                            
                            servidor.rdt_send(bill.encode('utf-8'))
                            clientMessage = servidor.rdt_rcv()['data']
                            value = clientMessage.decode('utf-8')

                            money, result = bill_verify(value, table, name)

                            print("Verificando se o pagamento foi efetuado...")

                            if (result):
                                if (money > 0):
                                    responsePayment = f"Seu troco é R$ {money:.2f}\nDeseja confirmar o pagamento?\n"
                                else:
                                    responsePayment = "Deseja confirmar o pagamento?"

                                servidor.rdt_send(responsePayment.encode('utf-8'))
                                clientMessage = servidor.rdt_rcv()['data']
                                confirm = clientMessage.decode('utf-8')
                                if (confirm in negacoes):
                                    servidor.rdt_send('Pagamento cancelado'.encode('utf-8'))
                                else:
                                    servidor.rdt_send('Você pagou sua conta, obrigado!'.encode('utf-8'))
                            else:
                                servidor.rdt_send(f"Você ainda deve R$ {money:.2f}".encode('utf-8'))
# ----------------------------------------------------- #
#  Textos que serão enviados ao cliente ou verificações #
# ----------------------------------------------------- #

opcoes = "Digite uma das opções a seguir (o número ou por extenso):\n\
        1 - cardápio\n\
        2 - pedido\n\
        3 - conta individual\n\
        4 - conta da mesa\n\
        5 - pagar\n\
        6 - levantar\n"

respostasPorExtenso = ['cardapio', 'pedido', 'conta individual', 'conta da mesa', 'sair', 'pedir', 'levantar', 'pagar']

cardapio = "Cardápio do CINtofome:\n\n\
            0 - Churrasco Misto: R$ 45,00\n\
            1 - Parmegiana: R$ 20,00\n\
            2 - Filé Mignon: R$ 30,00\n\
            3 - Risoto de Camarão: R$ 25,00\n\
            4 - Salmão Grelhado: R$ 35,00\n\
            5 - Feijoada: R$ 18,00\n\
            6 - Lasanha: R$ 22,00\n\
            7 - Picanha: R$ 40,00\n\
            8 - Espaguete à Carbonara: R$ 28,00\n\
            9- Pizza Margherita: R$ 25,00\n\
            Digite 'pedir' para fazer o pedido ou qualquer outra coisa para voltar as opções\n"

cardapioPorExtenso = ['churrasco misto', 'parmegiana', 'filé mignon',\
                       'risoto de camarão', 'salmão grelhado', 'feijoada',\
                        'lasanha', 'picanha', 'espaguete à carbonara', 'pizza margherita']

negacoes = ['não', 'nao', 'n', 'no']

# ----------------------------------------------------- #
#  Textos que serão enviados ao cliente ou verificações #
# ----------------------------------------------------- #

if __name__ == '__main__':
    main()