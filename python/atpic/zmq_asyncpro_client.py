#!/usr/bin/python3
# import logging
import atpic.log
import socket
import zmq
import struct

# pushes a job to the virtual machine
# the server runs in a VM

xx=atpic.log.setmod("INFO","zmq_asyncpro_client")




def send(filename):
    yy=atpic.log.setname(xx,'send')
    atpic.log.debug(yy,'input:',filename)
    atpic.log.info('SENDING',filename)
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    # socket.setsockopt(zmq.HWM, 800)
    socket.connect("tcp://192.168.69.3:5056")
    socket.send(filename)
    socket.close()

if __name__ == "__main__":
    print("before....")
    # logging.basicConfig(level=logging.DEBUG)
    print("starting....")
    for i in range(0,1):
        print(i)
        # Log|timsetamp|....
        send(b'L|123456|1|9999|var/www/jpg|tropic.jpg')
