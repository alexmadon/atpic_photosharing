#!/usr/bin/python3
# similar to twuwsgi.py the twisted uwsgi client

import socket
import struct
import time

def packvar(key,value):
    # this packs a variable
    return struct.pack('<H',len(key)) + key + struct.pack('<H',len(value)) + value

def packall(keyvals):
    # recieves as input a list of (key,value) to pack
    # returns a string of bytes correctly packed
    keyvals_packed=[]
    for (key,value) in keyvals:
        keyvals_packed.append(packvar(key,value))

    keyvals_bytes=b''.join(keyvals_packed)
    # data to send
    data=struct.pack('<BHB',0, len(keyvals_bytes),0)+keyvals_bytes
    return data

def forge_keyvals():
    keyvals=[]
    keyvals.append((b'CONTENT_LENGTH',b'0'))
    # keyvals.append((b'REQUEST_METHOD',b'GET'))
    # keyvals.append((b'PATH_INFO',b'/aaaa'))
    return keyvals

if __name__ == "__main__":
    keyvals=forge_keyvals()
    print(keyvals)
    keyvals_packed=packall(keyvals)
    t1=time.time()
    amax=1000
    for i in range(0,amax):        
        usock = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
        usock.connect( "/var/run/uwsgi/app/test/socket" )
        # usock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # usock.connect(('localhost', 9099))
        usock.send(keyvals_packed)
        response=usock.recv(1024)
        usock.close()
    t2=time.time()
    print('Time',t2-t1,'s',amax/(t2-t1),'req/s')
    print(response)
