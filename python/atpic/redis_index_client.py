#!/usr/bin/python3
import time

# import atpic.worker
import atpic.log
import atpic.redis_pie
from atpic.redisconst import *
import atpic.mybytes

xx=atpic.log.setmod("INFO","redis_index_client")

# we re-index a uid, a uid:gid or a uid:gid:pid
"""
not sure how to deal with deletes.
maybe delete anything you want to reindex.

"""
def put_in_queue(rediscon,uid,gid=None,pid=None):
    yy=atpic.log.setname(xx,'put_in_queue')
    atpic.log.debug(yy,'input',rediscon,uid,gid,pid)
    if pid:
        key=b':'.join((uid,gid,pid))
    elif gid:
        key=b':'.join(uid,gid)
    else:
        key=uid
    atpic.log.debug(yy,'key',key)
    atpic.redis_pie._sadd(rediscon,REDIS_INDEX+b'queue',key)


def get_queue_card(rediscon):
    """
    gets the number of items in the queue that remains to index.
    """
    yy=atpic.log.setname(xx,'get_queue_card')
    numitems = atpic.redis_pie._scard(rediscon,REDIS_INDEX+b'queue')
    atpic.log.debug(yy,'number of items to do:',numitems)
    return numitems

# need to reindex for each action in FTP, HTTP, (SMTP)
# (re-)indexing needs to happen AFTER a poc is transformed to thumbs
# as we do index paths
# so ideally that should be done sending a ZMQ message to asyncdone server

# reindexing a user is costful:
# only reindex gallery or pic if possible (just what is necessary)

# when using index you have to balance between
# indexng speed, search speed: you can't have both high:
# we chose slow indexing, fast searches
if __name__ == "__main__":
    rediscon=atpic.redis_pie.connect_first()

    put_in_queue(rediscon,b'1')
    put_in_queue(rediscon,b'2')
    put_in_queue(rediscon,b'2',b'22',b'333')
    time.sleep(2)    
    put_in_queue(rediscon,b'11')
    put_in_queue(rediscon,b'22')
    put_in_queue(rediscon,b'22',b'22',b'333')
    time.sleep(2)    
    put_in_queue(rediscon,b'111')
    put_in_queue(rediscon,b'222')
    put_in_queue(rediscon,b'222',b'22',b'333')
