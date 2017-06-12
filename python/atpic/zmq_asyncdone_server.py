#!/usr/bin/python3
"""
This is a callback run on the host.
It listens to messages sent by the guest.
It does the SQL insert into artefact table

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
import atpic.forgesql
import atpic.libpqalex
import atpic.mybytes
import atpic.connection_young
import atpic.needindex
import atpic.redis_pie

import atpic.zmq_index_client

"""
This is a single threaded tcp server.
"""

xx=atpic.log.setmod("INFO","zmq_asyncdone_server")

def do_index(message,idxsocket):
    # check if that message needs to trigger indexing
    yy=atpic.log.setname(xx,'do_index')
    atpic.log.debug(yy,'input=',message)
    atpic.needindex.index_asyncdone(message,idxsocket)




def do_processing(receivedData,db,dbcounter):
    # input message is
    # T|message (Timing: to measure delays)
    # L|message (Lost mesage)
    # A: create Artefact SQL (_pic_artefact)
    # U: Update SQL (_pic)
    # can also be prepended with 't': testing
    yy=atpic.log.setname(xx,'do_processing')
    atpic.log.debug(yy,'input=',receivedData)

    time1=time.time()

    # T: timing, L: Lost
    if receivedData.startswith(b'T'): # original transform message used to meaure delays in the queue
        splitted=receivedData.split(b'|')
        timestamp1=atpic.mybytes.bytes2float(splitted[1])
        timestamp2=time.time() # unix epoch
        delay=timestamp2-timestamp1
        atpic.log.info(yy,"delay",delay,"for message",receivedData)
        if delay> 30:
            atpic.log.warn(yy,"delay",delay,"!!! for message",receivedData)
    elif receivedData.startswith(b'L'): # Lost message due to exception in VM
            atpic.log.error(yy,"LOSTinVM:",receivedData)
    else:

        # A: Artefact (insert a new artefact), 
        # U: update (update a _pic row)
        # two modes: A, U, tA, tU
        # testing mode if starts with 't'
        # (no insert is done but debug)


        if receivedData.startswith(b't'):
            testmode=True
            message=receivedData[1:]
        else:
            testmode=False
            message=receivedData

        (query,query_args)=atpic.forgesql.asyncpro(message)
        if testmode:
            atpic.log.info(yy,"TESTING MODE")
            atpic.log.info(yy,"Would do:",(query,query_args))
        else:
            # start db connection (or could open and connect)
            (db,dbcounter)=atpic.connection_young.get_db(db,dbcounter)
            result=atpic.libpqalex.pq_exec_params(db,query,query_args)
            result=atpic.libpqalex.process_result(result)
            atpic.log.debug(yy,"result=",result)
        time2=time.time()
        ittook=time2-time1
        atpic.log.debug(yy,"It took (seconds):",ittook)
    return (db,dbcounter)    


def main_loop():
    yy=atpic.log.setname(xx,'main_loop')

    atpic.log.info(yy,"STARTING zmq_asyncdone_server....")
    
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://192.168.69.1:5057")
    dbcounter = 0
    db=None

    idxsocket=atpic.zmq_index_client.get_socket()

    while True:
        try:
            # receive the message
            msg = socket.recv()
            receivedData=msg
            atpic.log.info(yy,"receivedData",receivedData)
            (db,dbcounter)=do_processing(receivedData,db,dbcounter)
            do_index(receivedData,idxsocket)


        except KeyboardInterrupt:
            raise
        except:
            atpic.log.error(yy,traceback.format_exc())
            atpic.log.error(yy,'LOST MESSAGE',(receivedData))
            # raise
            # KeyboardInterrupt

if __name__ == "__main__":
    yy=atpic.log.setname(xx,'main')
    main_loop()
