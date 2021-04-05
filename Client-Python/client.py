#!/usr/bin/env python3

import socket

TCP_IP = 'iao.life'
TCP_PORT = 11030
BUFFER_SIZE = 1024
f = open('/mnt/d/iao13/Pictures/Cache_-19fd3b1376964f02..jpg', 'rb')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while 1:
    MESSAGE = f.read(BUFFER_SIZE)
    if not MESSAGE:
        break
    s.send(MESSAGE)
s.close()
f.close()
