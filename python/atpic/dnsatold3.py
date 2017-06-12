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

def decode_request(message):
    
    # decode the query
    message=dns.message.from_wire(message)
    myprint(type(message))
    myprint("---query----")
    myprint(message)
    myprint("------------")
    # section eg: message.question or message.answer
    # section=message.question
    # name="A"
    # rdclass= 1 # IN the internet
    
    # rdtype= 1 # A 1 a host address
    # rrs = message.find_rrset(section, name, rdclass, rdtype)
    # rrs = message.get_rrset(section, name, rdclass, rdtype)
    myprint("id %s" % message.id)
    myprint("rcode %s" % message.rcode())
    myprint(" rcode %s" % dns.rcode.to_text(message.rcode()))
    # print dir(message.rcode)
    myprint("opcode %s" % message.opcode())
    myprint(" opcode %s" % dns.opcode.to_text(message.opcode()))
    myprint("flags %s" % message.flags)
    myprint(" flags %s" % dns.flags.to_text(message.flags))
    myprint("index %s" % message.index)
    for rrset in message.question: # list of dns.rrset.RRset objects
        myprint("----> rrset: %s" % rrset)
        myprint(" covers %i" % rrset.covers)
        myprint(" rdclass %i" % rrset.rdclass)
        myprint(" rdtype %i" % rrset.rdtype)
        myprint(" ttl %i" % rrset.ttl)
        myprint(" name  %s" % rrset.name)
    return message

def make_response(message):
    response=dns.message.make_response(message) # create a new message object from the message received
    
    response.answer.append(dns.rrset.from_text("atpic.com.",99,dns.rdataclass.IN,"A","88.198.21.167"))  # see google andns.py
    myprint("========")
    myprint(response.to_text())
    myprint("========")
    return response


# see DatagramServerChannel
# at http://acs.lbl.gov/~dang/tmp/NetLogger/source/socketserver.html
class AsyncDNS(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        # self.r = resolver.Resolver()
        # self.query = ''
 
        # self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)

        # self.connect((self.r.nameservers[0], self.r.port))


        signal.signal(signal.SIGHUP, handler)
        pid=os.getpid()
        print "PID=%s" % pid
        print "to kill me, use: kill -HUP %s" % pid
        host = '127.0.0.1' 
        # host = "0.0.0.0" # if we want to bind on all possible IP addresses
        port = 5353
        print "binding %s %s" % (host,port)
        
        # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	self.create_socket (socket.AF_INET, socket.SOCK_DGRAM)
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.set_reuse_addr()
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # s.bind((host, port))
        self.bind((host, port))

    def handle_read(self):
        try:
            message, address = self.socket.recvfrom(8192)
            # print "I received %s" % data
            myprint("Got data from %s,%i" % (address[0],address[1]))
            myprint("message was: %s" % message)
            message=decode_request(message)
            response=make_response(message)
            self.socket.sendto(response.to_wire(), address)

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


"""
while 1:
    try:
        message, address = s.recvfrom(8192)
        # print type(address[0])
        # print type(address[1])
        # Acknowledge it.
        # s.sendto("I am here", address)

        # forge an answer
        answer=[]
        answer.append("id %s" % message.id)
        answer.append("opcode %s" % dns.opcode.to_text(message.opcode()))
        answer.append("rcode %s" % dns.rcode.to_text(message.rcode()))
        answer.append("flags %s" % dns.flags.to_text(message.flags))
        answer.append(";QUESTION")
        answer.append("%s" % message.question[0])
        answer.append(";ANSWER")
        answer.append("atpic.com. 20 IN A 88.198.21.167")
        answer.append(";AUTHORITY")
        answer.append(";ADDITIONAL")
        theanswer="\n".join(answer)
        myprint("+++++++++")
        myprint(theanswer)
        myprint("+++++++++")
        answermessage=dns.message.from_text(theanswer)

        # other method to forge an answer:

        # s.sendto(answermessage.to_wire(), address)



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
"""
