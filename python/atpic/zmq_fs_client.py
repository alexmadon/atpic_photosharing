#!/usr/bin/python3

import zmq

context = zmq.Context()

# Socket to talk to server
print ("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:5555")

# Do 10 requests, waiting each time for a response
requests=[
b'readdir /alexmadon/italia2006',
b'readdir /alexmadon/italia2006/firenze',
b'readdir alexmadon/italia2006/firenze',
b'realpath /alexmadon/italia2006/firenze/immagine_292.jpg',
# b'create /alexmadon/italia2006/firenze/test10.jpg',
b'readdir /alexmadon/55124',
b'dirtype /alexmadon',
b'dirtype /alexmadon/a',
b'dirtype /alexmadon/a/b',
b'dirtype /alexmadon/a/b/c',
b'dirtype /alexmadon/a/b/c/bad',
b'dirtype /alexmadon/italia2006',

]
for request in requests:
    print (">>", request)
    socket.send (request)
    # Get the reply.
    message = socket.recv()
    print ("<<", message)
