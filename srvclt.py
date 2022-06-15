import socket
import threading
from comutil import ComUnit

class Server():
    def __init__(self):
        self.SERVERIP = '127.0.0.1'
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

                client.send(data)
                #content = pickle.load(data)
                #reciever = self.clients[content.reciever]
                #reciever.send(data)

            except ConnectionResetError:
                break

        # クライアントリストから削除
        self.clients.pop(addr)
        print("- close client:{}".format(addr))

        client.shutdown(socket.SHUT_RDWR)
        client.close()

    def run(self):
        while True:
            new_clt, addr = self.sock.accept()
            # クライアントをリストに追加
            self.clients[addr] = new_clt
            print("+ join client:{}".format(addr))

            thread = threading.Thread(target=self.recvClient, args=(addr,))
            thread.start()

class Client():
    def __init__(self):
        self.IPADDR = "127.0.0.1"
        self.PORT = 334
        self.BUFFER_SIZE = 1024

    def prepareSocket(self):
        sock = socket.socket(socket.AF_INET)
        sock.connect((self.IPADDR, self.PORT))
        self.sock = sock

    # データ受信関数
    def recvData(self):
        while True:
            try:
                data = self.sock.recv(self.BUFFER_SIZE)
                if data == b"":
                    break
                print(data.decode("utf-8"))
            except ConnectionResetError:
                break

        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def run(self):
        # データ受信をサブスレッドで実行
        thread = threading.Thread(target=self.recvData)
        thread.start()

        # データ入力ループ
        while True:
            data = input("> ")
            if data == "exit":
                break
            else:
                try:
                    self.sock.send(data.encode("utf-8"))
                except ConnectionResetError:
                    break

        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()