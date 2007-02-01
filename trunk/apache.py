#!/usr/bin/env python

"""
A simple echo server
"""

import socket

host = ''
port = 3222
backlog = 5
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)
while 1:
        client, address = s.accept()
        data = client.recv(size)
        print "received", data
        if data:
            client.sendall("HTTP/1.0 200 OK\r\n\r\nThis is web. It really really really is. html head footer etc. etc. hee hee\r\n\r\n\r\n")
        print "done sending\n"
        client.close()
