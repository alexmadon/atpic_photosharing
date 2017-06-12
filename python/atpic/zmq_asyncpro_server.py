#!/usr/bin/python3
"""
Once an image is uploaded, we send to this server the image id, 
to generate artefacts.
Expects:
UID|PID
then queries the rest from SQL
To unit test, define functions without DB
"""
import subprocess
import os
import socket
import sys
import zmq
import time
import signal
import traceback


import atpic.log
import atpic.asyncpro
import atpic.zmq_asyncdone_client

"""
This is a single threaded tcp server.
As exiftool requires a single thread of input we should not multithread this one.
Rather use a zmq queue to serialize requests.

Needs to be run as 'www-user' as we need to write to the filesystem.

There is a dispatcher:
extract mimetype,width,height with exiftool
if video-> extract frames
elif image/raw->convert to jpg with dcraw
elif image -> if width,height ->thumbnail with convert

"""

xx=atpic.log.setmod("INFO","zmq_asyncpro_server")


# NO SQL for security reasons
# just filesystem
# sql updates are sent back to listener on host




def do_processing(socketres,receivedData):
    # PROTOCOL:
    # input message is T|UID|PID|path (T=Transform, UID: user id, PID: Pic ID
    yy=atpic.log.setname(xx,'do_processing')
    atpic.log.debug(yy,'input=',receivedData)

    time1=time.time()
    atpic.asyncpro.process(receivedData,socketres)
    time2=time.time()
    ittook=time2-time1
    atpic.log.debug(yy,"It took (seconds):",ittook)
    


def main_loop():
    yy=atpic.log.setname(xx,'main_loop')
    # run as user www-data
    os.setuid(33)


    atpic.log.info(yy,"STARTING zmq_asyncpro....")
    
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://192.168.69.3:5056") # runs in VM

    socketres=atpic.zmq_asyncdone_client.get_socket()

    while True:
        try:
            # receive the message
            msg = socket.recv()
            receivedData=msg
            atpic.log.info(yy,"receivedData",receivedData)
            do_processing(socketres,receivedData)
        except KeyboardInterrupt:
            raise
        except:
            atpic.log.error(yy,traceback.format_exc())
            atpic.log.error(yy,'LOST MESSAGE',(receivedData))
            atpic.zmq_asyncdone_client.send(socketres,b'LOST'+receivedData)
            # raise
            # KeyboardInterrupt

if __name__ == "__main__":
    yy=atpic.log.setname(xx,'main')
    main_loop()
