import socket

#mySocket.send ( 'From:134.250.70.126to:MiscreantNamerdp') # carriage returns?

mySocket =  socket.socket ( socket.AF_INET, socket.SOCK_STREAM )

mySocket.connect(('localhost', 8000))
mySocket.send('MiscreantNamerdp') # that's it -- as long as it comes in the first packet we're good TODO

# the echo miscreant :)

try:
 while True:
     a = mySocket.recv(1024)
     if not a:
         break
     mySocket.sendall(a)
     print "echoing ", a, "\n"
except KeyboardInterrupt:
  print "shutting down\n"
print "done!\n"
