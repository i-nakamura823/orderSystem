import socket
import threading
import pickle
import re
from ..comutil import ComUnit

class Client():
    def __init__(self, ip, tree):
        self.CLIENTIP = ip
        self.SERVERIP = '192.168.0.3'
        self.PORT = 334
        self.BUFFER_SIZE = 1024
        self.orderId = 0
        self.tree = tree
        self.iid = 5

    def prepareSocket(self):
        sock = socket.socket(socket.AF_INET)
        sock.connect((self.SERVERIP, self.PORT))
        self.sock = sock

    # データ受信関数
    def recvData(self):
        while True:
            try:
                data = self.sock.recv(self.BUFFER_SIZE)
                if data == b"":
                    break
                content = pickle.loads(data)
                print(f'new order({content.key}):', 'menu:', content.menuId, 'num:', content.num)
                if content.mode == 3 :
                    catch_order(tree, iid, content.sender, name, num, cost)
                    iid += 1
                elif content.mode == 1 :
                    clear_order
            except ConnectionResetError:
                break

        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        
    def run(self):
        # �f�[�^��M���T�u�X���b�h�Ŏ��s
        thread = threading.Thread(target=self.recvData)
        thread.start()

    def send(self, unit):
        # �f�[�^�����[�v
        try:
            unit.key = self.orderId
            self.sock.send(pickle.dumps(unit))
            self.orderId += 1
        except ConnectionResetError:
            pass

    def disconnect(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()