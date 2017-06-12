#!/usr/bin/python3
import time
from red import pie                  
#import redis

server = pie.Redis()
server.select(5)
server.hset("key","field","value")
server.hset("key","","value2")
# server.hset("key","field","value")
val=server.hget("key","")
print(val)
quit()

times = []
for j in range(5):
    start = time.clock()
    for i in range(10000):
        #server.hset("key","field","value")
        #server.hset("word","field","value")
        #server.hset("word","fielr","value")
        server.set("key","value")
    elapsed = time.clock() - start
    times.append(elapsed)
    print(elapsed)
