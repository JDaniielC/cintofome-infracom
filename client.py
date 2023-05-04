from server.rdt import *
from datetime import datetime

def get_time():
    return datetime.now().strftime('%H:%M')

def main():
    # Conexão foi abstraída para a classe Rdt
    client = Rdt('client')

    print("Conexão estabelecida com o servidor")
    serverMessage = b'' # Mensagem recebida do servidor
    while (serverMessage.decode('utf-8') != "Volte sempre ^^"):
        # Envia uma mensagem para o servidor
        clientMessage = input('{} Client: '.format(get_time()))
        client.rdt_send(clientMessage.encode('utf-8'))

        # Recebe uma mensagem do servidor
        serverMessage = client.rdt_rcv()['data']
        print('{} CINtofome: '.format(get_time()), serverMessage.decode('utf-8'))
    
    # Fecha a conexão
    print("Conexão encerrada")   

if __name__ == '__main__':
    while True:
        main()