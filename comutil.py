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
        self.mode = mode          # �������[�h
        self.sender = None        # ���M��(���M���Ɏ����⊮)
        self.reciever = reciever  # ����
        self.menuId = menuId      # ���j���[�ԍ�
        self.num = num            # ����
        self.key = None           # �e�N���C�A���g�̒����ԍ�(���M���Ɏ����⊮)
        self.orderId = None       # ����ID(�T�[�o�Ŋ��蓖��)