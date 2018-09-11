#!/usr/bin/env python
# -*- coding=utf-8 -*-


"""
file: recv.py
socket service
"""


import socket
import threading
import time
import sys
import os
import struct

HOST = ''
PORT = '9999'

def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', 6666))
        s.listen(True)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('Waiting connection...')

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()

def deal_data(conn, addr):
    print('Accept new connection from {}'.format(addr))
    #conn.settimeout(500)
    conn.send(b'Hi, Welcome to the server!')

    while 1:
        fileinfo_size = struct.calcsize('128sl')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            filename = filename.decode('utf-8')
            fn = filename.strip('\00')
            new_filename = os.path.join('/home/skylu/Desktop/TCP/Download', 'new_' + fn)
            print('file new name is {0}, filesize if {1}'.format(new_filename,filesize))

            recvd_size = 0  # 定义已接收文件的大小

            with open(new_filename, 'wb') as fp:
                print('start receiving...')

                while not recvd_size == filesize:
                    if filesize - recvd_size > 1024:
                        print("Processing:{0}%".format(round((recvd_size) * 100 / filesize)), end="\r")
                        time.sleep(0.5)
                        data = conn.recv(1024)
                        recvd_size += len(data)
                    else:
                        data = conn.recv(filesize - recvd_size)
                        recvd_size = filesize
                    fp.write(data)
            print('end receive...')
        break

    conn.close()


if __name__ == '__main__':
    socket_service()