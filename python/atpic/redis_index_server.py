#!/usr/bin/python3
import time
import traceback


import atpic.log
import atpic.redis_pie
from atpic.redisconst import *
import atpic.mybytes
import atpic.elasticsearch_sql
import atpic.zmq_elastic_client
import atpic.connection_young


xx=atpic.log.setmod("INFO","redis_index_server")

# we re-index a uid, a uid:gid or a uid:gid:pid
# the aim is to smooth and avoid DOS
# you put in a set once until we process a snapshot
# next puts just override the first put

def transform2triplet(logkey):
    yy=atpic.log.setname(xx,'transform2triplet')
    atpic.log.debug(yy,'input=',logkey)
    splitted = logkey.split(b':')
    if len(splitted)==3:
        (uid,gid,pid)=splitted
    elif len(splitted)==2:
        (uid,gid)=splitted
        pid=b''
    elif len(splitted)==1:
        uid=splitted[0]
        pid=b''
        gid=b''
    atpic.log.debug(yy,'output=',(uid,gid,pid))
    return (uid,gid,pid)

def do_reindex(logkey,db,essock):
    yy=atpic.log.setname(xx,'do_reindex')
    atpic.log.debug(yy,'input=',logkey)
    (uid,gid,pid)=transform2triplet(logkey)
    atpic.log.info(yy,'need to reindex (uid,gid,pid)=',(uid,gid,pid))
    atpic.elasticsearch_sql.doindex_pic(uid,gid,pid,db,essock)
    atpic.elasticsearch_sql.doindex_path(uid,gid,pid,db,essock)
    atpic.elasticsearch_sql.doindex_vpath(uid,gid,pid,db,essock)


def process_queue(rediscon,db,essock):
    yy=atpic.log.setname(xx,'process_queue')
    atpic.log.debug(yy,'starting...')
    atpic.log.debug(yy,'taking a snapshot of the queue:')
    atpic.redis_pie._sinterstore(rediscon,REDIS_INDEX+b'processqueue', [REDIS_INDEX+b'queue'])
    numitems = atpic.redis_pie._scard(rediscon,REDIS_INDEX+b'processqueue')    # return number of items in our set 'log'
    numitems=atpic.mybytes.bytes2int(numitems)
    atpic.log.debug(yy,'number of items to do:',numitems)
    for i in range(0, numitems):
        atpic.log.debug(yy,'doing item',i)
        logkey = atpic.redis_pie._spop(rediscon,REDIS_INDEX+b'processqueue')     # grab an item from our set 'log' and delete it from the set
        do_reindex(logkey,db,essock)
        # delete from the original set:
        atpic.redis_pie._srem(rediscon,REDIS_INDEX+b'queue',logkey)
    atpic.log.debug(yy,'finished')


def main_loop():
    yy=atpic.log.setname(xx,'main_loop')
    rediscon=atpic.redis_pie.connect_first()
    essock=atpic.zmq_elastic_client.connect_first()
    dbcounter = 0
    db=None

    while True:
        try:
            (db,dbcounter)=atpic.connection_young.get_db(db,dbcounter)
            process_queue(rediscon,db,essock)
            atpic.log.debug(yy,"sleeping")
            time.sleep(1)
        except:
            atpic.log.error(yy,traceback.format_exc())
            time.sleep(1)

    put_in_queue(rediscon,b'1')
    put_in_queue(rediscon,b'2')
    put_in_queue(rediscon,b'2:22:333')
    process_queue(rediscon)


if __name__ == "__main__":
    print('starting')#
    main_loop()
    pass

