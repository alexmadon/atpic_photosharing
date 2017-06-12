# task scheduler
# inspired by 'ts' (C program)
# and oreilly
# Example 19-8. Asynchronous TCP echo server using asynchat
# but with uni domain sockets

import asyncore
import asynchat
import socket
import os

class MainServerSocket(asyncore.dispatcher):
    def __init__(self, port):
        print 'initing MSS'
        asyncore.dispatcher.__init__(self)
        # self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.create_socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # self.bind(('',port))
        unixsocket="/tmp/socketname"
        try:
            os.remove(unixsocket)
        except OSError:
            pass
        self.bind(unixsocket)

        self.listen(5)
    def handle_accept(self):
        newSocket, address = self.accept(  )
        print "Connected from client"
        SecondaryServerSocket(newSocket)
    def writable(self):
        return 0
    def readable(self):
        return 1

class SecondaryServerSocket(asynchat.async_chat):
    def __init__(self, *args):
        print 'initing SSS'
        asynchat.async_chat.__init__(self, *args)
        self.set_terminator('\n')
        self.data = []
    def collect_incoming_data(self, data):
        self.data.append(data)
    def found_terminator(self):
        data2send=''.join(self.data)
        print "will send %s" % data2send
        self.push(data2send)
        self.data = []
    def handle_close(self):
        print "Disconnected from client"
        self.close(  )

MainServerSocket(8881)
asyncore.loop(  )
