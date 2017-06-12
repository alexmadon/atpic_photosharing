#!/usr/bin/python3
# import logging
import socket
import zmq
import struct
import time

import atpic.log
import atpic.mybytes

xx=atpic.log.setmod("INFO","zmq_asyncdone_client")


def get_socket():
    yy=atpic.log.setname(xx,'get_socket')
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    # socket.setsockopt(zmq.HWM, 800)
    socket.connect("tcp://192.168.69.1:5057")
    return socket

def send(socket,response):
    yy=atpic.log.setname(xx,'send')
    atpic.log.debug(yy,'input:',response)
    socket.send(response)

if __name__ == "__main__":
    print("before....")
    # logging.basicConfig(level=logging.DEBUG)
    print("starting....")
    socket=get_socket()
    

    # t=test, A=Artefact, U=Update SQL, T=original transform message

    send(socket,b'tA|8|2222|515542|0|jpg|n/2014/05/23/14/20/8_2222_0.jpg') 
    send(socket,b'tU|7|3333|image/x-canon-crw|3072|2048||||2.8||||||||')

    send(socket,b'U|7|3333|image/x-canon-crw|3072|2048||||2.8||||||||')
    send(socket,b'A|8|2222|515542|0|jpg|n/2014/05/23/14/20/8_2222_0.jpg') 

    ts=time.time()
    tsb=atpic.mybytes.float2bytes(ts)
    send(socket,b'T|'+tsb+b'|testing') 

    socket.close()

    # protocol: zmq         zmq         redis       zmq       http
    # serveur:   -> asyncpro -> asyncdone -> indexer -> zmq_es -> ES
    # message:   T         (A,U,T)
