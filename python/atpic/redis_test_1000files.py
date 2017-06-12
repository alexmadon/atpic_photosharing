#!/usr/bin/python3
# import logging
import re
import traceback
import socket
import time
import atpic.log
import atpic.redis_pie  
import atpic.mybytes

xx=atpic.log.setmod("INFO","redis_test_1000files")





if __name__ == "__main__":
    print('hi')
    server = atpic.redis_pie.Redis()
    start = time.clock()
    amax=1 # 1000
    for i in range(amax):
        server._hset(b"word",b"field"+atpic.mybytes.int2bytes(i),b"value"+atpic.mybytes.int2bytes(i))
    elapsed = time.clock() - start

    print(elapsed)

    start = time.clock()
    #val=server._hget("word","field888")
    for i in range(amax):
        server._hget(b"word",b"field"+atpic.mybytes.int2bytes(i))
    elapsed = time.clock() - start
    print(elapsed)
    # print(val)



    start = time.clock()
    for i in range(amax):
        server._set(b"wordfield"+atpic.mybytes.int2bytes(i),b"value"+atpic.mybytes.int2bytes(i))
    elapsed = time.clock() - start

    print(elapsed)

    start = time.clock()
    #val=server._hget("word","field888")
    for i in range(amax):
        server._get(b"wordfield"+atpic.mybytes.int2bytes(i))
    elapsed = time.clock() - start
    print(elapsed)

    print('getall:')

    start = time.clock()
    server._hgetall(b"word")
    elapsed = time.clock() - start
    print(elapsed)

    print('del:')

    start = time.clock()
    server._del(b"word")
    elapsed = time.clock() - start
    print(elapsed)
