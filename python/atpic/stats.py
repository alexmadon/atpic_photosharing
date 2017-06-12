#!/usr/bin/python3
# keep the statistics and pages hits
# in a queue like redis
# 
# what do we count?
# the nb of display of 
# GET alex.atpic.faa/
# GET alex.atpic.faa/gallery/1
# GET alex.atpic.faa/gallery/1/pic/22

# # import logging
import time

# import atpic.worker
import atpic.log
import atpic.redis_pie
from atpic.redisconst import *
import atpic.mybytes

xx=atpic.log.setmod("INFO","stats")


def update_stats(rediscon,hxplo,pxplo,actions):
    """
    Write into redis the pic details
    Should we track gallery?
    Gallery does not mean too much now that we have search and blog 
    (tree == gallery)
    """
    yy=atpic.log.setname(xx,'update_stats')
    atpic.log.debug(yy,'input=',rediscon,hxplo,pxplo,actions)
    if pxplo.keys()==[b'user',b'gallery',b'pic']:
        if pxplo.getmatrix(2,1):
            atpic.log.debug(yy,'we need to update pic stats')
            uid=pxplo.getmatrix(0,1)
            gid=pxplo.getmatrix(1,1)
            pid=pxplo.getmatrix(2,1)
            atpic.log.debug(yy,uid,pid,gid)
            put_stats(rediscon,uid,pid,gid)
    else:
        atpic.log.debug(yy,'no stats to update')
    


def put_stats(rediscon,uid,pid,gid):
    yy=atpic.log.setname(xx,'put_stats')
    atpic.log.debug(yy,'input',rediscon,uid,pid,gid)
    atpic.redis_pie._incr(rediscon,REDIS_STATS+uid+b':'+gid+b':'+pid) # increment a redis counter#
    atpic.redis_pie._sadd(rediscon,REDIS_STATS+b'log',uid+b':'+gid+b':'+pid)

    pass

def process_list(rediscon):
    """
    Each time a (uid,gid,pid) is accessed, 
    a) increment a counter counter_(uid,gid,pid)
    b) and (re)add the counter key to a list of stats: 'stats_set'
    Later you have a process that 
    1) get all the keys is stats_set (set copy)
    2) and process them one by one:
         a) get and remove the key (non atomic? = bad)
         b) and increment in SQL
    """
    yy=atpic.log.setname(xx,'process_list')
    atpic.log.debug(yy,'starting...')
    # dayhour_key = time.strftime('%Y%m%d%H', time.localtime())
    atpic.redis_pie._sinterstore(rediscon,REDIS_STATS+b'processlog', [REDIS_STATS+b'log'])
    numitems = atpic.redis_pie._scard(rediscon,REDIS_STATS+b'processlog')    # return number of items in our set 'log'
    numitems=atpic.mybytes.bytes2int(numitems)
    for i in range(0, numitems):
        atpic.log.debug(yy,'doing item',i)
        logkey = atpic.redis_pie._spop(rediscon,REDIS_STATS+b'processlog')     # grab an item from our set 'log' and delete it from the set
        splitted = logkey.split(b':')
        atpic.log.debug(yy,splitted) # REDIS_STATS+uid+b':'+gid+b':'+pid
        count = atpic.redis_pie._get(rediscon,REDIS_STATS+logkey)     # get the count from our key
        atpic.log.debug(yy,'count',count)
        atpic.redis_pie._del(rediscon,REDIS_STATS+logkey)
        # delete from the original set:
        atpic.redis_pie._srem(rediscon,REDIS_STATS+b'log',logkey)

def monitor(rediscon):
    yy=atpic.log.setname(xx,'monitor')
    atpic.log.debug(yy,'starting...')
    nb1=atpic.redis_pie._scard(rediscon,REDIS_STATS+b'processlog')
    nb2=atpic.redis_pie._scard(rediscon,REDIS_STATS+b'log')
    atpic.log.debug(yy,nb1,nb2)

def daemon(rediscon):
    yy=atpic.log.setname(xx,'daemon')
    atpic.log.debug(yy,'starting...')
    while True:
        process_list(rediscon)
        atpic.log.debug(yy,'sleepin...')
        time.sleep(10)

def hi():
    yy=atpic.log.setname(xx,'hi')
    atpic.log.debug(yy,'starting...')

if __name__ == "__main__":
    hi()
    rediscon=atpic.redis_pie.Redis()
    put_stats(rediscon,b'1',b'22',b'333')
    print('hello')
    monitor(rediscon)
    process_list(rediscon)
    rediscon.quit()
