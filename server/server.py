from rdt import *

cardapioDict = {"churrasco misto": 45.00, "parmegiana": 20.00, "filé Mignon": 30,\
             "risoto de camarão": 25, "salmão grelhado": 35, "feijoada": 18, \
                "lasanha": 22, "picanha": 40, "espaguete à carbonara": 28, "pizza margherita": 25}

mesas = {"1": {"Vítor Azevedo": ["parmegiana", 'feijoada'], "Felipe Maltez": ["lasanha", 'picanha']}}

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
            preco = cardapioDict.get(item)
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
    pedidos = mesa.get(nome)
    if not pedidos:
        return "Não foram encontrados pedidos para este cliente."
    
    linha = f"| {nome} |\n"
    for pedido in pedidos:
        print(pedido)
        preco = cardapioDict.get(pedido)
        print(preco)
        if (preco is not None):
            linha += "{} => R$ {}\n".format(pedido, preco)
            total += preco
    
    linha += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-"
    linha += f"\nTotal - R$ {total}\n"
    linha += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-"
    
    return linha

def bill_verify(valor, mesa, nome): 
    total = 0
    pedidos = mesa.get(nome)
    if pedidos is not None:
        for pedido in pedidos:
            preco = cardapioDict.get(pedido)
            if (preco is not None):
                total += preco
    if (valor >= total):
        return valor - total, True
    else:
        return total - valor, False

def save_request(mesa: dict, nome: str, pedido: str):
    if (pedido.isdigit()):
        if (int(pedido) in range(0, 10)):
            pedido = cardapioPorExtenso[int(pedido)]
    pedidos = mesa.get(nome)
    pedidos.append(pedido)
    print(f"Pedido {pedido} adicionado para {nome} na mesa.")

def sum_bill(nome, mesa):
    total_individual = 0.0
    total_mesa = 0.0
    for name, requests in mesa.items():
        total_cliente = 0.0
        for item in requests:
            preco = cardapioDict.get(item)
            if preco is not None:
                total_cliente += preco

        total_mesa += total_cliente
    
    pedidos = mesa.get(nome)
    for pedido in pedidos:
        preco = cardapioDict.get(pedido)
        if preco is not None:
            total_individual += preco
    
    return f"Sua conta foi R$ {total_individual:.2f} e a da mesa R$ {total_mesa:.2f}. Digite o valor que deseja pagar"
                         
def main():
    # Conexão foi abstraída para a classe Rdt
    servidor = Rdt('server')
    # No qual fornece uma conexão UDT com os príncipios de RDT3.0

    print('Conexão estabelecida com o cliente')
    servidor.reset_num_seq()
    while True:
        # Recebe uma mensagem do cliente
        clientMessage = servidor.rdt_rcv()['data']

        if (clientMessage.decode('utf-8') == 'chefia'):
            tableNumber = 'Recebe número.'
            print("Aguardando número do usuário.")
            # Verificar se a mensagem foi um número:
            while (not tableNumber.isdigit()):
                servidor.rdt_send('Digite sua mesa'.encode('utf-8'))
                clientMessage = servidor.rdt_rcv()['data']
                tableNumber = clientMessage.decode('utf-8')
            
            servidor.rdt_send("Digite seu nome".encode('utf-8'))
            clientMessage = servidor.rdt_rcv()['data']
            name = clientMessage.decode('utf-8')

            if (mesas.get(tableNumber) == None):
                mesas[tableNumber] = {name: []}
                print("Mesa criada, usuário adicionado à mesa.")
            elif (mesas.get(tableNumber).get(name) == None):
                mesas[tableNumber][name] = []
                print("Usuário adicionado à mesa.")

            print("Cadastro finalizado")
            while (True):
                servidor.rdt_send(opcoes.encode('utf-8'))
                clientMessage = servidor.rdt_rcv()['data']
                if (clientMessage == 'ACK'):
                    print("Erro ao enviar opções.")
                    continue
                options = clientMessage.decode('utf-8')

                table = mesas.get(tableNumber)

                if (options in respostasPorExtenso or (options.isdigit() and int(options) in range(1, 7))):
                    match(options):
                        case 'sair' | 'levantar' | '6':
                            print("Decidiu sair, verificando se pode sair...")
                            money, result = bill_verify(0, table, name)
                            if (result):
                                servidor.rdt_send('Volte sempre ^^'.encode('utf-8'))
                                mesas[tableNumber].update(table)
                                clientMessage = servidor.rdt_rcv()['data']
                                break
                            else: 
                                servidor.rdt_send('Você ainda não pagou sua conta.\nAperte enter para continuar'.encode('utf-8'))
                                clientMessage = servidor.rdt_rcv()['data']
                        case 'cardapio' | '1':
                            print("Enviando cardápio...")
                            servidor.rdt_send(cardapio.encode('utf-8'))
                            clientMessage = servidor.rdt_rcv()['data']

                        case 'pedido' | 'pedir' | '2':
                            servidor.rdt_send('Digite qual o primeiro item que gostaria (número ou por extenso)\
                                              {}'.format(cardapio).encode('utf-8'))
                            clientMessage = servidor.rdt_rcv()['data']
                            item = clientMessage.decode('utf-8')

                            print("Aguardando pedido existente...")

                            while (item in cardapioPorExtenso or (item.isdigit() and int(item) in range(0, 10))):
                                save_request(table, name, item)

                                servidor.rdt_send('Gostaria de mais algum item? (número ou por extenso)'.encode('utf-8'))
                                clientMessage = servidor.rdt_rcv()['data']
                                item = clientMessage.decode('utf-8')
                            
                            servidor.rdt_send('Aperte enter para continuar'.encode('utf-8'))
                            clientMessage = servidor.rdt_rcv()['data']

                        case 'conta individual' | '3':
                            print("Enviando conta individual...")
                            servidor.rdt_send('{}\nAperte enter para continuar.'.format(individual_bill(table, name)).encode('utf-8'))
                            servidor.rdt_rcv()['data']

                        case 'conta da mesa' | '4':
                            print("Enviando conta da mesa...")
                            servidor.rdt_send('{}\nAperte enter para continuar.'.format(table_bill(table)).encode('utf-8'))
                            servidor.rdt_rcv()['data']
                        
                        case 'pagar' | '5':
                            bill = sum_bill(name, table)
                            servidor.rdt_send(bill.encode('utf-8'))
                            clientMessage = servidor.rdt_rcv()['data']
                            value = clientMessage.decode('utf-8')

                            result = False

                            if (value.isdigit()):
                                money, result = bill_verify(int(value), table, name)
                            else:
                                print("Valor inválido.")
                                money, result = bill_verify(0, table, name)

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
                                    servidor.rdt_send('Pagamento cancelado.\nAperte enter para continuar.'.encode('utf-8'))
                                    servidor.rdt_rcv()
                                else:
                                    servidor.rdt_send('Você pagou sua conta, obrigado!\nAperte enter para continuar'.encode('utf-8'))
                                    servidor.rdt_rcv()
                            else:
                                servidor.rdt_send(f"Você ainda deve R$ {money:.2f}.\nAperte enter para continuar".encode('utf-8'))
                                servidor.rdt_rcv()
        else:
            servidor.rdt_send('Seja bem vindo ao CINtofome!\nDigite "chefia" para iniciar o sistema'.encode('utf-8'))
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
            9- Pizza Margherita: R$ 25,00\n"

cardapioPorExtenso = ['churrasco misto', 'parmegiana', 'filé mignon',\
                       'risoto de camarão', 'salmão grelhado', 'feijoada',\
                        'lasanha', 'picanha', 'espaguete à carbonara', 'pizza margherita']

negacoes = ['não', 'nao', 'n', 'no']

# ----------------------------------------------------- #
#  Textos que serão enviados ao cliente ou verificações #
# ----------------------------------------------------- #

if __name__ == '__main__':
    main()