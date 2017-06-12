"""
python2.6  dnsthreads.py

dig -p 5053 atpic.com @localhost

for i in `seq 1 10000`; do echo "atpic.com A" >> testdata; done

dnsperf -s 127.0.0.1 -p 5053 -d testdata
  Queries per second:   609.351585 qps

"""
import socket
import threading
import SocketServer

import dns.message
import dns.rdataset
import dns.rdata
import dns.rdatatype
import dns.rrset
import dns.opcode
import dns.flags
import traceback
import signal
import os
# import asyncore

def handler(signum, frame):
    print "Signal handler called with signal", signum
    print "I should reinsert the config IP"


def myprint(mes):
    # print mes
    pass

def decode_request(message):
    
    # decode the query
    message=dns.message.from_wire(message)
    """
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
        """
    return message

def make_response(message):
    response=dns.message.make_response(message) # create a new message object from the message received
    
    response.answer.append(dns.rrset.from_text("atpic.com.",99,dns.rdataclass.IN,"A","88.198.21.167"))  # see google andns.py
    myprint("========")
    myprint(response.to_text())
    myprint("========")
    return response


class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):

    # def handle(self):
    #     data = self.request.recv(1024)
    #     cur_thread = threading.currentThread()
    #     response = "%s: %s" % (cur_thread.getName(), data)
    #     self.request.send(response)
    def handle(self):
        message=self.request[0]
        socket=self.request[1]
        address=self.client_address

        cur_thread = threading.currentThread()
        myprint("This is thread %s" % cur_thread.getName())
        myprint(threading.enumerate())

        message=decode_request(message)
        response=make_response(message)
        socket.sendto(response.to_wire(), address)

        # print "%s wrote:" % self.client_address[0]
        # response = "%s: %s" % (cur_thread.getName(), data)
        # socket.sendto(response, self.client_address)

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass




if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 5053

    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    ip, port = server.server_address
    print ip
    print port
    server.serve_forever()
