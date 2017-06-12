#!/usr/bin/python3
# import logging
# import logging.handlers
import sys
import os
import traceback
import signal
import datetime
import re
# http://docs.python.org/py3k/howto/logging.html#configuring-logging
import atpic.log
import atpic.redis_pie


xx=atpic.log.setmod("INFO","pdns_pipe")

"""
TO TEST:
1) start this script
2) cut and paste queries:

Q	atpic.com	IN	ANY	-1	192.0.43.10
Q	atpic.com	IN	MX	-1	192.0.43.10
Q	atpic.com	IN	AAAA	-1	192.0.43.10
Q	atpic.com	IN	NOEXIST	-1	192.0.43.10
HELO	1
Q	atpic.com	IN	TXT	-1	192.0.43.10
Q	atpic.com	IN	A	-1	192.0.43.10
 
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
    """ 
    Reads the response of the server, byte per byte,
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
    yy=atpic.log.setname(xx,'getbanner')
    atpic.log.info(yy,'input=',query)
    if query==b"HELO\t1":
        response=b"OK\tSample backend firing up"
    else:
        response=b"FAIL"
    atpic.log.info(yy,'output=',response)
    return response

def get_arecord(qname,rediscon):
    yy=atpic.log.setname(xx,'get_arecord')
    atpic.log.info(yy,'input=',qname)
    # returns the IP
    if qname==b'ns01.atpic.com':
        theip=b'5.9.136.58'
    elif qname==b'ns02.atpic.com':
        theip=b'144.76.168.36'
    else:
        theip=b'5.9.136.58'
    atpic.log.info(yy,'output=',theip)
    return theip


def get_nsservers():
    # returns the list of NameServers' IPs
    return [b'ns01.atpic.com',b'ns02.atpic.com']



def dnsquery_a(resp,qname,rediscon):
    theip=get_arecord(qname,rediscon)
    # response=b'DATA	atpic.com	IN	A	3600	-1	1.1.1.1'
    aline=[]
    aline.append(b'DATA')
    aline.append(qname)
    aline.append(b'IN')
    aline.append(b'A')
    aline.append(b'3600')
    aline.append(b'-1')
    aline.append(theip)
    resp.append(b'\t'.join(aline))
    return resp

def dnsquery_aaaa(resp,qname,rediscon):
    theip=get_arecord(qname,rediscon) # NOT USEDDDDDDD
    # response=b'DATA	atpic.com	IN	A	3600	-1	1.1.1.1'
    aline=[]
    aline.append(b'DATA')
    aline.append(qname)
    aline.append(b'IN')
    aline.append(b'AAAA')
    aline.append(b'3600')
    aline.append(b'-1')
    aline.append(b'2a01:4f8:190:1022::2')
    resp.append(b'\t'.join(aline))
    return resp


def dnsquery_txt(resp,qname):
    # response=b'DATA	atpic.com	IN	A	3600	-1	1.1.1.1'
    aline=[]
    aline.append(b'DATA')
    aline.append(qname)
    aline.append(b'IN')
    aline.append(b'TXT')
    aline.append(b'3600')
    aline.append(b'-1')
    aline.append(b'v=spf1 a -all')
    resp.append(b'\t'.join(aline))
    return resp


def dnsquery_mx(resp,qname):
    # theip=get_arecord(qname,rediscon)
    # response=b'DATA	atpic.com	IN	A	3600	-1	1.1.1.1'
    aline=[]
    aline.append(b'DATA')
    aline.append(qname)
    aline.append(b'IN')
    aline.append(b'MX')
    aline.append(b'3600')
    aline.append(b'-1')
    aline.append(b'10')
    aline.append(b'smtp.atpic.com') # 1st smtp server
    resp.append(b'\t'.join(aline))
    return resp

def dnsquery_ns(resp,qname):
    nsservers=get_nsservers()
    for nsserver in nsservers:
        aline=[]
        aline.append(b'DATA')
        aline.append(qname) # b'atpic.com')
        aline.append(b'IN')
        aline.append(b'NS')
        aline.append(b'3600')
        aline.append(b'-1')
        aline.append(nsserver)
        resp.append(b'\t'.join(aline))
    return resp

def dnsquery_soa(resp,qname):
    # response=b'DATA\tatpic.com\tIN\tSOA\t3600\tns8.atpic.com\tcontact.atpic.com\t2010122804\t28800\t7200\t604800\t86400'
    
    # SOA is stored:
    # primary hostmaster serial refresh retry expire default_ttl
    # response=b'DATA\tatpic.com\tdns@atpic.com\t'+serial+b'\t'+refresh+b'\t'
    serial=b'-1'
    aline=[]
    aline.append(b'DATA')
    aline.append(qname) # aline.append(b'atpic.com')
    aline.append(b'IN')
    aline.append(b'SOA')
    aline.append(b'3600')
    aline.append(serial)
    aline.append(b'ns01.atpic.com') # nameserver
    aline.append(b'atpicversion2.gmail.com') # hostmaster
    # aline.append(b'2010122804') # serial
    # the most popular convention being yyyymmddss 
    # where yyyy = year, mm = month and dd = day ss = a sequence number in case you update it more than once in the day! 
    seq=0
    ss="%02i" % seq
    datetimefirst=datetime.datetime.now()
    serial=datetimefirst.strftime("%Y%m%d")
    aline.append((serial+ss).encode('utf8'))
    aline.append(b'28800') # refresh
    aline.append(b'7200') # retry
    aline.append(b'604800') # expire
    aline.append(b'86400') # default_ttl
    resp.append(b'\t'.join(aline))
    return resp

def dnsquery(query,rediscon):
    yy=atpic.log.setname(xx,'dnsquery')
    atpic.log.info(yy,'input=',query,rediscon)
    splitted=query.split(b'\t')
    if query.startswith(b'HELO'):
        atpic.log.info(yy,'got HELO, sending banner')
        response=b"OK\tSample backend firing up"
        return response
    if len(splitted)<6:
        atpic.log.info(yy,'splitted len < 6!!!!!!')
        return b'END'
    (atype,qname,qclass,qtype,aid,ip)=splitted
    atpic.log.info(yy,'(atype,qname,qclass,qtype,aid,ip)',(atype,qname,qclass,qtype,aid,ip))
    # queries sent by pdns to the pipe are 6 elements separated by a tab \t
    "Q	atpic.com	IN	A	123	10.10.10.10"
    "Q	www.ds9a.nl	IN	CNAME	-1	213.244.168.210"

    resp=[]
    qname=qname.lower()
    if not(qname.endswith(b'atpic.com')) and not(qname.endswith(b'atpicdata.com')) :
        atpic.log.info(yy,'ENDED1 on:','atype=',atype,'qname=',qname,'qclass=',qclass,'qtype=',qtype,'aid=',aid,'ip=',ip)
        pass # will end
    elif qtype==b'ANY' and qname in [b'atpic.com',b'atpicdata.com']:
        # see notes about ANY query in 
        # /home/madon/doc/pdns/backends-detail.html
        # needs to get SOA, CNAME and NS records in one go
        resp=dnsquery_ns(resp,qname)
        resp=dnsquery_soa(resp,qname)
        resp=dnsquery_mx(resp,qname)
        resp=dnsquery_txt(resp,qname)
        resp=dnsquery_a(resp,qname,rediscon)
        resp=dnsquery_aaaa(resp,qname,rediscon)
    elif qtype==b'ANY' and qname in [b'www.atpic.com',b'www.atpicdata.com']:
        resp=dnsquery_a(resp,qname,rediscon)
    elif qtype==b'ANY':
         resp=dnsquery_a(resp,qname,rediscon)
    elif qtype==b'NS' and qname in [b'atpic.com',b'atpicdata.com']:
        resp=dnsquery_ns(resp,qname)
    elif qtype==b'MX' and qname in [b'atpic.com',]:
        resp=dnsquery_mx(resp,qname)
    elif qtype==b'SOA':
        resp=dnsquery_soa(resp,qname)
    elif qtype==b'A':
        resp=dnsquery_a(resp,qname,rediscon)
    elif qtype==b'TXT':
        resp=dnsquery_txt(resp,qname)
    elif qtype==b'AAAA':
        resp=dnsquery_aaaa(resp,qname,rediscon)
    else:
        atpic.log.info(yy,'ENDED2 on:','atype=',atype,'qname=',qname,'qclass=',qclass,'qtype=',qtype,'aid=',aid,'ip=',ip)
        # resp.append(b'FAIL')
        return b'END'
    response=b'\n'.join(resp)

    if response!=b'FAIL':
        response=response+b'\nEND'
    atpic.log.info(yy,'output=',response)
    return response



if __name__ == "__main__":

    yy=atpic.log.setname(xx,'main')

    infile = sys.stdin
    outfile = sys.stdout
    rediscon=atpic.redis_pie.connect_first()


    # first get the banner
    # query=getLine(infile.buffer)
    # response=getbanner(query)
    # outfile.buffer.write(response+b'\n')
    # outfile.buffer.flush()

    while True:
        # inline=infile.readline()
        # outfile.write(inline)
        query=getLine(infile.buffer)
        atpic.log.info(yy,'query',query)
        if query==b'':
            atpic.log.info(yy,'got empty bytes, QUITTING!')
            quit()
        try:
            response=dnsquery(query,rediscon)
            atpic.log.info(yy,'response',response)
        except:
            reponse=b'FAIL'
            atpic.log.error(yy,traceback.format_exc())

        outfile.buffer.write(response+b'\n')
        outfile.buffer.flush()
