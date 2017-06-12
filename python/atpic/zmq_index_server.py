#!/usr/bin/python3
import zmq
import time
import traceback


import atpic.log
import atpic.redis_pie
import atpic.redis_index_client

"""
A light wrapper around redis.
may not be needed but we light zmq buffering

This is a single threaded tcp server.
"""

xx=atpic.log.setmod("INFO","zmq_index_server")


def send_to_redis_index(message,rediscon):
    yy=atpic.log.setname(xx,'send_to_redis_index')
    (uid,gid,pid)=message.split(b'|')
    atpic.log.debug(yy,'we do need to index, sending to redis',(uid,gid,pid))
    atpic.redis_index_client.put_in_queue(rediscon,uid,gid,pid)
    

def main_loop():
    yy=atpic.log.setname(xx,'main_loop')

    atpic.log.info(yy,"STARTING zmq_index_server....")
    
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://127.0.0.1:5059")

    rediscon=atpic.redis_pie.connect_first()

    while True:
        try:
            # receive the message
            msg = socket.recv()
            receivedData=msg
            atpic.log.info(yy,"receivedData",receivedData)
            send_to_redis_index(receivedData,rediscon)
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
