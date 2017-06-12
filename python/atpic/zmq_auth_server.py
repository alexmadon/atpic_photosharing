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
import atpic.authenticatesql
import atpic.errors
import atpic.mybytes
import atpic.libpqalex

xx=atpic.log.setmod("INFO","zmq_auth_server")

global db
global counter

counter=0

def getdb():
    global db
    global counter
    yy=atpic.log.setname(xx,'getdb')
    atpic.log.debug(yy,'counter=',counter)
    if counter==0:
        db=atpic.libpqalex.db_native()
        counter=1
    else:
        counter=counter+1
        pass
    return db

def deldb():
    # remove the db if too old
    global db
    global counter
    yy=atpic.log.setname(xx,'deldb')

    atpic.log.debug(yy,'counter=',counter)
    if counter>20:
        counter=0
        atpic.log.debug(yy,'closing db')
        atpic.libpqalex.close(db)
        atpic.log.debug(yy,'closed db')

def auth(username,password):
    db=getdb()
    yy=atpic.log.setname(xx,'auth')
    (authd,details)=atpic.authenticatesql.check_username_password(username,password,db)
    deldb()
    return authd 

def parse_message(request):
    yy=atpic.log.setname(xx,'parse_message')
    atpic.log.debug(yy,'input=',request)
    splitted=request.split(b':')
    username=splitted[0]
    password=b'|'.join(splitted[1:])
    authd=auth(username,password)
    atpic.log.debug(yy,'output=',authd)
    return authd

def main_loop():
    yy=atpic.log.setname(xx,'main_loop')

    # socket to zmq
    context = zmq.Context()
    zmqsocket = context.socket(zmq.REP)
    atpic.log.info(yy,'starting zmq_auth_server')
    zmqsocket.bind("tcp://127.0.0.1:5558")

    while True:
        try:
            # Wait for next request from client
            atpic.log.debug(yy,"waiting to get a message on ZMQ socket")
            request = zmqsocket.recv()
            atpic.log.debug(yy,"Received request: ", request)
            authd=parse_message(request)
            if authd:
                zmqsocket.send(b'ok')
            else:
                zmqsocket.send(b'notok')
        except:
            atpic.log.error(yy,traceback.format_exc())
            zmqsocket.send(b'error')

            # pass

if __name__ == "__main__":
    print('starting')#
    main_loop()
    pass
