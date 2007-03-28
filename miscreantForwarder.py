import socket
import select
#mySocket.send ( 'From:134.250.70.126to:MiscreantNamerdp') # carriage returns?
import sys


server = "planetlab1.byu.edu"
myUniqueMiscreantName = "roger_school"
socketToSendToLocalHost = 8888 
socketToConnectToProxy = 8001 # todo try two of them -- a list ;)


print "command line ref: localsocketin [8888], sockettoconnectforeign [8000]\n"

if len(sys.argv) > 1:
    socketToSendToLocalHost = int(sys.argv[1])

if len(sys.argv) > 2:
    socketToConnectToProxy = int(sys.argv[2])

infiniteLoop = True
keepGoing = True

print "attempting to connect to proxyserver %s:%d as miscreant %s " % (server, socketToConnectToProxy, myUniqueMiscreantName)
print "will establish incoming [through my connection on %d with proxy] to %s" % (socketToConnectToProxy, socketToSendToLocalHost)

while keepGoing:
 print "trying to connect again..."
 try:
    mySocketToSelf = [] #socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
    mySocketOut =  socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
    mySocketOut.connect((server, socketToConnectToProxy))
    mySocketOut.sendall(myUniqueMiscreantName) # that's it -- as long as it comes in the first packet we're good TODO this is a kinda bad way, though...
    print "success!"
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
                     print "establishing new inward socket to my own %d" % socketToSendToLocalHost
                     mySocketToSelf.connect(('localhost', socketToSendToLocalHost))
                 toSend = mySocketOut.recv(1000000)
                 if toSend:
                   closeLocation = toSend.find("control:close")
                   if closeLocation != -1:
                       localConnectionToSelfAlive = False # well it should be false
                       print "got a close signal--cutting it off to sockettoself"
                       toSend = toSend[0:closeLocation] # don't send that on, though it will close. Oh trust me--it will close :)
                   #vverbose
                   #print "sending [%s] in from internet to my internal socket" % toSend
                   mySocketToSelf.sendall(toSend)
    # todo bound this for errors...

                 else:
                     print "ack lost it to the proxy! todo\n"
                     break

             elif wroteToMe == mySocketToSelf:
                try:
                    toSend = mySocketToSelf.recv(1000000)
                     # verbose
                    #print "some from my local headed out [%s] " % toSend 
                except socket.error, e:
                    print "local connection dropped us."
                    localConnectionToSelfAlive = False
                  
                if toSend:
    # verbose                print "O",
                    mySocketOut.sendall(toSend)
                else:
                    localConnectionToSelfAlive = False
                    print "local client must have dropped us it's no longer around\n"

             else:
                print "weird!"

             if not localConnectionToSelfAlive:
                    print "telling proxy that socket here closed\n"
                    mySocketOut.sendall("control:close")
                    mySocketToSelf.close()
                    mySocketToSelf = []

    # verbose         print "T",
         else:
             #verbose print "select_z",
             pass

 except socket.error, e:
   print "socket exception!\n", e
 except KeyboardInterrupt:
   print "shutting down Ctrl-C\n"
 if not infiniteLoop:
     keepGoing = False
 mySocketOut.close()
 if mySocketToSelf:
     mySocketToSelf.close()

#ack! miscreant exception stops its thread! We are dead! todo :)

print "done finito!\n"
