#!/usr/bin/python3
# import logging
import atpic.log
import socket
import zmq
import struct

xx=atpic.log.setmod("INFO","exiftool3k_zmq_client")




def send(filename):
    yy=atpic.log.setname(xx,'send')
    atpic.log.debug(yy,'input:',filename)
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.setsockopt(zmq.HWM, 8)
    socket.connect("tcp://127.0.0.1:5000")
    socket.send(filename)
    socket.close()

if __name__ == "__main__":
    print("before....")
    # logging.basicConfig(level=logging.DEBUG)
    print("starting....")
    for i in range(0,10):
        print(i)
        send(b'/home/madon/public_html/perso/entreprise/sql_current/site/atpic/python/tests/fixture/raw/RAW_NIKON_D70.NEF')
