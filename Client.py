#! /usr/bin/env python

import socket
import sys
import time
import threading
import select
import traceback
import time
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

state = True
chaves = []
mensagens = []
message = dict

key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()
aes_key = get_random_bytes(32)        
cipher_aes = AES.new(aes_key, AES.MODE_GCM)

cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))


class Server(threading.Thread):
    def initialise(self, receive):
        self.receive = receive

    def run(self):
        global chaves
        global message
        lis = []
        lis.append(self.receive)
        while 1:
            read, write, err = select.select(lis, [], [])
            for item in read:
                try:           
                    if len(chaves) == 0:
                        s = item.recv(1024)
                        chaves.append(s.decode())
                        chunk = ""
                    else:   
                        s = item.recv(1024)                        
                        x = s.decode('UTF-8')       
                        if x.find('-----') == 0:
                            s = ''
                        if s != '':
                            #aki esta errrado, a msg tem q ser descriptografada com a chave publica no array chaves[0]
                            decrypted_message_rsa = cipher_aes.decrypt_and_verify(*message.keys(), *message.values())
                            decrypted_message = cipher_rsa.decrypt(decrypted_message_rsa)
                            print(decrypted_message.decode() + '\n>>')
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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        try:
            host = '127.0.0.1'
            port = 5535
        except EOFError:
            print("Error")
            return 1
        print("Connecting\n")
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

        global captura_msg, captura_tag

        # def EnviaChaves():
        #     time.sleep(10)
        #     global chaves
        #     if len(chaves) == 0 or len(chaves) == 1:
        #         msg = str(public_key)
        #         data = msg.encode()
        #         print("chave 1 enviada")
        #         self.client(host, port, data)

        def EnviaChaves():
            global chaves
            time.sleep(10)            
            if len(chaves) == 0 or len(chaves) == 1:
                msg = str(public_key)
                encrypted_message = cipher_rsa.encrypt(msg.encode('utf-8'))
                captura_msg, captura_tag = cipher_aes.encrypt_and_digest(encrypted_message)
                data = {captura_msg: captura_tag}
                print("chave 1 enviada")
                self.client(host, port, data)
               

        EnviaChaves()        
        print("Conectando..")
        time.sleep(5)
        while 1:
            print("Conectado")
            global message
            msg = input('>>')
            if msg == 'exit':
                break
            if msg == '':
                continue
            # print "Sending\n"
            msg = user_name + ': ' + msg
            encrypted_message = cipher_rsa.encrypt(msg.encode('utf-8'))
            captura_msg, captura_tag = cipher_aes.encrypt_and_digest(encrypted_message)
            message = {captura_msg: captura_tag}
            self.client(host, port, message)
            message.clear()
        return (1)


if __name__ == '__main__':
    print("Starting client")
    cli = Client()
    cli.start()