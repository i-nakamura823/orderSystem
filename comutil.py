import pickle
import socket

class ComUtil:
    SERVERIP = '192.168.0.3'
    PORT = 334
    BUFFER_SIZE = 1024

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ComUtil.SERVERIP, ComUtil.PORT))

    def send(self, unit):
        self.sock.send(pickle.dumps(s))

class ComUnit:
    def __init__(self, mode = None, sender = None, reciever = None, menuId = None, num = None, key = None):
        self.mode = mode
        self.sender = sender
        self.reciever = reciever
        self.menuId = menuId
        self.num = num
        self.key = key