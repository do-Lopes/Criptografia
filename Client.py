#! /usr/bin/env python

import socket
import sys
import time
import threading
import select
import traceback
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet

state = True
chaves = []


private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
    )

class Server(threading.Thread):
    def initialise(self, receive):
        self.receive = receive

    def run(self):
        lis = []
        lis.append(self.receive)
        while 1:
            read, write, err = select.select(lis, [], [])
            for item in read:
                try:
                    s = item.recv(1024)
                    if s != '':
                        chunk = s
                        print(chunk.decode() + '\n>>')
                except:
                    traceback.print_exc(file=sys.stdout)
                    break


class Client(threading.Thread):
    def connect(self, host, port):
        self.sock.connect((host, port))

    def client(self, host, port, msg):
        sent = self.sock.send(msg)
        # print "Sent\n"

    def run(self):
        # global state
        # print(state)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        try:
            host = '127.0.0.1'
            port = 5535
        except EOFError:
            print("Error")
            return 1
        print("Connecting\n")
        # if state:
        #     state = False
        s = ''
        self.connect(host, port)
        print("Connected\n")      
        user_name = input("Enter the User Name to be Used\n>>")
        receive = self.sock
        time.sleep(1)
        srv = Server()
        srv.initialise(receive)
        srv.daemon = True
        print("Starting service")
        srv.start()
        
        #aki a chave publica e privada é criada
        #------------------------------------------
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        public_key = private_key.public_key()
        #------------------------------------------

        chaves.append(private_key)
        chaves.append(public_key)

        print(chaves)

#         key = Fernet.generate_key()

# # Crie um objeto Fernet com a chave gerada
#         fernet = Fernet(key)

# # Dados a serem criptografados
#         data = chaves

# # Criptografe os dados
#         encrypted_data = fernet.encrypt(data)

# # Salve os dados criptografados em um arquivo
#         with open('dados_criptografados.txt', 'wb') as file:
#             file.write(encrypted_data)
            


        #chaves.append(private_key)preciso fazer esses dados persistirem para o segundo cliente
        #nesse ponto as chaves publicas de ambos os clientes ja devem estar entregues
        
        
        #em seguida é necessário fazer a chave simétrica

        # apos as chaves simétricas serem feitas, é necessário criptografar a C.S. com a chave 
        # publica do destino, descriptografar ela e fazer seu hash. Ao mesmo tempo, é feito
        # o hash da chave simétrica e criptografada pela chave privada do remetente, descriptografa ela e faz o hash, compara os dois hash pra confirmar a confidencialidade

        while 1:
            # print "Waiting for message\n"
            msg = input('>>')
            if msg == 'exit':
                break
            if msg == '':
                continue
            # print "Sending\n"
            msg = user_name + ': ' + msg
            data = msg.encode()#aki a mensagem precisa ser codificada utilizando a chave simétrica
            self.client(host, port, data)
        return (1)


if __name__ == '__main__':
    print("Starting client")
    cli = Client()
    cli.start()