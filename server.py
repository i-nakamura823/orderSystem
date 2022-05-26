import socket

server_ip = "192.168.0.1"
server_port = 334
listen_num = 5
buffer_size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server_ip, server_port))
s.listen(listen_num)
while True:
    client, address = s.accept()
    print(f"Connection from {address} is established")
    client.send(bytes("hello", 'utf-8'))
    client.close()
