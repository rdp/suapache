#!/usr/bin/env python

"""
A simple echo server
"""

import socket
import sys
import time # this is no longer a simple apache :)

host = ''
port = 3222
if len(sys.argv) >= 2:
    port = int (sys.argv[1])
print "reasonable apache listening on port ", port

backlog = 1
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)
while 1:
        client, address = s.accept()
        data = client.recv(size)
        print "received", data
        toSend ="HTTP/1.0 200 OK\r\n\r\nThis is web. It really really really is. html head footer etc. etc. hee hee\r\n\r\n\r\n" 
        if data:
            client.sendall(toSend)
        print "done sending\n"
        client.close()
#        time.sleep(1)
# todo -- debug: if this is too fast then it sends the message late to the serverproxy (which I think is actually ok since it didn't open or close- - wait that's right ;)


