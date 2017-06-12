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
http://www.dnspython.org/docs/1.7.1/html/dns.message-module.html

dns.message.from_text
dns.message.from_wire

1) start the server
python dnsat.py

2) make queries
dig -p 5353 atpic.com @localhost

3) load test:

for i in `seq 1 10000`; do echo "atpic.com A" >> testdata; done

dnsperf -s 127.0.0.1 -p 5353 -d testdata

  Queries per second:   355.959939 qps

with asyncore

  Queries per second:   743.682473 qps

"""


import scapy.all
import dns.message
import dns.rdataset
import dns.rdata
import dns.rdatatype
import dns.rrset
import dns.opcode
import dns.flags
import socket, traceback
import signal, os
import asyncore

def handler(signum, frame):
    print "Signal handler called with signal", signum
    print "I should reinsert the config IP"


def myprint(mes):
    # print mes
    pass

def mkdnsresponse(dr, malhost):

    # http://www.hackaholic.org/papers/blackmagic.txt
    d = scapy.all.DNS()
    # print "id %s" % dr.id
    # print "qd %s" % dr.qd
    d.id = dr.id
    d.qd = dr.qd
    d.qdcount = 1
    d.qr = 1
    d.opcode = 16
    d.an = scapy.all.DNSRR(rrname=dr.qd.qname, ttl=10, rdata=malhost)
    return d



def decode_request(message):
    
    # decode the query
    message=dns.message.from_wire(message)
    return message

def make_response(message):
    response=dns.message.make_response(message) # create a new message object from the message received
    
    response.answer.append(dns.rrset.from_text("atpic.com.",99,dns.rdataclass.IN,"A","88.198.21.167"))  # see google andns.py
    # myprint("========")
    # myprint(response.to_text())
    # myprint("========")
    return response


# see DatagramServerChannel
# at http://acs.lbl.gov/~dang/tmp/NetLogger/source/socketserver.html
class AsyncDNS(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        signal.signal(signal.SIGHUP, handler)
        pid=os.getpid()
        print "PID=%s" % pid
        print "to kill me, use: kill -HUP %s" % pid
        host = '127.0.0.1' 
        # host = "0.0.0.0" # if we want to bind on all possible IP addresses
        port = 5353
        print "binding %s %s" % (host,port)
	self.create_socket (socket.AF_INET, socket.SOCK_DGRAM)
        self.set_reuse_addr()
        self.bind((host, port))

    def handle_read(self):
        try:
            message, address = self.socket.recvfrom(8192)
            # message=decode_request(message)
            # response=make_response(message)
            message=scapy.all.DNS(message)
            res=mkdnsresponse(message,"10.10.10.29")
            # res.display()
            self.socket.sendto(str(res), address)
        
        except socket.timeout:
            pass
        except (KeyboardInterrupt, SystemExit):
            raise
        except socket.error, x:
            errno= x.args[0]
            msg = x.args[1]
            if errno==4:
                print "I received a  (4, 'Interrupted system call'), continuing"
            else:
                traceback.format_exc()

        except:
            traceback.format_exc()

    def writable(self):
        """False for UDP"""
        return False

    def handle_accept(self):
        """pass for UDP"""
        pass

    def handle_connect(self):
        """pass for UDP"""
        pass
    
    def handle_close(self):
        """pass for UDP"""
        pass


if __name__ == "__main__":
    d = AsyncDNS()

    asyncore.loop()

