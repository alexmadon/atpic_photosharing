import zmq
import struct
import time

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://127.0.0.1:5000")
counter = 0

while True:
    # receive the message
    msg = socket.recv()

    # print ("Message Size is: {0} [MB]".format( len(msg) / (1000 * 1000) ))
    counter += 1
    print ("Total messages recieved: {0}".format(counter))
    time.sleep(1)
