import pickle
import socket

#class ComUtil:
#    SERVERIP = '192.168.0.3'
#    PORT = 334
#    BUFFER_SIZE = 1024

#    def __init__(self):
#        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        self.sock.connect((ComUtil.SERVERIP, ComUtil.PORT))

#    def send(self, unit):
#        self.sock.send(pickle.dumps(s))

class ComUnit:
    def __init__(self, mode = None, reciever = None, menuId = None, num = None):
        self.mode = mode          # 注文モード
        self.sender = None        # 送信元(送信時に自動補完)
        self.reciever = reciever  # 宛先
        self.menuId = menuId      # メニュー番号
        self.num = num            # 数量
        self.key = None           # 各クライアントの注文番号(送信時に自動補完)
        self.orderId = None       # 注文ID(サーバで割り当て)