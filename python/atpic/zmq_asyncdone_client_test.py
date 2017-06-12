#!/usr/bin/python3
# import logging
import socket
import zmq
import struct
import time

import atpic.log
import atpic.mybytes
import atpic.zmq_asyncdone_client

xx=atpic.log.setmod("INFO","zmq_asyncdone_client_test")


if __name__ == "__main__":
    print("before....")
    # logging.basicConfig(level=logging.DEBUG)
    print("starting....")
    socket=atpic.zmq_asyncdone_client.get_socket()
    
    # t= test, I=Insert, P=Ping +timestamp
    # ONLY TESTING here
    atpic.zmq_asyncdone_client.send(socket,b'tA|8|2222|515542|0|jpg|n/2014/05/23/14/20/8_2222_0.jpg') 
    atpic.zmq_asyncdone_client.send(socket,b'tU|7|3333|image/x-canon-crw|3072|2048||||2.8||||||||')


    ts=time.time()
    tsb=atpic.mybytes.float2bytes(ts)
    atpic.zmq_asyncdone_client.send(socket,b'T|'+tsb+b'|testing') 

    socket.close()
