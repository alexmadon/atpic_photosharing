#!/usr/bin/python3

import atpic.errors
import atpic.log
import atpic.redis_pie                 
from atpic.mybytes import *
from atpic.redisconst import *

"""
Anti DoS based on memory cache (redis, memcache)
Current implementation uses redis

The redis keys are:

iIP (counter)
bIP (blacklist with value B)

we count over a sliding window of 1 second
If count > 20 we blacklist for 5 minutes.

"""

xx=atpic.log.setmod("INFO","antidos")



def blacklist(environ):
    yy=atpic.log.setname(xx,'blacklist')
    # blist=['192.168.1.1','127.0.0.1',]
    blist=[]
    ip=environ[b'REMOTE_ADDR']
    atpic.log.debug(yy,'input ip:',ip)
    if ip in blist:
        atpic.log.debug(yy,'that ip is blacklisted')
        raise atpic.errors.AntidosError
    else:
        atpic.log.debug(yy,'that ip is not blacklisted')



def whitelist(ip):
    yy=atpic.log.setname(xx,'whitelist')
    white=[
        # my ips
        b"127.0.0.1",
        b"216.32.66.210",
        b"216.32.66.211",
        b"88.198.67.36",
        b"213.133.123.140",
        b"88.198.21.167",
        b"46.4.24.136",
        # other whitelisted addresses
        b"194.239.94.33",
        b"85.80.174.206", # carsten
        b"195.6.174.244", # groupama
        ]
    atpic.log.debug(yy,'inpit ip:',ip)
    if ip in white:
        atpic.log.debug(yy,'that ip is whitelisted')
        return True
    else:
        atpic.log.debug(yy,'that ip is not whitelisted')
        return False

def getcount(rediscon,ip,period):
    # read an increment
    yy=atpic.log.setname(xx,'getcount')
    atpic.log.debug(yy,'input',rediscon,ip,period)
    count=atpic.redis_pie._incr(rediscon,REDIS_IP_CNT+ip)         #  i like IP (counter)
    atpic.log.debug(yy,count)
    res=atpic.redis_pie._expire(rediscon,REDIS_IP_CNT+ip,period)  #  i like IP expires
    atpic.log.debug(yy,'will return:',count)
    return count

def set_cache_blacklist(rediscon,ip):
    yy=atpic.log.setname(xx,'getcount')
    atpic.log.debug(yy,"blacklisting",ip)
    atpic.redis_pie._set(rediscon,REDIS_IP_BLK+ip,b'B')           # b,B like 'Blacklisted'
    atpic.redis_pie._expire(rediscon,REDIS_IP_BLK+ip,b'300')      # blacklist for 5 minutes

def get_cache_blacklist(rediscon,ip):
    yy=atpic.log.setname(xx,'get_cache_blacklist')
    atpic.log.debug(yy,'input:',rediscon,ip)
    value=atpic.redis_pie._get(rediscon,REDIS_IP_BLK+ip)          # b like blacklist
    if value==b'B':
        atpic.log.info(yy,ip,"is blacklisted")
        raise atpic.errors.AntidosError


def protect(rediscon,environ):
    """
    Check the number of connections per timeperiod from an IP.
    If greater than a limit, then raise a exception to block.

    """
    yy=atpic.log.setname(xx,'protect')
    atpic.log.debug(yy,'input',rediscon,environ)
    ip=environ[b'REMOTE_ADDR']
    if whitelist(ip):
        pass
    else:
        if get_cache_blacklist(rediscon,ip):
            atpic.log.debug(yy,'AntidosError1')
            raise atpic.errors.AntidosError
        else:
            period=b'1' # 1 second
            maxperperiod=b'40' #
            count=getcount(rediscon,ip,period)
            if bytes2int(count)>bytes2int(maxperperiod):
                # put in cache black list
                set_cache_blacklist(rediscon,ip)
                atpic.log.debug(yy,'AntidosError2')
                raise atpic.errors.AntidosError
            else:
                pass


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    yy=atpic.log.setname(xx,'main')

    environ={b'REMOTE_ADDR':b'1.1.1.1', }
    rediscon=atpic.redis_pie.Redis()
    for i in range(1,10):
        protect(rediscon,environ)
