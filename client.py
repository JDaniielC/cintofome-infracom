from socket import *
import os

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 5500
BUFFER_SIZE = 1024
PORT = 5501

sending_file = True

def main():
    while sending_file:
        # O arquivo que será enviado é o test_file.txt
        if os.path.exists("test_file.txt"):
            with open("test_file.txt", "rb") as file:
                data = file.read()

                # Após leitura do arquivo vamos criar o socket UDP
                udp_client = socket(AF_INET, SOCK_DGRAM)

                # O envio do arquivo será feito em chunks de 1024 bytes
                for i in range(0, len(data), BUFFER_SIZE):
                    # Enviando parte a parte até finalizar o arquivo
                    chunk = data[i:i+BUFFER_SIZE]
                    udp_client.sendto(chunk, (SERVER_ADDRESS, SERVER_PORT))

                print("Arquivo enviado.")
                udp_client.close() # Fechando o socket
        else:
            print("Crie o arquivo e põe no diretório do cliente!")

        # ------------- Agora vamos receber o arquivo do servidor -------------

        udp_client = socket(AF_INET, SOCK_DGRAM)
        udp_client.bind((SERVER_ADDRESS, PORT))
        # Endereço ou porta deve ser diferente do servidor

        print("Pronto para receber o arquivo, cada ponto é um chunk recebido:")
        data = bytearray()
        try:
            while True:
                udp_client.settimeout(2)
                print(".")
                chunk, server_address = udp_client.recvfrom(BUFFER_SIZE)

                # Se não houver mais dados para receber, sair do loop
                if not chunk:
                    sending_file = False
                    break
                data += chunk # Adicionando o chunk ao arquivo
        except timeout: # Se acabar por tempo é porque não recebeu todo arquivo.
            print("Tempo esgotado, reenviando arquivo.")
    print("Arquivo recebido e armazenado.")
    with open("received_file.txt", "wb") as file:
        file.write(data) # Escrevendo o arquivo

    print("Acabou, fechando conexão.")
    udp_client.close()

if __name__ == '__main__':
    main()
