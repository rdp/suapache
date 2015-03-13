# Introduction #
v 00:
Code lacks working with PHP, setup, leave running, test. Could be fascinating :)
Then, AFAIK it should work for limited use, especially with PHP. We can even host the PHP portion on planetlab1.byu.edu and just point there for setup, and it should just work for open communication on a few ports if you so desire it.

v 01:
multiplexing, round robin among good hosts with one central

v 02:

Moderate protection speed-wise. At least fair queueing.

# Random thots #

What about injecting raw packets onto the wire locally, that "say" they are from this other host, then (I guess) listen on the wire for packets 'to' this IP. Don't know if this is possible, but if it were would this be a benefit?

Might be nice to have "our system" interface with jxta, or even contribute to it. I don't know what that would mean exactly. Hmm. We seem to already do what they do.

We could do the HTML 'map me a port' AND the DNS 'map me a port' where HTML might be more accurate, but both would seem to work, and HTML is less automatic, but hey.

Nice might be 'instructions' to the miscreant server to 'establish another connection with so and so' type of thing.

Could use tracepath to supplement the IP mask.

Load Balancing.
A good host that's close, but the host should be between the two clients. There always is a best host. Find it.

Smarter miscreant client (straight through TCP). Or one that contributes, even. Very low prio.

Could research to see if this has been done (I think it has) before. Was it good? Successful?
SSH tunnel? So this idea isn't a bad one...
Could do an SSL tunnel...

Could write a client for the outside hosts so they don't use the proxies/dynamic dns [it's really similar to jxta java p2p](then.md). Then STUN would be faster. Low Prio. 3rd party.

TODO: Use OpenDHT for available proxies. This could be nice for proxy selection. Could use OpenDHT for the lookups, too. Hmm. Then they choose their own proxy, register themselves on OpenDHT. I like it already. Then we can use OpenDHT for name resolution, too, perhaps--like arbitrary. This yes :)

research allowing spurts but then slowing down that little stream :)

Research ways to open more ports:
> miscreants tell you which ports they want open (one to one mapping).
> or their (normal) 3114 -> local 80
> or request a port range,
> or 10 different ones on every proxy
> or myname800.us.org -> some proxy that is running it on 800 and can work with ya (yes).

maybe a distinct port (random) for a miscreant if they want to ensure they are good (open a new one on the proxy). Random or requested.

Research into potential problems
> round robin to overcome it?
> distinct alients, miscreants (could be a conflict if it were used from same proxy, with only a single DNS lookup, two NAT'ed aliens within the same "room" that go to two different miscreants.

Login system: use the sweet logins via web (javascript?) or the smarter client they have to install--one or the other (smart clients generally frowned upon).

Maybe an azureus plugin to just use this other name (nice). Low prio. Like way low. 3rd party.

Tight would be using a java applet to somehow lookup the 'real' IP of the host (assuming they are doing an HTTP get), or also setting an extra cookie to transactions or what not, so that we know for sure which host they are. Or if they don't have that cookie requiring them to login or what not.
Maybe requiring logins for everyone to use it (ever) would be nice. Yeah probably :)

Could do HTTP request via an HTTP proxy/tunnel, too, using POST (very low priority don't do). 3rd party


DNS is connect similar. Could definitely be ambiguous. HTTP is connect straight.

Future project: streaming from one source out (oooh).  If that were actually really possible--wow. Wow.

Limit bandwidth among ALL per proxy. Limit bandwidth among connection, or, if strict, limit bandwidth among all within the user's NAT (true IP)--that would actually really limit it--maybe we can use the round robin to get around this.
Round Robin Fair Queue with a cap would be nice.

Super tight would be when one proxy gets overloaded or maybe its quota is almost reached, it would possible...transfer connections to someone else. That would be tight. I've almost never heard of anything like it, except routers.

Could set it up so that it starts a program when a connection occurs, then kills it after (like apache). Hmm. like inetd :) 3rd party.
Also could do: HTTP request at beginning, to fake out filters.
HTTP proxy guy.

Eula: "you need administrator approval"

# DNS #
We need to set a low TTL. Like negligible.
We may be able to use godaddy and just use subdomaings (if godaddy will forward queries on to us). If not then we need to possibly "get a friend" that happens to have their own ns servers and have them forward everything about it on to us. Or some service that will do it for us (should exist).

DNS: if from dns then connect similar, theoretically other queries near would be from same (in theory).  So a new query from the same dns server should go to a new proxy (hopefully still a good proxy) to avoid conflicts--I think.  Re-requests to the same place can/should safely go to the same place (for us for now just re-send it 'next request goes to here').

# Security #
Enforce a EULA.
Tell them to only use a secure program that they trust.
It only opens (as of now) a few ports, so that's nice for security. It's punching a small hole through the firewalls :)

Could do username, password using diffie-hellman or "weak passwords" from the host--nice. Not yet necessary tell them to only use public things that are secure. Could be 'allow connection only once' or what not, to be better security.

Using this system will not really 'hide' you from anyone, because the DNS queries (or web page login) must originate from you in order for it to work, so it is trivially trackable. This does not provide anonymity.

Warn about security! Secure progs only! Or make them explicitly enable certain domains (theirnameXXX.us.org) so that they know what is coming in and going out. Give an EULA. Could also let them choose who to let in (like an IP mask), or require password authentication back to the original host, before allowing it to connect (through one port at least :)

Maybe for security for now...one proxy (only) per miscreant. Sounds like a good plan to me. This would simplify the load balancing.

With balancing maybe could have it 'stop' all tthe connections when it reaches the limit, too, forcing them to a new host. That would make sense. Just use up their daily quota per day, and then just really cap down on the bandwidth allowed.