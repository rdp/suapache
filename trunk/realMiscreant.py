import socket
import select
#mySocket.send ( 'From:134.250.70.126to:MiscreantNamerdp') # carriage returns?

mySocketOut =  socket.socket ( socket.AF_INET, socket.SOCK_STREAM )

mySocketOut.connect(('localhost', 8000))
mySocketOut.sendall('MiscreantNamerdp') # that's it -- as long as it comes in the first packet we're good TODO


mySocketToSelf = [] #socket.socket ( socket.AF_INET, socket.SOCK_STREAM )

try:
 while True:
     toListenTo = [mySocketOut]
     if mySocketToSelf:
         toListenTo += [mySocketToSelf] 
     readMe, writeMe, errors = select.select(toListenTo, [], [], 5)

     if readMe:
         localConnectionToSelfAlive = True
         wroteToMe = readMe[0]
         if wroteToMe == mySocketOut:
             if not mySocketToSelf:
                 mySocketToSelf = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
                 mySocketToSelf.connect(('', 3222)) # todo prod
             mySocketToSelf.sendall(wroteToMe.recv(10000))
         elif wroteToMe == mySocketToSelf:
            print "some from my local headed out"
            try:
                toSend = mySocketToSelf.recv(10000)
            except socket.error, e:
                print "local connection dropped us."
                localConnectionToSelfAlive = False
              
            if toSend:
                mySocketOut.sendall(toSend)
            else:
                localConnectionToSelfAlive = False
                print "local client must have dropped us it's no longer around\n"

            if not localConnectionToSelfAlive:
                mySocketToSelf.close()
                mySocketToSelf = []
         else:
            print "weird"

     else:
         print "uh...nothing in or out\n"
     
except KeyboardInterrupt:
  print "shutting down\n"

# todo aggressively reconnect or something...in big server says (107, 'Transport endpoint is not connected')
#ack! miscreant exception stops its thread! We are dead!


mySocketOut.close()
if mySocketToSelf:
    mySocketToSelf.close()
print "done!\n"
