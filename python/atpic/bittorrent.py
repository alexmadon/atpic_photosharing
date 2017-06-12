# -*- coding: utf-8 -*-


import struct
import socket
# http://code.activestate.com/recipes/66517/
# http://sourceforge.net/projects/lighttracker
peers=[
    ("192.168.58.23",3331),
    ("122.168.58.23",8831)
]

packed=""
for (ip,port) in peers:
    packed += socket.inet_aton(ip) + struct.pack('>H', int(port))
    # in Python:
    # ! 	network (= big-endian) 	standard
    # L 	unsigned long 	long
    # H 	unsigned short 	integer
    # PHP format is Nn
    # N  	unsigned long (always 32 bit, big endian byte order)
    # n  	unsigned short (always 16 bit, big endian byte order)

print packed

