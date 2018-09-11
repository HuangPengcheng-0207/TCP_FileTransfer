#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
file: send.py
socket client
"""

import socket
import os
import sys
import struct

def send_file(s):
    while True:
        filepath = input('please input file path: ')
        if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包含文件名和文件大小
            fhead = struct.pack('128sl', os.path.basename(filepath).encode('utf-8'),os.stat(filepath).st_size)
            s.send(fhead)
            print('client filepath: {}'.format(filepath))
            fp = open(filepath, 'rb')
            while True:
                data = fp.read(1024)
                if not data:
                    print('{} file send over...'.format(filepath))
                    break
                s.send(data)
        break

def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 6666))
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print(s.recv(1024).decode('utf-8'))

    send_file(s)

    s.close()


if __name__ == '__main__':
    while True:
        socket_client()
