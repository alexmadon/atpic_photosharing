#!/usr/bin/python3
# import logging
# import logging.handlers
import sys
import os
import traceback
import signal

# http://docs.python.org/py3k/howto/logging.html#configuring-logging
import atpic.log
import atpic.redis_pie
xx=atpic.log.setmod("INFO","pdns_pipe.old2")

# Note that if your server is not listening on UDP port 514, 
# SysLogHandler may appear not to work.
# /etc/rsyslog.conf to allow UDP
# http://scottbarnham.com/blog/2008/01/01/sysloghandler-not-writing-to-syslog-with-python-logging/





# will log to /var/log/{user.log,syslog,debug}
# create syslog handler and set level to debug

ch = logging.handlers.SysLogHandler() # or SysLogHandler(address='/dev/log')
# ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(process)d-%(name)s: %(levelname)s %(message)s')
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# logger = logger.getChild(__name__+'%s' % pid)


"""

/etc/init.d/pdns monitor
tail -f /tmp/example.log

dig @localhost -p 53 a atpic.com
dnsperf -s 127.0.0.1 -p 53 -d testdata




Python 3.1 added io.TextIOBase.detach(), with a note in the documentation for sys.stdout:

    The standard streams are in text mode by default. To write or read binary data to these, use the underlying binary buffer. For example, to write bytes to stdout, use sys.stdout.buffer.write(b'abc'). Using io.TextIOBase.detach() streams can be made binary by default. This function sets stdin and stdout to binary:

    def make_streams_binary():
        sys.stdin = sys.stdin.detach()
        sys.stdout = sys.stdout.detach()



"""



def getLine(afile):
    """ Reads the response of the server, byte per byte,
        and returns a line of the server response
        The line returned is in byte format, not in 
        any encoded form.

        In the end, the socket points to the start of the next line

        @param line: Socket communicating with the redis server
        @return: A line of bytes
    """
    yy=atpic.log.setname(xx,'getLine')
    line = b""
    while True:
        next_byte = afile.read(1)  # read a byte
        atpic.log.debug(yy,'read next_byte',next_byte)
        if next_byte==b'':
            atpic.log.debug(yy,'got empty bytes, needs to QUIT!')
            # quit()
            return b''
        # print('next_byte',next_byte)
        if next_byte == b"\n":    # if it's end of line, break
            # print('got newline, breaking')
            break
        else:           
            line += next_byte         # otherwise, stick it with the rest
    return line

def getbanner(query):
    if query==b"HELO\t1":
        response=b"OK\tSample backend firing up"
    else:
        response=b"FAIL"
    return response


def dnsquery(query,rediscon):
    splitted=query.split(b'\t')
    if len(splitted)<6:
        atpic.log.debug(yy,'splitted len < 6!!!!!!')
        return b'END'
    (atype,qname,qclass,qtype,aid,ip)=splitted
    "Q	atpic.com	IN	A	123	10.10.10.10"
    "Q	www.ds9a.nl	IN	CNAME	-1	213.244.168.210"
    resp=[]
    if qtype==b'A' or qtype==b'ANY':
        response=b'DATA	atpic.com	IN	A	3600	-1	1.1.1.1'
        resp.append(b'DATA')
        resp.append(b'atpic.com')
        resp.append(b'IN')
        resp.append(b'A')
        resp.append(b'3600')
        resp.append(b'-1')
        resp.append(b'1.1.1.1')
    elif qtype==b'SOA':
        # response=b'DATA\tatpic.com\tIN\tSOA\t3600\tns8.atpic.com\tcontact.atpic.com\t2010122804\t28800\t7200\t604800\t86400'

        # SOA is stored:
        # primary hostmaster serial refresh retry expire default_ttl
        # response=b'DATA\tatpic.com\tdns@atpic.com\t'+serial+b'\t'+refresh+b'\t'
        serial=b'-1'
        resp.append(b'DATA')
        resp.append(b'atpic.com')
        resp.append(b'IN')
        resp.append(b'SOA')
        resp.append(b'3600')
        resp.append(serial)
        resp.append(b'ns8.atpic.com') # nameserver
        resp.append(b'contact.atpic.com')
        resp.append(b'2010122804')
        resp.append(b'28800')
        resp.append(b'7200')
        resp.append(b'604800')
        resp.append(b'86400')
    else:
        atpic.log.debug(yy,'FAILED on:','atype=',atype,'qname=',qname,'qclass=',qclass,'qtype=',qtype,'aid=',aid,'ip=',ip)
        resp.append(b'FAIL')

    response=b'\t'.join(resp)

    if response!=b'FAIL':
        response=response+b'\nEND'
    return response



if __name__ == "__main__":

    logger2=logger
    atpic.log.debug(yy,'hi')
    infile = sys.stdin
    outfile = sys.stdout
    rediscon=atpic.redis_pie.Redis()


    # first get the banner
    query=getLine(infile.buffer)
    response=getbanner(query)
    outfile.buffer.write(response+b'\n')
    outfile.buffer.flush()

    while True:
        # inline=infile.readline()
        # outfile.write(inline)
        query=getLine(infile.buffer)
        atpic.log.debug(yy,'query',query)
        if query==b'':
            atpic.log.debug(yy,'got empty bytes, QUITTING!')
            quit()
        try:
            response=dnsquery(query,rediscon)
            atpic.log.debug(yy,'response',response)
        except:
            reponse=b'FAIL'
            atpic.log.error(yy,traceback.format_exc())

        outfile.buffer.write(response+b'\n')
        outfile.buffer.flush()
