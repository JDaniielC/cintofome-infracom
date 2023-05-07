from rdt import *
from func import *

def main():
    # Conexão foi abstraída para a classe Rdt
    servidor = Rdt('server')
    # No qual fornece uma conexão UDT com os príncipios de RDT3.0

    print('Conexão estabelecida com o cliente')
    servidor.reset_num_seq()
    while True:
        print("Aguardando mensagem do novo cliente.")
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
                            if name in pagamentos:  # Verifique se o cliente já pagou a conta
                                servidor.rdt_send('Volte sempre ^^'.encode('utf-8'))
                                table.pop(name)
                                break
                            else: 
                                servidor.rdt_send('Você ainda não pagou sua conta.{}'.format(continueText).encode('utf-8'))
                                clientMessage = servidor.rdt_rcv()['data']
                        case 'cardapio' | '1':
                            print("Enviando cardápio...")
                            servidor.rdt_send("{}{}".format(cardapio, continueText).encode('utf-8'))
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
                            servidor.rdt_send('{}{}.'.format(individual_bill(table[name]), continueText).encode('utf-8'))
                            servidor.rdt_rcv()['data']


                        case 'conta da mesa' | '4':
                            print("Enviando conta da mesa...")
                            servidor.rdt_send('{}{}.'.format(table_bill(table), continueText).encode('utf-8'))
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
                                pagamentos[name] = True  # Adicione o nome do cliente à lista de pagamentos
                                if (money > 0):
                                    responsePayment = f"Seu troco é R$ {money:.2f}\nDeseja confirmar o pagamento?\n"
                                else:
                                    responsePayment = "Deseja confirmar o pagamento?"

                                servidor.rdt_send(responsePayment.encode('utf-8'))
                                clientMessage = servidor.rdt_rcv()['data']
                                confirm = clientMessage.decode('utf-8')
                                if (confirm in negacoes):
                                    servidor.rdt_send('Pagamento cancelado.{}.'.format(continueText).encode('utf-8'))
                                    servidor.rdt_rcv()
                                else:
                                    servidor.rdt_send('Você pagou sua conta, obrigado!{}'.format(continueText).encode('utf-8'))
                                    table[name] = []
                                    servidor.rdt_rcv()
                            else:
                                servidor.rdt_send(f" Não foi possível finalizar pagamento, pois ficou faltando : R$ {money:.2f}, refaça o pagamento, por gentileza.{continueText}".encode('utf-8'))
                                servidor.rdt_rcv()

        else:
            servidor.rdt_send('Seja bem vindo ao CINtofome!\nDigite "chefia" para iniciar o sistema'.encode('utf-8'))


if __name__ == '__main__':
    main()
