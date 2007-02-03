import socket
import sys

mySocket =  socket.socket ( socket.AF_INET, socket.SOCK_STREAM )

# intro server
mySocket.connect( ('localhost', 10005))
mySocket.sendall ( 'From:127.0.0.1to:MiscreantNamerdp') # carriage returns?
#mySocket.sendall ( 'From:134.250.70.126to:MiscreantNamerdp') # carriage returns?
print mySocket.recv ( 1024 )
mySocket.close()

# Alien
myAlien =  socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
if len(sys.argv) >= 2:
    portToConnectTo = int(sys.argv[1])
else:
    portToConnectTo = 3221
print "connecting to proxyServer on its port ", portToConnectTo
myAlien.connect(('localhost', portToConnectTo))
count = 1
while True:
    toSend = "abc%d" % count
    count += 1
    myAlien.sendall(toSend)
    gotBack = myAlien.recv(1024)
    if not gotBack:
        print "done with that connection!"
        myAlien.close()
        myAlien.connect(('localhost', portToConnectTo))

    print "%s == %s\n" % (toSend, gotBack)
    if toSend != gotBack:
        print "ack! not equal!\n"
#        break;

# never gets here or past here
print "alien is done\n"
myAlien.close()

print "done!\n"
