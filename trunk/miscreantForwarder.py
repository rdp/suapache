import socket
import select
import sys

pingString = "PINGPONG@@@@!!!!"

# parameters -- vary these
myUniqueMiscreantName = socket.gethostname()
socketToSendToLocalHost = 3001 # this is the  

# more parameters, probably don't have to change
server = "planetlab1.byu.edu"
socketToConnectToProxy = 8000 # todo do two of them -- a list ;)

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
    mySocketToProxy =  socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
    mySocketToProxy.connect((server, socketToConnectToProxy))
    mySocketToProxy.sendall(myUniqueMiscreantName) # that's it -- as long as it comes in the first packet we're good TODO this is a kinda bad way, though...
    print "success! connections may now be mapped through %s as %s and will end up going to port %d" % (server, myUniqueMiscreantName, socketToSendToLocalHost)
    lastPingTime = time.time()
    while True:
         toListenTo = [mySocketToProxy]
         if mySocketToSelf:
             toListenTo += [mySocketToSelf] 
         readMe, writeMe, errors = select.select(toListenTo, [], [], 5)
         # ping every 15 s
         if time.time() - lastPingTime > 15:
            mySocketToProxy.sendall(pingString)
         # ha ha :)
         if readMe:
             localConnectionToSelfAlive = True
             shouldSendOutBreak = False
             wroteToMe = readMe[0]
             if wroteToMe == mySocketToProxy:
                 if not mySocketToSelf:
                     mySocketToSelf = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
                     print "establishing new inward socket to my own %d" % socketToSendToLocalHost
                     mySocketToSelf.connect(('localhost', socketToSendToLocalHost))
                 toSend = mySocketToProxy.recv(1000000) # todo bound
                 #vverbose
                 #print "got [%s] from proxy heading in" % toSend
                 if toSend:
# assume that close comes before open...if it comes...todo some day have them all started/terminated...                       
                   closeLocation = toSend.find("control:close")
                   
                   if closeLocation != -1:
                       localConnectionToSelfAlive = False # well it should be false
                       shouldSendOutBreak = False
                       print "got a close signal--cutting it off to sockettoself"
                       toSend = toSend[0:closeLocation] # don't send that on, though it will close. Oh trust me--it will close :)

                   openLocation = toSend.find("control:open")
                   if openLocation != -1:
                       toSend = toSend[openLocation + 12:] # don't send on the open message...

                   pingLocation = toSend.find(pingString)
                   if pingLocation != -1:
                           print "got ping!\n"
                           assert len(toSend) == len(pingString)
                           toSend = ""

                   #vverbose
                   #print "sending [%s] in from internet to my internal socket" % toSend
                   try:
                       mySocketToSelf.sendall(toSend)
                   except socket.error, e:
                        print "local connection dropped us."
                        localConnectionToSelfAlive = False
                        shouldSendOutBreak = True
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
                    shouldSendOutBreak = True

                if toSend:
    # verbose                print "O",
                    mySocketToProxy.sendall(toSend)
                else:
                    # at this point this means that we read from the inside connection, it gave us nothing (had closed)
                    localConnectionToSelfAlive = False
                    shouldSendOutBreak = True
                    print "local connection dropped us 2"

             else:
                print "weird!"

             if not localConnectionToSelfAlive and shouldSendOutBreak:
                    print "telling proxy that socket here closed\n"
                    mySocketToProxy.sendall("control:close")
                    mySocketToSelf.close()
                    mySocketToSelf = []

            # verbose
             print "Transfer_occurred",
         else:
             #verbose
             print "select_z", mySocketToProxy.getpeername()
             pass

 except KeyboardInterrupt:
   print "shutting down Ctrl-C\n"
   keepGoing = False
 except socket.error, e:
   print "ack random unhandled socket exception!\n", e


 mySocketToProxy.close()
 if mySocketToSelf:
     mySocketToSelf.close()

 if not infiniteLoop:
     keepGoing = False # only do loop once...

#ack! miscreant exception stops its thread! We are dead! todo :)

print "done finito!\n"
