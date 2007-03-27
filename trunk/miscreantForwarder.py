import socket
import select
#mySocket.send ( 'From:134.250.70.126to:MiscreantNamerdp') # carriage returns?
import sys


server = "planetlab1.byu.edu"
myUniqueMiscreantName = "roger_school"
socketToSendToLocalHost = 8888 # could be over written by command line

mySocketOut =  socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
mySocketOut.connect((server, 8000))
mySocketOut.sendall(myUniqueMiscreantName) # that's it -- as long as it comes in the first packet we're good TODO this is a kinda bad way, though...

if len(sys.argv) > 1:
    socketToSendToLocalHost = int(sys.argv[1])

print "attempting to connect to proxyserver %s as miscreant %s " % (server, myUniqueMiscreantName)
print "will establish incoming [through my connection on 8000 with proxy] to ", socketToSendToLocalHost

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
                 print "establishing socket to my own %d" % socketToSendToLocalHost
                 mySocketToSelf.connect(('localhost', socketToSendToLocalHost))
# todo if this fails [port is closed but just output something, not die]
             toSend = mySocketOut.recv(1000000)
             if toSend:
               closeLocation = toSend.find("control:close")
               if closeLocation != -1:
                   localConnectionToSelfAlive = False # well it should be false
                   print "got a close signal--cutting it off to sockettoself"
                   toSend = toSend[0:closeLocation] # don't send that on, though it will close. Oh trust me--it will close :)
               print "sending [%s] in" % toSend
               mySocketToSelf.sendall(toSend)
# todo bound this

             else:
                 print "ack lost it to the proxy! todo\n"
                 break
         elif wroteToMe == mySocketToSelf:
            print "some from my local headed out"
            try:
                toSend = mySocketToSelf.recv(1000000)
            except socket.error, e:
                print "local connection dropped us."
                localConnectionToSelfAlive = False
              
            if toSend:
                print "O",
                mySocketOut.sendall(toSend)
            else:
                localConnectionToSelfAlive = False
                print "local client must have dropped us it's no longer around\n"

            if not localConnectionToSelfAlive:
                print "telling proxy that socket here closed\n"
                mySocketOut.sendall("control:close")
                mySocketToSelf.close()
                mySocketToSelf = []
         else:
            print "weird!"
         print "T",
     else:
         print "z",
     
except KeyboardInterrupt:
  print "shutting down Ctrl-C\n"

# todo aggressively reconnect or something...in big server says (107, 'Transport endpoint is not connected')
#ack! miscreant exception stops its thread! We are dead!

mySocketOut.close()
if mySocketToSelf:
    mySocketToSelf.close()
print "done finito!\n"
