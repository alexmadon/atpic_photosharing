#!/usr/bin/python3
# checks that all daemons run
# the asyncdone can have test messages (start with a 't')

# difficult because of asynchronous

# in zmq PUSH-PULL, could add time stamp
import atpic.zmq_asyncdone_client


if __name__ == "__main__":
    socket=atpic.zmq_asyncdone_client.get_socket()
    atpic.zmq_asyncdone_client.send(socket,b'tU|7|3333|image/x-canon-crw|3072|2048||||2.8||||||||')
    socket.close()
