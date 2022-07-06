import socket
import threading
import pickle
from comutil import ComUnit

class Server():
    def __init__(self):
        self.SERVERIP = '192.168.0.3'
        #SERVERIP = '192.168.0.3'
        self.PORT = 334
        self.BUFFER_SIZE = 1024
        self.clients = dict()
        self.orderCount = 0

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
                # IDが未割当の注文にIDを付与して data を更新・返送
                if content.orderId is None:
                    content.orderId = self.orderCount
                    data = pickle.dumps(content)
                    client.send(data)
                    self.orderCount += 1
                # 送信先が存在することを確認して data を送信
                if content.reciever in self.clients:
                    reciever = self.clients[content.reciever]
                    reciever.send(data)

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
        self.key = 0
        self.msglog = dict()

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
                if content.sender != self.CLIENTIP:
                    print(f'new order({content.key}):', 'menu:', content.menuId, 'num:', content.num)
                # サーバから注文IDつきの ComUnit が返送されたとき msglog に入っているログを更新
                if content.key in self.msglog:
                    self.msglog[content.key] = content
                    print(f'My order #{content.key} is allocated ID({content.orderId})')
            except ConnectionResetError:
                break
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except OSError:
            pass
        
    def run(self):
        # データ受信をサブスレッドで実行
        thread = threading.Thread(target=self.recvData)
        thread.start()

    def send(self, unit, sender = None):
        # 引数の ComUnit を pickle 化してサーバに送信
        # client 情報を Unit に付与 
        if sender is None:
            unit.sender = self.CLIENTIP
        else:
            unit.sender = sender
        unit.key = self.key
        try:
            self.sock.send(pickle.dumps(unit))
            self.msglog[self.key] = unit
            self.key += 1
        except ConnectionResetError:
            pass

    def disconnect(self):
        # サーバとの接続を切断
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

#     def run(self):
#         # データ受信をサブスレッドで実行
#         thread = threading.Thread(target=self.recvData)
#         thread.start()

#         # データ入力ループ
#         while True:
#             print('input order: menuId, num, reciever IP Address')
#             data = input("> ")
#             if data == "exit":
#                 break
#             else:
#                 try:
#                     menuId, num, reciever = re.split('[,\s]+',data)
#                     unit = ComUnit(0 ,self.CLIENTIP, reciever, menuId, num, self.orderId)
#                     self.sock.send(pickle.dumps(unit))
#                     self.orderId += 1
#                 except ConnectionResetError:
#                     break

#         self.sock.shutdown(socket.SHUT_RDWR)
#         self.sock.close()
