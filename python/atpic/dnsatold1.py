"""
python-adns - Python bindings to the asynchronous DNS resolver library
python-dns - pydns - DNS client module for Python
python-musicdns - Python bindings for the MusicIP service
python-musicdns-dbg - debug symbols for the MusicIP Python bindings
python-twisted-names - A DNS protocol implementation with client and server
python-dnspython - DNS toolkit for Python

python-dnspython 
http://www.gnu-darwin.org/www001/src/ports/dns/py-dnspython/work/dnspython-1.5.0/tests/message.py
http://www.dnspython.org/kits/1.7.1/
http://www.dnspython.org/docs/1.7.1/html/dns.message-module.html
http://www.sfr-fresh.com/unix/www/webcleaner-2.41.tar.gz:a/webcleaner-2.41/wc/dns/tests/test_zone.py
http://www.dnspython.org/docs/1.7.1/html/dns.message.Message-class.html


dns.message.from_text
dns.message.from_wire

1) start the server
python dnsat.py

2) make queries
dig -p 5353 madon.net @localhost


"""



import dns.message
import dns.rdataset
import dns.rdata
import dns.rdatatype
import dns.rrset
import dns.opcode
import dns.flags
import socket, traceback
host = '127.0.0.1' 
# host = "0.0.0.0" # if we want to bind on all possible IP addresses
port = 5353
print "binding %s %s" % (host,port)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

while 1:
    try:
        message, address = s.recvfrom(8192)
        print "Got data from", address
        print "message was: %s" % message
        # Acknowledge it.
        # s.sendto("I am here", address)
        # decode the query
        message=dns.message.from_wire(message)
        print type(message)
        print "---query----"
        print message
        print "------------"
        # section eg: message.question or message.answer
        # section=message.question
        # name="A"
        # rdclass= 1 # IN the internet

        # rdtype= 1 # A 1 a host address
        # rrs = message.find_rrset(section, name, rdclass, rdtype)
        # rrs = message.get_rrset(section, name, rdclass, rdtype)
        print "id %s" % message.id
        print "rcode %s" % message.rcode()
        print " rcode %s" % dns.rcode.to_text(message.rcode())
        # print dir(message.rcode)
        print "opcode %s" % message.opcode()
        print " opcode %s" % dns.opcode.to_text(message.opcode())
        print "flags %s" % message.flags
        print " flags %s" % dns.flags.to_text(message.flags)
        print "index %s" % message.index
        for rrset in message.question: # list of dns.rrset.RRset objects
            print "----> rrset: %s" % rrset
            print " covers %i" % rrset.covers
            print " rdclass %i" % rrset.rdclass
            print " rdtype %i" % rrset.rdtype
            print " ttl %i" % rrset.ttl
            print " name  %s" % rrset.name

            # print dir(rrset)
            # for item in rrset.items():
            #     print item
        # print rrs
        # rds = message.get_rdataset('madon.net.', 'A')
        # print rds
        # answer=""
        # dns.rdataset.from_text('IN', 'SOA', 300, 'foo bar 1 2 3 4 5')
        # dns.rrset.from_text('@', 300, 'IN', 'SOA', 'foo bar 1 2 3 4 5')
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.format_exc()
