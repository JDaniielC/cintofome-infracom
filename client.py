from socket import *
import os

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 5500
BUFFER_SIZE = 1024
PORT = 5501

def main():
    sending_file = True
    file_type = "txt"
    while sending_file:
        file_name = input("Escreva o nome e tipo do arquivo que deseja enviar (test_file.txt):")
        # Primeiro vou enviar o tipo de arquivo que será enviado
        file_type = os.path.splitext(file_name)[1]

        if os.path.exists(file_name): # Verificar se o arquivo existe
            with open(file_name, "rb") as file:
                # Após leitura do arquivo vamos criar o socket UDP
                udp_client = socket(AF_INET, SOCK_DGRAM)
                udp_client.sendto(file_type.encode(), (SERVER_ADDRESS, SERVER_PORT))
                udp_client.close()

                # Agora vou enviar o arquivo
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
            
            # ------------- Agora vamos receber o arquivo do servidor -------------
            udp_client = socket(AF_INET, SOCK_DGRAM)
            udp_client.bind((SERVER_ADDRESS, PORT))
            # Endereço ou porta deve ser diferente do servidor

            print("Pronto para receber o arquivo, cada ponto é um chunk recebido:")
            data = bytearray()
            try:
                while True:
                    # Se passou 6 segundos sem receber, é pq o servidor provavelmente não recebeu seu arquivo
                    udp_client.settimeout(6)
                    print(".")
                    chunk, server_address = udp_client.recvfrom(BUFFER_SIZE)

                    # Se não houver mais dados para receber, sair do loop
                    if not chunk:
                        sending_file = False
                        break
                    data += chunk # Adicionando o chunk ao arquivo
            except timeout: # Se acabar por tempo é porque não recebeu todo arquivo.
                print("Tempo esgotado, reenviando arquivo.")
        else:
            print("Crie o arquivo e põe no diretório do cliente!")

    print("Arquivo recebido e armazenado.")
    with open(f"received_file.{file_type}", "wb") as file:
        file.write(data) # Escrevendo o arquivo

    print("Acabou, fechando conexão.")
    udp_client.close()

if __name__ == '__main__':
    main()
