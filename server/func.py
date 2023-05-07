cardapioDict = {"churrasco misto": 45.00, "parmegiana": 20.00, "filé mignon": 30,\
             "risoto de camarão": 25, "salmão grelhado": 35, "feijoada": 18, \
                "lasanha": 22, "picanha": 40, "espaguete à carbonara": 28, "pizza margherita": 25}

mesas = {"1": {"Vítor Azevedo": ["parmegiana", 'feijoada'], "Felipe Maltez": ["lasanha", 'picanha']}}
pagamentos = {}

def individual_bill(pedidos):
    total = 0
    linha = "Conta individual:\n"
    linha += "{:<20}{:>10}\n".format("Item", "Preço")
    linha += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n"
    for pedido in pedidos:
        preco = cardapioDict.get(pedido)
        if preco is not None:
            linha += "{:<20}{:>10.2f}\n".format(pedido, preco)
            total += preco

    linha += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n"
    linha += "Total - R$ {:,.2f}\n".format(total)
    linha += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n"
    return linha

def table_bill(pedidos):
    total_mesa = 0.0 # variável para armazenar o total da mesa
    
    saida = "Conta da mesa:\n\n"
    for nome_cliente, lista_pedidos in pedidos.items():
        saida += f"{nome_cliente}:\n"
        saida += "{:<20}{:>10}\n".format("Item", "Preço")
        saida += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n"
        for pedido in lista_pedidos:
            preco = cardapioDict.get(pedido)
            if preco is not None:
                saida += "{:<20}{:>10.2f}\n".format(pedido, preco)
                total_mesa += preco
        
        saida += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n"
    
    # total da mesa
    saida += "Total da mesa - R$ {:,.2f}\n".format(total_mesa)
    saida += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n"
    
    return saida



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
                         
# ----------------------------------------------------- #
#  Textos que serão enviados ao cliente ou verificações #
# ----------------------------------------------------- #

continueText = "\nAperte enter para continuar"

opcoes = "Digite uma das opções a seguir (o número ou por extenso):\n\
        1 - cardápio\n\
        2 - pedido\n\
        3 - conta individual\n\
        4 - conta da mesa\n\
        5 - pagar\n\
        6 - levantar\n"

respostasPorExtenso = ['cardapio', 'pedido', 'conta individual', 'conta da mesa', 'sair', 'pedir', 'levantar', 'pagar']

cardapio = "Cardápio do CINtofome:\n\n\
            0 - churrasco misto: R$ 45,00\n\
            1 - parmegiana: R$ 20,00\n\
            2 - filé mignon: R$ 30,00\n\
            3 - risoto de camarão: R$ 25,00\n\
            4 - salmão grelhado: R$ 35,00\n\
            5 - feijoada: R$ 18,00\n\
            6 - lasanha: R$ 22,00\n\
            7 - picanha: R$ 40,00\n\
            8 - espaguete à carbonara: R$ 28,00\n\
            9- pizza margherita: R$ 25,00\n"

cardapioPorExtenso = ['churrasco misto', 'parmegiana', 'filé mignon',\
                       'risoto de camarão', 'salmão grelhado', 'feijoada',\
                        'lasanha', 'picanha', 'espaguete à carbonara', 'pizza margherita']

negacoes = ['não', 'nao', 'n', 'no']

# ----------------------------------------------------- #
#  Textos que serão enviados ao cliente ou verificações #
# ----------------------------------------------------- #