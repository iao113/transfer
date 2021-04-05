#!/usr/bin/env python3

import socket

TCP_IP = 'iao.life'
TCP_PORT = 11030
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(bytes(MESSAGE, 'utf-8'))
data = s.recv(BUFFER_SIZE)
s.close()

print("received data:", str(data, 'utf-8'))
