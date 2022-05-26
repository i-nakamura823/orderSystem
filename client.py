import socket
target_ip = "192.168.0.1"
target_port = 334
buffer_size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((target_ip, target_port))
messsage = s.recv(1024)
print(messsage.decode("utf-8"))