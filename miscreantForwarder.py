import socket
import select
import sys

server = "planetlab1.byu.edu"
myUniqueMiscreantName = "roger_school"
socketToSendToLocalHost = 8888 
socketToConnectToProxy = 8000 # todo try two of them -- a list ;)

print "command line ref: localsocketin [8888], sockettoconnectforeign [8000], miscreantNameToBeKnownAs [%s]\n" % (myUniqueMiscreantName)

if len(sys.argv) > 1:
    socketToSendToLocalHost = int(sys.argv[1])

if len(sys.argv) > 2:
    socketToConnectToProxy = int(sys.argv[2])

if len(sys.argv) > 3:
    myUniqueMiscreantName = sys.argv[3]


infiniteLoop = True
keepGoing = True

print "will establish incoming [through my connection on %d with proxy] to %s" % (socketToConnectToProxy, socketToSendToLocalHost)
print "attempting to connect to proxyserver %s:%d as miscreant %s " % (server, socketToConnectToProxy, myUniqueMiscreantName)

while keepGoing:
 print "about to connect......"
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
                 toSend = mySocketOut.recv(1000000) # todo bound
                 #vverbose
                 #print "got [%s] from proxy heading in" % toSend
                 if toSend:
# assume that close comes before open...if it comes...todo some day have them all started/terminated...                       
                   closeLocation = toSend.find("control:close")
                   if closeLocation != -1:
                       localConnectionToSelfAlive = False # well it should be false
                       print "got a close signal--cutting it off to sockettoself"
                       toSend = toSend[0:closeLocation] # don't send that on, though it will close. Oh trust me--it will close :)

                   openLocation = toSend.find("control:open")
                   if openLocation != -1:
                       toSend = toSend[openLocation + 12:] # don't send on the open message...

                   #vverbose
                   #print "sending [%s] in from internet to my internal socket" % toSend
                   try:
                       mySocketToSelf.sendall(toSend)
                   except socket.error, e:
                        print "local connection dropped us."
                        localConnectionToSelfAlive = False
                 else:
                     print "ack lost it to the proxy! todo\n"
                     break

             elif wroteToMe == mySocketToSelf:
                toSend = ""
                try:
                    toSend = mySocketToSelf.recv(1000000)
                     # vverbose
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

 except KeyboardInterrupt:
   print "shutting down Ctrl-C\n"
   keepGoing = False
 except socket.error, e:
   print "ack random unhandled socket exception!\n", e


 mySocketOut.close()
 if mySocketToSelf:
     mySocketToSelf.close()

 if not infiniteLoop:
     keepGoing = False # only do loop once...

#ack! miscreant exception stops its thread! We are dead! todo :)

print "done finito!\n"
