#!/usr/bin/python3

"""
a light wrapper around redis
"""
import socket
import zmq
import time

import atpic.log
import atpic.mybytes

xx=atpic.log.setmod("INFO","zmq_asyncdone_client")


def get_socket():
    yy=atpic.log.setname(xx,'get_socket')
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    # socket.setsockopt(zmq.HWM, 800)
    socket.connect("tcp://127.0.0.1:5059")
    return socket

def send(socket,response):
    yy=atpic.log.setname(xx,'send')
    atpic.log.debug(yy,'input:',response)
    socket.send(response)

if __name__ == "__main__":
    print("starting....")
    socket=get_socket()
    send(socket,b'1||1') 
    socket.close()

    # protocol: zmq         zmq         redis       zmq       http
    # serveur:   -> asyncpro -> asyncdone -> indexer -> zmq_es -> ES
    # message:   T         (A,U,T)
