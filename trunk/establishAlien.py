import socket
import sys
import re # regular expressions for IP address parsing


# intro server
def match(alienIP, host):
  mySocket =  socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
  mySocket.connect( ('localhost', 10005))
  mySocket.sendall ( 'From:%sto:%s' % (alienIP, host))
  returnString = ""  
  returnString += "got back from mapping request:" + mySocket.recv ( 1024 )
  mySocket.close()

  print "done mapping %s to %s! [received %s]\n" % (alienIP, host, returnString)
  ipOut = ""
  portOut = ""
  pattern = re.compile(".* (\d+\.\d+\.\d+\.\d+):(\d+) => \w+.*", re.DOTALL)
  a =  re.match(pattern, returnString)
  if a:
    ipOut = a.groups()[0]
    portOut = a.groups()[1]
    print "internal: in match got ip %s port %s\n" % (ipOut, portOut)
  else:
	print "did not match with %s\n" % returnString
 
  return returnString, ipOut, portOut

#testing code:
#match("127.0.0.1", "MiscreantNamerdpCanned")
#match("127.0.0", "MiscreantNamerdpCanned")

# Basic web server lifted from a web page...
import socket

host = ''
port = 7777
print "listening on port %d for incoming HTTP requests which I will then map to the right place" % (port)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind((host,port))
sock.listen(1)

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
  miscreantName = re.match(".*mapMeTo=(\w*)", line)
  if not miscreantName:
	miscreantName =  re.match(".*mapToMe=(\w*)", line)
  if miscreantName:
 	miscreantDesired = miscreantName.groups()[0]
 	connectionReturnString = "Got miscreantDesired of " + miscreantDesired
	connectionReturnString += match(ipAddressOfIncomingAlien,miscreantDesired)[0]
	successMapping = match(firstThreePartsOfIP, miscreantDesired)
	connectionReturnString += successMapping[0]
	if successMapping[1] and successMapping[2]:
		host = successMapping[1]
		port = successMapping[2]
		connectionReturnString += "or try <a href=http://%s:%s>http://%s:%s</a>" % (host, port, host, port)

  if line == '': # ran into one newline...not the best way to do it, but hey :)
   print "string is now", connectionReturnString
   cfile.write("HTTP/1.0 200 OK\n\n")
   cfile.write("<head><title>Eh?</title></head>")
   cfile.write("<h1>Returned this value:[" + connectionReturnString + "]</h1>")
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
    
