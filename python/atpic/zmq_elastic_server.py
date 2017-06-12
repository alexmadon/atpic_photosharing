#!/usr/bin/python3
# opens long lived connection to REST elastic search
# in one thread only
# just handles failures
# and reconnect when service is back up.

import socket
import traceback
import time
import errno
import zmq

import atpic.log
import atpic.redis_pie_comm
import atpic.errors
import atpic.mybytes

xx=atpic.log.setmod("INFO","zmq_elastic_server")

def parse_message(request):
    yy=atpic.log.setname(xx,'parse_message')
    atpic.log.debug(yy,'input=',request)
    splitted=request.split(b'|')
    http_verb=splitted[0]
    http_uri=splitted[1]
    jsondata=b'|'.join(splitted[2:])

    atpic.log.debug(yy,'output=',(http_verb,http_uri,jsondata))
    return (http_verb,http_uri,jsondata)

def main_loop():
    yy=atpic.log.setname(xx,'main_loop')
    http_verb=b'GET'
    http_uri=b'/atpic/pic/1?pretty=1'

    # socket to elasticsearch
    essock=None

    # socket to zmq
    context = zmq.Context()
    zmqsocket = context.socket(zmq.REP)
    atpic.log.info(yy,'starting zmq elasticsearch wrapper')
    zmqsocket.bind("tcp://127.0.0.1:5557")

    while True:
        try:
            # Wait for next request from client
            atpic.log.debug(yy,"waiting to get a message on ZMQ socket")
            request = zmqsocket.recv()
            atpic.log.debug(yy,"Received request: ", request)
 
            if not essock:
                essock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                essock.connect(('127.0.0.1', 9200))
            # curl -XGET 'http://localhost:9200/atpic/pic/1?pretty=1'
            (http_verb,http_uri,jsondata)=parse_message(request)
            clenint=len(jsondata)
            clen=atpic.mybytes.int2bytes(clenint)
            atpic.log.debug(yy,"request content len",clen)

            essock.sendall(http_verb+b' '+http_uri+b' HTTP/1.1\r\n')
            essock.sendall(b'Host: localhost\r\n')
            essock.sendall(b'Content-type: application/json; charset=utf-8\r\n')
            essock.sendall(b'Content-Length: '+clen+b'\r\n')
            essock.sendall(b'\r\n')
            essock.sendall(jsondata)
            atpic.log.debug(yy,"all data sent")

            # receive data
            head=[]
            while True:    
                line=atpic.redis_pie_comm.getLine(essock)
                atpic.log.debug(yy,'line',line)
                head.append(line)
                if line==b'':
                    break
            clength_int=0
            for aline in head:
                if aline.startswith(b'Content-Length: '):
                    clength=aline.strip(b'Content-Length: ')
                    clength_int=atpic.mybytes.bytes2int(clength)
            if clength_int>0:
                payload = essock.recv(clength_int)
            # detect a 503 error:
            firstline=head[0]
            atpic.log.debug(yy,"(head,payload)",(head,payload))
            if firstline.startswith(b'HTTP/1.1 5'):
                raise atpic.errors.Error5XX(b'5XX error in elasticsearch',firstline)
            # Send reply back to client
            zmqsocket.send(payload)
           # time.sleep(1)
        except socket.error as e:
            atpic.log.error(yy,'this is a socket.error')
            atpic.log.error(yy,traceback.format_exc())
            if e.errno == errno.EPIPE:
                atpic.log.error(yy,'errno.EPIPE broken pipe')
                # sock.shutdown(socket.SHUT_RDWR)
                essock.close()
                del essock
                essock=None
            elif e.errno == errno.ECONNREFUSED:
                atpic.log.error(yy,'errno.ECONNREFUSED')
                essock.close()
                del essock
                essock=None
                # time.sleep(2)
            else:
                atpic.log.error(yy,'GENERIC socket error')
                essock.close()
                del essock
                essock=None
                # time.sleep(1)
            # Send reply back to client
            zmqsocket.send(b'{"zmq_error":"socket.error"}')
        except atpic.errors.Error5XX as e:
            # need to clear elasticsearch cache???
            # curl -XPOST 'http://localhost:9200/atpic/_cache/clear'
            atpic.log.error(yy,traceback.format_exc())
            essock.close()
            del essock
            essock=None
            zmqsocket.send(b'{"zmq_error":"5xx.error"}')
        except:
            atpic.log.error(yy,traceback.format_exc())
            # time.sleep(1)
            zmqsocket.send(b'{"zmq_error":"unknown.error"}')

            pass


if __name__ == "__main__":
    print('starting')#
    main_loop()
    pass
