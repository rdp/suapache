order:

HTML: who would you like to reach? (with port) rdp port? _3122_
[Enter](Enter.md)

contact planetlab1.byu.edu:10005 tells it "next connection from you [ip](ip.md) is to rdp"
assume it will be open for you to attach (TCP), and say the following "from:TheirIPto:rdp" and cut the connection.

to the user it returns (next page): "use http://planetlab1.byu.edu:3122" from ip, until instructed otherwise.

Done with your part.

assumes that we don't need to multiplex,

on planetlab1.byu.edu smart forwarder (cake),


The miscreant one needs, in python, to go to planetlab1 some arbitrary port and connect and assume that incoming data is from clients going to port 3122, one at a time (or rather, forward that data to a new connection to localhost:3122).