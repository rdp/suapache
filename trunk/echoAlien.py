import socket


mySocket =  socket.socket ( socket.AF_INET, socket.SOCK_STREAM )

# intro server
mySocket.connect( ('localhost', 10005))
mySocket.sendall ( 'From:127.0.0.1to:MiscreantNamerdp') # carriage returns?
#mySocket.sendall ( 'From:134.250.70.126to:MiscreantNamerdp') # carriage returns?
print mySocket.recv ( 1024 )
mySocket.close()

# Alien
myAlien =  socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
myAlien.connect(('localhost', 3221))
count = 1
while True:
    toSend = "abc%d" % count
    count += 1
    myAlien.sendall(toSend)
    gotBack = myAlien.recv(1024)
    print "%s == %s\n" % (toSend, gotBack)
    if toSend != gotBack:
        print "ack! not equal!\n"
#        break;
#
print "alien is done\n"
myAlien.close()

print "done!\n"
