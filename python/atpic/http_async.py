#!/usr/bin/python
"""
Example 19-8. Asynchronous TCP echo server using asynchat

Example 19-8 uses module asynchat to reimplement the server of Example 19-7, with small differences due to using class asynchat.async_chat instead of class asyncore.dispatcher_with_send. To highlight async_chat's typical use, Example 19-8 responds (by echoing the received data back to the client, like all other server examples in this chapter) only when it has received a complete line (i.e., one ending with \n).


oreiley
python http_async.py


/usr/local/apache2/bin/ab -n 1000 -c 10 http://localhost:8882/

"""

import asyncore
import asynchat
import socket
import atpic.httpr
import atpic.tokyofs # we need it here to open a connection to tokyo DB



import psyco # package python-psyco 
psyco.full()

# counter=0

def myprint(message):
    pass
    # print message

class MainServerSocket(asyncore.dispatcher):
    def __init__(self, port):
        print 'initing MainServerSocket'
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr() # allow to rebind without having to wait 1 minute if killed
        self.bind(('',port))
        self.listen(5)
        print("Listening on port %s" % port)
        # connect to tokyo to get a db handler
        dbh=atpic.tokyofs.open()
        self.dbh=dbh

    def handle_accept(self):
        newSocket, address = self.accept()
        # myprint("Remote: %s, %i " % address)
        SecondaryServerSocket(newSocket,address,self.dbh)

    def handle_close(self):
        self.close()




class SecondaryServerSocket(asynchat.async_chat):
    def __init__(self, newSocket,address,dbh): # could pass only newSocket, but pass addres too to debug
        # dbh is the tokyo db handler
        # myprint("initing SecondaryServerSocket")
        # myprint("from address %s %i" % (address[0],address[1]))
        asynchat.async_chat.__init__(self, newSocket)
        self.set_terminator('\r\n\r\n')
        self.head=True # start to expect Headers
        self.data = [] # data is owned by this secondary server
        # informative:
        self.address=address
        self.dbh=dbh # tokyo

    def collect_incoming_data(self, data):
        # myprint("-> %s:%i, collect_incoming_data: %s" % (self.address[0],self.address[1],data))
        self.data.append(data)

    def found_terminator(self):     
        # myprint("Found terminator")
        # react to self.data
        # myprint("reaction to: %s " % "\n".join(self.data))
        # self.push(''.join(self.data))

        if self.head:
            # process the headers and check if we need to keep reading
            self.headers=self.data
            self.data = []
            size=atpic.httpr.parse_headers(self.headers)
            print "size=%i" % size
            # if size>0 then we need to keep reading
            if size>0:
                self.set_terminator(size) # we need to read 'size' bytes
                self.head=False # start to expect Body
            else:
                response=atpic.httpr.answer(headers=self.headers,tokyo=self.dbh)
                self.push(response)
                self.data = []
                self.handle_close() # we have nothing more to say
                
        else:
            # this is what comes after the headers
            response=atpic.httpr.answer(headers=self.headers,tokyo=self.dbh,body=self.data)
            self.push(response)
            self.data = []
            self.handle_close() # we have nothing more to say

    def handle_close(self):
        # print "Disconnected from", self.getpeername(  )
        self.close()



# connect to tokyo

# start the HTTP server
MainServerSocket(8882)
asyncore.loop()
