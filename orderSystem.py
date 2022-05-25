import socket

import socket [server.py]
server_ip = "192.168.0.1"
server_port = 334
listen_num = 5
buffer_size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server_ip, server_port))
s.listen(listen_num)

While True:
