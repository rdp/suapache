import socket
import sys
import re # regular expressions for IP address parsing


# intro server
def match(alienIP, host):
 returnString = ""  
 ipOut = ""
 portOut = ""
 miscreantThoughtWas = ""
 for port in (10005, 10006):
  try:
   print "trying port %d\n" % port
   mySocket =  socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
   mySocket.connect( ('localhost', port))
   mySocket.sendall ( 'From:%sto:%s' % (alienIP, host))
   returnString += "got back from mapping request:" + mySocket.recv ( 1024 )
   mySocket.close()
 
   print "done mapping %s to %s! [received %s]\n" % (alienIP, host, returnString)
   pattern = re.compile(".* (\d+\.\d+\.\d+\.\d+):(\d+) => ([\w_]+).*", re.DOTALL)
   a =  re.match(pattern, returnString)
   if a:
     ipOut = a.groups()[0]
     portOut = a.groups()[1]
     miscreantThoughtWas = a.groups()[2]
     print "internal: in match got ip %s port %s\n" % (ipOut, portOut)
   else:
     print "DID NOT MATCH with %s\n" % returnString
  except socket.error, e:
    print "that port didn't work!\n", e
 
 return returnString, ipOut, portOut, miscreantThoughtWas

#testing code:
#match("127.0.0.1", "MiscreantNamerdpCanned")
#match("127.0.0", "MiscreantNamerdpCanned")

# Basic web server lifted from a web page...
import socket

host = ''
port = 7777
print "Port:%d incoming HTTP requests which I will then map to the right miscreant by connecting to mapper" % (port)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind((host,port))
sock.listen(1)


totalIn = 0

while 1:
 csock,caddr = sock.accept()
 cfile = csock.makefile('rw',0)
 print caddr # == csock.getpeername(), for notes' sake

 ipAddressOfIncomingAlien = caddr[0]
 print "got ip incoming of %s" % (ipAddressOfIncomingAlien)
 
 firstThreePartsOfIP = re.match("\d+\.\d+\.\d+", ipAddressOfIncomingAlien).group()

# Protocol exchange - read request
 connectionReturnString = ""
 while 1:
  line = cfile.readline().strip()
#  print line
  miscreantName = re.match(".*mapmeto=(\w*)", line.lower())
  if miscreantName:
 	miscreantDesired = miscreantName.groups()[0]
 	connectionReturnString = "Parsed your request: You desired miscreant name " + miscreantDesired
	connectionReturnString += match(ipAddressOfIncomingAlien,miscreantDesired)[0]
	successMapping = match(firstThreePartsOfIP, miscreantDesired)
	connectionReturnString += successMapping[0]
	if successMapping[1] and successMapping[2]:
		host = successMapping[1]
		port = successMapping[2]
		miscreant = successMapping[3]
		connectionReturnString = "Success mapping you to %s!<p>" % (miscreantDesired)
		connectionReturnString += "or %s:%s => <a href=http://%s:%s>%s</a>" % (host, port, host, port, miscreantDesired)	
		connectionReturnString += "<p>Try <a href=http://%s:%s>this link.<a>" % (host, port)
		redirectToLocation = re.match(".*redirectto=[%s].*")
		if redirectToLocation:
			pathString = redirectLocation.groups()[0]
		  	connectionReturnString += "<META HTTP-EQUIV=\"Refresh\" CONTENT=\"1; URL=http://%s:%s/%s\">" % (host, port, pathString)
			print "redirecting to %s"  % (pathString)
	else:
	  connectionReturnString += "error connecting into mapper (or parsing it) for some reason -- proxyServer might be down"

  if line == '': # ran into one newline...not the best way to do it, but hey :)
   print "string is now", connectionReturnString
   cfile.write("HTTP/1.0 200 OK\n\n")
   cfile.write("<head><title>Eh? %d</title></head>" % totalIn)
   totalIn += 1
   cfile.write("<h1>" + connectionReturnString + "</h1>")
   cfile.close()
   csock.close()
   break # break out of this interior loop...
   connectionReturnString = ""
   

# todo someday use basichttpserver...alas...
class Csikk(SimpleHTTPRequestHandler):
    """
    main request handler class for csikk.
    """
    
    server_version = "Csikk HTTPD/%s" % __version__
    sessid = None
    
    def __init__(self, request, client_address, server):
        SimpleHTTPRequestHandler.__init__(self, request,
        client_address, server)
        self.init_session()

        print "[csikk] request [SID#%s] from %s" % (str(self.sessid),
        ":".join(map(lambda x: str(x), client_address)))
    
