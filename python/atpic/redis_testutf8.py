#!/usr/bin/python3
# https://github.com/stargazer/Red-Pie
import time
from red import pie                  
#import redis
start = time.clock()
for i in range(100):
    server = pie.Redis()
    server.select(5)
    
    # print(dir(server))
    server.set("Clara cet été","là")
    key=server.get("Clara cet été")
    # print(key)
    server.quit()
elapsed = time.clock() - start
print(elapsed)


# times = []
# for j in range(5):
#     start = time.clock()
#     for i in range(100):
#         server.hset("key","field","value")
#         #server.hset("word","field","value")
#         #server.hset("word","fielr","value")
#     elapsed = time.clock() - start
#     times.append(elapsed)
#     print(elapsed)
