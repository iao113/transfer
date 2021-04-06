#!/usr/bin/env python3

import os
import socket
import sys

from CommonPython.header import Header, HEAD_SIZE

def headDecoder(messageHead: bytes) -> Header:
    header = None
    for headTerm in Header:
        if messageHead[headTerm.value.index] == headTerm.value.value:
            if header == None:
                header = headTerm
            else:
                raise ValueError
    return header

def main():
    TCP_IP = ''
    TCP_PORT = 11030
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(5)

    while 1:
        conn, addr = s.accept()
        print('Connection address:', addr)
        filename = ''
        filesize = None
        f = None
        while 1:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            while len(data) < BUFFER_SIZE:
                data = data + conn.recv(BUFFER_SIZE - len(data))
            header = headDecoder(data[0:HEAD_SIZE])
            if header == Header.FILE_NAME:
                try:
                    filename += data[HEAD_SIZE:].decode('utf-8').strip('\x00')
                except UnicodeDecodeError as e:
                    sys.stderr.write(str(e))
                    sys.stderr.write('\nClient sent wrong filename.\n')
                    break
            elif header == Header.FILE_SIZE:
                if filesize == None:
                    filesize = int.from_bytes(data[HEAD_SIZE:], byteorder='big')
                else:
                    sys.stderr.write('Client did not send the filesize.\n')
                    break
            elif header == Header.FILE_CONTEXT:
                try:
                    try:
                        filesize -= f.write(data[HEAD_SIZE:HEAD_SIZE + filesize])
                    except AttributeError:
                        if os.path.exists(filename):
                            sys.stderr.write('Client sent same file.\n')
                            break
                        f = open(filename, 'wb')
                        filesize -= f.write(data[HEAD_SIZE:HEAD_SIZE + filesize])
                except FileNotFoundError:
                    sys.stderr.write('Client did not send the filename.\n')
                    break
        if filesize != None and filesize != 0:
            sys.stderr.write('Client did not send the full file, remains {size} byte(s).\n'.format(size=filesize))
        if f != None and not f.closed:
            f.close()
        conn.close()

if __name__ == '__main__':
    main()
