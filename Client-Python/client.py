#!/usr/bin/env python3

import os
import socket

from collections import namedtuple
from enum import Enum, unique

HeadTerm = namedtuple('HeadTerm', ['index', 'value'])

@unique
class Header(Enum):
    FILE_NAME = HeadTerm(index=0, value=0x80)
    FILE_SIZE = HeadTerm(index=0, value=0x40)
    FILE_CONTEXT = HeadTerm(index=0, value=0x20)

def headEncoder(header: Header) -> bytes:
    HEAD_SIZE = 8
    messageHead = bytearray(HEAD_SIZE)
    messageHead[header.value.index] = header.value.value
    return bytes(messageHead)

def main():
    TCP_IP = 'iao.life'
    TCP_PORT = 11030
    BUFFER_SIZE = 1024
    HEAD_SIZE = 8
    FILE_DIR = '/mnt/d/iao13/Pictures/Cache2.jpg'
    f = open(FILE_DIR, 'rb')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    filename = bytes(FILE_DIR.split('/')[-1], 'utf-8')
    for i in range(0, len(filename), BUFFER_SIZE - HEAD_SIZE):
        message = filename[i:i + BUFFER_SIZE - HEAD_SIZE]
        if not message:
            break
        message = headEncoder(Header.FILE_NAME) + message
        if len(message) < BUFFER_SIZE:
            message = message + bytes(BUFFER_SIZE - len(message))
        s.send(message)
    filesize = os.path.getsize(FILE_DIR)
    message = headEncoder(Header.FILE_SIZE) + filesize.to_bytes(BUFFER_SIZE - HEAD_SIZE, byteorder='big')
    s.send(message)
    while 1:
        message = f.read(BUFFER_SIZE - HEAD_SIZE)
        if not message:
            break
        message = headEncoder(Header.FILE_CONTEXT) + message
        if len(message) < BUFFER_SIZE:
            message = message + bytes(BUFFER_SIZE - len(message))
        s.send(message)
    s.close()
    f.close()

if __name__ == '__main__':
    main()
