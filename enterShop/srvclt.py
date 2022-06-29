import socket
import threading
import pickle
import re

class Server():
    def __init__(self):
        self.SERVERIP = '192.168.0.3'
        #SERVERIP = '192.168.0.3'
        self.PORT = 334
        self.BUFFER_SIZE = 1024
        self.clients = dict()

    def prepareSocket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.SERVERIP, self.PORT))
        s.listen()
        self.sock = s

    def recvClient(self, addr):
        client = self.clients[addr]
        while True:
            try:
                data = client.recv(self.BUFFER_SIZE)
                if data == b"":
                    break

                print("$ say client:{}".format(addr))

                content = pickle.loads(data)
                #print('client IP Address:', content.reciever)
                if content.reciever in self.clients:
                    reciever = self.clients[content.reciever]
                    reciever.send(data)

            except ConnectionResetError:
                break

        # �N���C�A���g���X�g����폜
        self.clients.pop(addr)
        print("- close client:{}".format(addr))

        client.shutdown(socket.SHUT_RDWR)
        client.close()

    def run(self):
        while True:
            new_clt, addr = self.sock.accept()
            # �N���C�A���g�����X�g�ɒǉ�
            addr = addr[0]
            self.clients[addr] = new_clt
            print("+ join client:{}".format(addr))

            thread = threading.Thread(target=self.recvClient, args=(addr,))
            thread.start()

class Client():
    def __init__(self, ip):
        self.CLIENTIP = ip
        self.SERVERIP = '192.168.0.3'
        self.PORT = 334
        self.BUFFER_SIZE = 1024
        self.orderId = 0

    def prepareSocket(self):
        sock = socket.socket(socket.AF_INET)
        sock.connect((self.SERVERIP, self.PORT))
        self.sock = sock

    # �f�[�^��M�֐�
    def recvData(self):
        while True:
            try:
                data = self.sock.recv(self.BUFFER_SIZE)
                if data == b"":
                    break
                content = pickle.loads(data)
                print(f'new order({content.key}):', 'menu:', content.menuId, 'num:', content.num)
            except ConnectionResetError:
                break
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except OSError:
            pass

    def run(self):
        # �f�[�^��M���T�u�X���b�h�Ŏ��s
        thread = threading.Thread(target=self.recvData)
        thread.start()

    def send(self, unit):
        # �f�[�^���̓��[�v
        try:
            unit.key = self.orderId
            self.sock.send(pickle.dumps(unit))
            self.orderId += 1
        except ConnectionResetError:
            pass
    
    def disconnect(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
