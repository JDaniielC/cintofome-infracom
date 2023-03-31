from socket import *

HOST = '127.0.0.1'
PORT = 5500

def main():
    # Criando o socket UDP
    udp_server = socket(AF_INET, SOCK_DGRAM)
    udp_server.bind((HOST, PORT))

    print("O servidor está esperando receber o tipo de arquivo que será enviado.")
    # Recebendo o tipo de arquivo que será enviado
    received_data, client_address = udp_server.recvfrom(1024)
    received_file_type = received_data.decode()

    # Criando o arquivo que será recebido
    received_file = open(f"received_server.{received_file_type}", "wb")

    print("Esperando receber arquivo:")
    data, client_address = udp_server.recvfrom(1024)

    try: # Se não receber nada, sair do loop
        while data:
            udp_server.settimeout(2)
            # Se passar 2 segundos sem receber nada, sair do loop

            received_file.write(data)
            print("Recebendo parte do arquivo...")
            data, client_address = udp_server.recvfrom(1024)
    except timeout:
        received_file.close()
        print("Arquivo foi recebido e armazenado.")

    # ----------------- Agora vamos enviar o arquivo de volta -----------------

    file_to_send = open(f"received_server.{received_file_type}", "rb")

    # Lembrando que deve ser enviado em chunks de 1024 bytes
    data = file_to_send.read(1024)
    while data:
        udp_server.sendto(data, (HOST, 5501))
        print("Parte enviada para o cliente.")
        data = file_to_send.read(1024)
    # Como o cliente está esperando um arquivo vazio para sair do loop:
    udp_server.sendto(b'', (HOST, 5501))

    file_to_send.close()
    udp_server.close() # Fechando o socket

if __name__ == '__main__':
    while True:
        main()