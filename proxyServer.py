# Echo server program
import socket
import re # for string parsing
import threading
import select
import time
import sys
import re

pingString = "PINGPONG@@@@!!!!"
socket.setdefaulttimeout(15) # set a default timeout for blocking actions -- note that this does not work because blocking means "the interior socket buffer is full" 
# however sendall still...uh..."sends" it (puts it in the buffer but it is not actually received)...uh...um...this is bad.

keepGoing = True
# 
# multiple threads, with a shared object for deciding forwarding
class sharedList:

        def __init__(self):
                self.connectionList = {}
                self.miscreants = {} # dictionary of threaded, running objects
                self.lastCited = "fake_roger_code starting last cited--if you see this it may mean that you haven't set up the mapping from the alien side yet"

        def setupNextIncomingAlien(self, fromIp, toHost):
		print "setupnextincominglaien from %s to %s" % (fromIp, toHost)
		if toHost:
	                self.connectionList[fromIp] = toHost
        	        self.lastCited = toHost
			print "setting lastCited to [%s]" % [toHost]
		else:
			print "ERROR ack why am I passed nothing? [%s] [%s]" % (fromIp, toHost)

        def addMiscreant(self, miscreantName, miscreantThatIsRunning):
                self.miscreants[miscreantName] = miscreantThatIsRunning
		#if self.lastCited.find("fake_roger_code") == 0: # we are just barely beginning.. todo someday :)
                self.lastCited = miscreantName
                print "using this [%s] as the lastCited miscreant, as well...just in case...might want to take this off todo..." % (miscreantName)

	def tryToHookAlien(self, miscreantName, alienConn):
	  try:
	     print "trying to hook to %s" % (miscreantName)
	     assert self.miscreants.has_key(miscreantName)
	     self.miscreants[miscreantName].addAlien(alienConn)
             print "success."
	     return True
          except socket.error, e:
            print "ack! failure adding alien to [%s] ERROR!" % (miscreantName)
	    return False

        def mapAlien(self, alienConn, alienDetails):
                print "incoming alien details (we are adding this one) are", alienDetails
                alienHost = alienDetails[0]
		alienHostBeginningThree = re.match("\d+\.\d+\.\d+", alienDetails[0]).group() # todo make this into a lib, as it is shared among two files

                if self.connectionList.has_key(alienHost): 
                    miscreantName = self.connectionList[alienHost]
                    print "Bada boom appropriate connection alien with full IP match!"
                elif self.connectionList.has_key(alienHostBeginningThree):
		   miscreantName = self.connectionList[alienHostBeginningThree]
		   print "made a connection using only first 3 of incoming ip..."
		else:
                   print "uh...we don't know how to map this! Guessing latest mapped in request...[%s]" % self.lastCited
                   miscreantName = self.lastCited
		   if not miscreantName:
			print "ERROR uh...lastCited was poorly set!"
			print "I think this is false, though that it has it...", self.miscreants.has_key(miscreantName)
	
                if self.miscreants.has_key(miscreantName):
                    print "mapping to miscreant [%s]...." % (miscreantName),
		    if not self.tryToHookAlien(miscreantName, alienConn):
			print "ack! adding it to [%s] failed ERROR deleting it!"
			del self.miscreants[miscreantName]
			if self.lastCited == miscreantName:
				if self.miscreants:
					self.lastCited = self.miscreants.keys()[0]
					print "Changing lastCited back to %s" % (self.lastCited)
					print "trying to connect with that..."
					self.tryToHookAlien(self.lastCited, alienConn)	
				else:
					print "ACK no more current hosts for lastCited! Giving up!"
					alienConn.sendall("Attempt to connect failed, and no more connections exist") # this won't block...
					alienConn.close
                else:
                    errorMessage =  "no miscreant found with that name [%s], though--giving up!!!!\n (may need to remap client and/or restart miscreant)" % (miscreantName)
                    print errorMessage
                    alienConn.send(errorMessage)
                    alienConn.close()
                    

globalShared = sharedList()

class miscreant( threading.Thread ):
        def run ( self ):
             print 'Received starting miscreant connection:', self.details [ 0 ]
             try: 
              while keepGoing:
		 	 listenToArray = [self.miscreantChannel]
		 	 if self.alienChannel:
				listenToArray += [self.alienChannel]
                         (rr, wr, er) = select.select(listenToArray, [], [], .5)
                         alienDied = False
                         if rr:
                                # verboseprint "R",
                                portWritingToUs = rr[0]
                                if portWritingToUs == self.miscreantChannel:
                                    receivedData = portWritingToUs.recv(1024000) 
				    #vverbose
				    #print "received [%s] from miscreant " % receivedData
                                    if receivedData:
                                      pingLocation = receivedData.find(pingString)
                                      if pingLocation != -1:
                                           print "got ping!\n"
                                           assert len(receivedData) == len(receivedData)
                                           continue
                                            
                                      controlLocation = receivedData.find("control:close")
                                      if controlLocation != -1:
                                          alienDied = True
                                          receivedData = receivedData[0:controlLocation] # strip that off
                                          print "sent us a close message out from miscreant so will send residue, kill with alien"
                                    
                                      try:
                                        #verbose print "S", 
					#vverbose
					#print "sending [%s] to alien" % receivedData
                                        if self.alienChannel:
						#verbose
						print " a << m "
						self.alienChannel.sendall(receivedData)
					else:
						print "unable to send packet out to alien--already dead!"
                                      except socket.error, e:
                                            # toast that outgoing connection
                                            alienDied = True # well, kind of it died :)
                                            print "alien arbitrarily cut off"
                                    else:
                                        print "miscreant tunnel died whoa!"
                                        self.miscreantChannel.close()
                                        self.miscreantChannel = [] # necessary?
                                        # todo take yourself out of the whole loop, really
                                        break 

                                elif portWritingToUs == self.alienChannel:
                                    try:
                                       receivedData = portWritingToUs.recv(1024000) 
				       # vverbose
				       #print "received %s from Alien, passing through" % (receivedData)
                                    except socket.error, e:
                                       alienDied = True
                                    if receivedData:
				       #verbose
				       print " a >> m ",
                                       self.miscreantChannel.sendall(receivedData) # assume this passes
                                    else:
                                        alienDied = True
# todo write to miscreant, inform of untimely death
                                if alienDied and self.alienChannel: # todo why this and ____ ?
                                        print "Alien died somehow  -- sending control message!\n"
					self.alienChannel.close()
                                        self.alienChannel = []
                                        self.miscreantChannel.sendall("control:close") # died from here
                                        print "sending in to miscreant that alien closed"
					# for now flush--in the future could just ignore it on an old closed tunnel port
                         else:
                             #verbose
			     print "miscreant_thread_z_x",
			     pass
                         
                         if wr:
                             print "weird wr\n"

                         if er:
                             print "weirderr\n"

              print "Done with this alien because keepGoing is done...or something!"
             except socket.error, e:
                print e
                print "ack! miscreant exception stops its thread! We are dead! Miscreant is dead\n" # todo inform the other, or restart., take it off list...
                self.miscreantChannel.close()
                if self.alienChannel: # todo this is weird
			self.alienChannel.close()

                   
        def addAlien(self, channel):
		if self.alienChannel:
			print "experimental closure of old alien"
			self.alienChannel.close()
			self.miscreantChannel.sendall("control:close") # died from here the question is what of remaining 'junk' on its way will get there todo
		try:
                	self.miscreantChannel.sendall("control:open")

			self.alienChannel = channel
		except socket.error, e:
			print "uh...miscreant has DIED ERROR -- we tried to send miscreant control:open and it crashed"
			raise

        def __init__(self, channel, details): # shamelessly lifted from http://www.devshed.com/c/a/Python/Basic-Threading-in-Python/1/
                self.miscreantChannel = channel # .send, .recv
                self.details = details
                self.alienChannel = []
                threading.Thread.__init__(self)

class miscreantAlienListener (threading.Thread):

        def __init__(self, alienBindPortAsInteger, miscreantBindPort = 8000): # this is weird I can't seem to pass this to run. Oh well :)
                self.alienBindPort = alienBindPortAsInteger
		self.miscreantBindPort = miscreantBindPort
                threading.Thread.__init__(self)

        def run(self):
		# todo report to ruby that '' does NOT work in windows...uh...should it?
                HOST = ''                		# Symbolic name meaning the local host
	      # todo make this loop--the listener upchucks every so often for some reason (todo figure out why)
	# todo: when it dies the other should notice getpeername
		try:
		# s is the main socket from which miscreants will attach in
                  sMiscreant = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                  sAlien = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                  alienPort = self.alienBindPort
                  print "Port:%d alien will listen on port" % alienPort
                  print "Port:%d miscreant listening on "% self.miscreantBindPort
                  
		  sMiscreant.bind((HOST, self.miscreantBindPort))
                  sMiscreant.listen(1)
                  
		  sAlien.bind((HOST, alienPort))
                  sAlien.listen(1)
                  
                  while globals()["keepGoing"]: # python bug
                      r, w, e = select.select([sMiscreant, sAlien], [], [], 1) # wait 1 second
                      
                      if r:
                          if r[0] == sMiscreant:
                                  conn, addr = sMiscreant.accept()
                                  print "got a connection by", addr
                                  name = conn.recv(1024000)
                                  name = name.lower()
				  if name.find("get http://") == -1:
                                    print "miscreant name will be %s" % name
                                    newMiscreant = miscreant(conn, addr)
                                    newMiscreant.start()
                                    globalShared.addMiscreant(name, newMiscreant)
				  else:
				    print "discarding miscreant (I think it's fake)[%s]" % name
                          elif r[0] == sAlien:
                                conn, addr = sAlien.accept()
                                print "got a new alien connection by ", addr[0]
				try:
                                	globalShared.mapAlien(conn, addr)
				except socket.error, e:
					print "ERROR", e
					print "Tried to add Alien and it died on us in that process!"
					conn.sendall("internal error died adding you")
					conn.close
					
                          else:
                                print "weird == ", r
                                a = r[0].accept() # throw it away
                                print "throwing away connection"
		      else:
				print "miscreant_alien_z_2",
                  print "done here because of keepGoign dying miscreant/alien listening pouncer\n"
                except socket.error, e:
		  print "THE MISCREANT LISTENER CHOKED (or alien listener) socket.error!%d" % self.miscreantBindPort , e
			
		sAlien.close() # clean-up
                sMiscreant.close()
                print "we closed the main miscreant connecting port %d!, instructed rest to conk... TODO" % (self.miscreantBindPort)
		globals()["keepGoing"] = False # todo
		print "z_2 closed it"
		


# process command line args...                
print "command line args are: alien bind [3221], incomingMapsToPort [10005], miscreantBindPort [8000]"

if len(sys.argv) >= 2:
    alienListenerBindPort = int(sys.argv[1])
else:
    alienListenerBindPort = 3221

if len(sys.argv) >= 3:
  incomingMapsToPort= int(sys.argv[2])
else:
  incomingMapsToPort = 10005

if len(sys.argv) >= 4:
  miscreantBindPort = int(sys.argv[3])
else:
  miscreantBindPort = 8000

miscreantAlienListener(alienListenerBindPort, miscreantBindPort).start()
time.sleep(1) # give us a chance to see if it is toast...
print "continuing"

# now the IP mapping listener...
# TODO make this a class, too.

HOST = ''                 # Symbolic name meaning the local host
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Port:%d  is incoming alien to miscreant mapper listener :)" % (incomingMapsToPort)
try:
  s.bind((HOST, incomingMapsToPort))
  s.listen(1)
  while keepGoing:
        r, w, e = select.select([s], [], [], 1) # wait 1 seconds
                     
        if r:
             if r[0] == s:        
                conn, addr = s.accept() # todo this needs to become a listen...ack!
                print 'Connected by', addr
                data = conn.recv(1024000)
                # note we don't do any error checking...

                data = data.lower() # lower case it
                # now we anticipate from:TheirIPto:rdp

                answers = re.search("from:(.*)to:(.*)", data)
                hostIp, miscreantName = answers.groups()

                print "I think that %s should next (and subsequently) go to %s\n" % (hostIp, miscreantName)
                if hostIp != "" and miscreantName != "":
                        globalShared.setupNextIncomingAlien(hostIp, miscreantName)
                        myIPAddress = socket.gethostbyname(socket.gethostname())
                        outputString = "success in mapping--%s on my port %d will go to %s! \n" % (hostIp, alienListenerBindPort, miscreantName)
                        outputString += "Or %s:%d => %s\n" % (myIPAddress, alienListenerBindPort, miscreantName)
                        conn.sendall(outputString) # we combine the above lines so that we can worry about parsing a single packet on the incoming.
                        print "success"
                else:
                        conn.sendall("FAIL!\n")
                        print "fail"

                conn.close()
             else:
                    print "errrrr"
        else:
               #verbose
               print "mapper_z_1",
               
  print "done with mapping listener\n"
except KeyboardInterrupt: 
        print "shutting downi Ctrl-C"
except socket.error, e:
	print "shutting down socket error with the alien listener for mapping"

s.close()
print "successfully closed alien port"
keepGoing = False
print "z_1 closed keepGoing"
time.sleep(2) # let the threads clean themselves up TODO take this out--they should still work, I think...

