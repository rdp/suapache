# Echo server program
import socket
import re # for string parsing
import threading
import select
import time

keepGoing = True

# multiple threads, with a shared object for deciding forwarding
class sharedList:

        def __init__(self):
                self.connectionList = {}
                self.miscreants = {} # dictionary of threaded, running objects
                self.lastCited = []

        def setupNextIncoming(self, fromIp, toHost):
                self.connectionList[fromIp] = toHost
                self.lastCited = toHost

        def addMiscreant(self, miscreantName, miscreantThatIsRunning):
                self.miscreants[miscreantName] = miscreantThatIsRunning

        def addAlien(self, alienConn, alienDetails):
                print "alien details are", alienDetails
                alienHost = alienDetails[0]
                if self.connectionList.has_key(alienHost):
                    miscreantName = self.connectionList[alienHost]
                    print "Bada boom appropriate connection alien to miscreant\n"
                else:
                    print "uh...we don't know how to map this! Guessing %s" % self.lastCited
                    miscreantName = self.lastCited
                if self.miscreants.has_key(miscreantName):
                    print "and connection made!\n"
                    self.miscreants[miscreantName].addAlien(alienConn)
                else:
                    print "no alien found with that name, though--giving up!\n"
                    

globalShared = sharedList()

class miscreant( threading.Thread ):
        def run ( self ):
             print 'Received starting miscreant connection:', self.details [ 0 ]
             try: 
              while keepGoing:
                 if self.miscreantChannel and self.alienChannel:
                         print "selecting on %s:%s -> %s:%s\n" % (self.miscreantChannel.getpeername(), self.miscreantChannel.getsockname(), self.alienChannel.getpeername(), self.alienChannel.getsockname())
                         (rr, wr, er) = select.select([self.miscreantChannel, self.alienChannel], [], [], 5)
                         alienDied = False
                         if rr:
                                print "doing a transfer or ending byte"
                                portWritingToUs = rr[0]
                                if portWritingToUs == self.miscreantChannel:
                                    receivedData = portWritingToUs.recv(1024) 
                                    if receivedData:
                                        try:
                                           self.alienChannel.sendall(receivedData)
                                        except socket.error, e:
                                           alienDied = True
                                    else:
                                        print "miscreant died!"
                                        self.miscreantChannel.close()
                                        self.miscreantChannel = [] # necessary?
                                        # todo take yourself out of the whole loop, really
                                        break 

                                elif portWritingToUs == self.alienChannel:
                                    try:
                                       receivedData = portWritingToUs.recv(1024) 
                                    except socket.error, e:
                                       alienDied = True
                                    if receivedData:
                                       self.miscreantChannel.sendall(receivedData) # assume this passes
                                    else:
                                        alienDied = True
# todo write to miscreant, inform of untimely death
                                if alienDied:
                                        print "Alien died somehow!\n"
                                        self.alienChannel.close()
                                        self.alienChannel = []
                         else:
                             print "z"
                         
                         if wr:
                             print "weird wr\n"

                         if er:
                             print "weirderr\n"

                 else:
                     print "d"
                     time.sleep(3)
             except socket.error, e:
                print e
                print "ack! miscreant exception stops its thread! We are dead!\n" # todo inform the other, or restart.
                self.miscreantChannel.close()
                self.alienChannel.close()

                   
        def addAlien(self, channel):
                self.alienChannel = channel

        def __init__(self, channel, details): # shamelessly lifted from http://www.devshed.com/c/a/Python/Basic-Threading-in-Python/1/
                self.miscreantChannel = channel # .send, .recv
                self.details = details
                self.alienChannel = []
                threading.Thread.__init__(self)

class miscreantAlienListener (threading.Thread):

        def run(self):
                HOST = ''                # Symbolic name meaning the local host
                PORT = 8000              # Arbitrary non-privileged port
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((HOST, PORT))
                s.listen(1)

                sAlien = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                alienPort = 3221
                sAlien.bind((HOST, alienPort))
                sAlien.listen(1)
                print "alien listening on port", alienPort
                print "miscreant listening on ", PORT
                
                while keepGoing:
                    r, w, e = select.select([s, sAlien], [], [], 3) # wait 3 seconds
                    
                    if r:
                        if r[0] == s:
                                conn, addr = s.accept()
                                print "got a miscreant connection by", addr
                                name = conn.recv(1024)
                                name = name.lower()
                                print "name", name
                                newMiscreant = miscreant(conn, addr)
                                newMiscreant.start()
                                globalShared.addMiscreant(name, newMiscreant)
                                print "added miscreant"
                        elif r[0] == sAlien:
                                conn, addr = sAlien.accept()
                                print "got a new alien connection by"
                                globalShared.addAlien(conn, addr)
                        else:
                                print "weird == ", r
                                a = r[0].accept() # throw it away
                                print "throwing away connection"
                sAlien.close() # clean-up
                s.close()
                
        
miscreantAlienListener().start()

# now the 
# changes in IP mapping part TODO make this a class, too.

HOST = ''                 # Symbolic name meaning the local host
PORT = 10005              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
try:
  while True:
        conn, addr = s.accept()
        print 'Connected by', addr
        data = conn.recv(1024)
        # note we don't do any error checking...

        data = data.lower() # lower case it
        # now we anticipate from:TheirIPto:rdp

        answers = re.search("from:(.*)to:(.*)", data)
        hostIp, data = answers.groups()

        print "I think that %s should next (and subsequently) go to %s\n" % (hostIp, data)
        if hostIp != "" and data != "":
                globalShared.setupNextIncoming(hostIp, data)
                conn.sendall("success in mapping!\n")
        else:
                conn.sendall("FAIL!\n")

        conn.close()
except KeyboardInterrupt: 
        print "shutting down"
        keepGoing = False
s.close()

# We also need to
# 1) accept from miscreant (on a different port), keep open
# 2) accepts incoming, appropriately forward to miscreant

