import zmq
import struct

# define a string of size 4[MB] 
msgToSend = struct.pack('i', 45) * 1000 * 1000 

context = zmq.Context()
socket = context.socket(zmq.PUSH)
# socket.setsockopt(zmq.HWM, 8)
socket.connect("tcp://127.0.0.1:5000")

# print the message size in bytes
for i in range(100):
    socket.send(msgToSend)
    print("Sent message")
