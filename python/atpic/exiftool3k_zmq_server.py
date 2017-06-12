#!/usr/bin/python3
import subprocess
# import logging
import atpic.log
import os
import socket
import sys
import zmq
import time
import signal
import traceback

import atpic.processinfiles

"""
This is a single threaded tcp server.
As exiftool requires a single thread of input we should not multithread this one.
Rather use a zmq queue to serialize requests.

Needs to be run as 'www-user' as we need to write to the filesystem.
"""

xx=atpic.log.setmod("INFO","exiftool3k_zmq_server")



def handler(signum, frame):
    yy=atpic.log.setname(xx,'handler')
    atpic.log.debug(yy,'Signal handler called with signal', signum)
    # raise IOError("Couldn't open device!")
    p1.kill() # or .terminate()
    quit()


def start_exif():
    """
    Starts the exiftool process. We will write to it using process pipes.
    """
    yy=atpic.log.setname(xx,'readpipe')
    atpic.log.debug(yy,"starting exiftool")
    # exiftool -stay_open True -@ exifpipe > exifresults 2>&1 &
    p1=subprocess.Popen(["exiftool","-stay_open","True","-@","-"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    print("p1 %s" % p1)
    return p1


def readpipe(read_pipe):
    """
    reads one line from the exiftool pipe.
    """
    yy=atpic.log.setname(xx,'readpipe')
    line = read_pipe.readline()
    line=line.decode('utf8')
    return line

def read_out(read_pipe):
    """
    Reads on the exiftool pipe the metadata analysis results made by exiftool
    """
    yy=atpic.log.setname(xx,'read_out')
    lines=[]
    line=readpipe(read_pipe)
    atpic.log.debug(yy,'aaa %s' % line)
    if line=="{ready}\n":
        atpic.log.debug(yy,'GOT END')
        pass
    else:
        lines.append(line)
        atpic.log.debug(yy,'first line=%s' % line)
        while line:
            line = readpipe(read_pipe)
            if line=="{ready}\n":
                atpic.log.debug(yy,'GOT END')
                break
            else:
                lines.append(line)
    thexml=''.join(lines)
    return thexml # there was no error



if __name__ == "__main__":
    yy=atpic.log.setname(xx,'main')
    # run as user www-data
    os.setuid(33)

    # Set the signal handler and a 5-second alarm

    signal.signal(signal.SIGTERM, handler)

    atpic.log.debug(yy,"daemon started")
    
    p1=start_exif()
    # atpic.log.debug(yy,dir(p1))
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://127.0.0.1:5000")
    counter = 0
    ittooks=[]
    while True:
        try:
            # receive the message
            msg = socket.recv()
            counter += 1
            atpic.log.debug(yy,"Total messages recieved: {0}".format(counter))
            receivedData=msg
            atpic.log.debug(yy,"receivedData",receivedData)
            time1=time.time()
            p1.stdin.write(b'-X\n')
            p1.stdin.write(b'-long\n')
            p1.stdin.write(receivedData+b'\n') # the filename as bytes with \n
            p1.stdin.write(b"-execute\n")
            
            
            thexml=read_out(p1.stdout)
            atpic.log.debug(yy,thexml)
            time2=time.time()
            ittook=time2-time1
            atpic.log.debug(yy,"It took (seconds):",ittook)
            ittooks.append(ittook)
            ittooks=ittooks[-10:]
            # print(ittooks)
            atpic.log.debug(yy,'it took',sum(ittooks)/len(ittooks))
        except:
            atpic.log.error(yy,traceback.format_exc())
            raise
            # KeyboardInterrupt
