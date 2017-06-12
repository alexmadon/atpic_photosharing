#!/usr/bin/python3

import zmq

import atpic.log

xx=atpic.log.setmod("INFO","zmq_elastic_client")



def connect_first():
    yy=atpic.log.setname(xx,'connect_first')
    context = zmq.Context()    
    # Socket to talk to server
    atpic.log.debug(yy,"Connecting to ZMQ elastic server...")
    socket = context.socket(zmq.REQ)
    socket.connect ("tcp://localhost:5557")
    return socket

def http_general(essock,method,uri,ajson):
    yy=atpic.log.setname(xx,'http_general')
    atpic.log.debug(yy,'input=',(essock,method,uri,ajson))
    # request=b'GET|'+uri+b'|'+ajson
    request=method+b'|'+uri+b'|'+ajson
    essock.send(request)
    message = essock.recv()
    atpic.log.debug(yy,'output=',message)
    return message

if __name__ == "__main__":
    socket=connect_first()
    # Do 10 requests, waiting each time for a response
    requests=[
        b'GET|/atpic/pic/1?pretty=1|',
        b'GET|/atpic/pic/2?pretty=1|',
        b'GET|/atpic/_status|',
        b'GET|/atpic/pic/_search?pretty=1|{"query" : {"term" : {"uid": "1"}}}',
        ]
    for request in requests:
        print (">>", request)
        socket.send (request)
        # Get the reply.
        message = socket.recv()
        print ("<<", message)


    print('Now using http_general()')
    mess=http_general(socket,b'GET',b'/atpic/pic/_search?pretty=1',b'{"query" : {"term" : {"uid": "1"}}}')
    print(mess)
