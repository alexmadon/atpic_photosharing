import sys
# import logging
from atpic.mybytes import *
import atpic.log
xx=atpic.log.setmod("INFO","redis_pie_comm")



def getLine(sock):
    """ Reads the response of the server, byte per byte,
        and returns a line of the server response
        The line returned is in byte format, not in 
        any encoded form.

        In the end, the socket points to the start of the next line

        @param line: Socket communicating with the redis server
        @return: A line of bytes
    """
    yy=atpic.log.setname(xx,'getLine')
    line = b""
    while True:
        next_byte = sock.recv(1)  # read a byte
        if next_byte == b"\r":    # if it's end of line, break
            break                  
        line += next_byte         # otherwise, istick it with the rest
    sock.recv(1)                  # Consume the remaining \n character
    # atpic.log.debug(yy,'will return:',line)
    return line
    

def getLineAlex(sock):
    # need a readline like
    f = sock.makefile("rb") # converts a socket to a file
    line=f.readline()
    f.close()
    return line

def constructMessage(command, args = []):
    """ Constructs the appropriate message, 
        that will be send to the redis server.
        The message represents a database query
        
        @param command: Database command to execute
        @param args: List of arguments for command
        @return: Message that will be send to the redis server
        in order to execute the query

        Messages are in the form:
        *<num arguments>\r\n
        $<length of command>\r\n
        command\r\n
        $<length of arg>\r\n
        argument\r\n
        $<length of arg>\r\n
        argument\r\n
        ...
        ...\r\n
    """
    yy=atpic.log.setname(xx,'constructMessage')
    atpic.log.debug(yy,"->",command,args)
    part_1 = [ \
        b"*" + int2bytes(len(args) + 1), \
        b"$" + int2bytes(len(command)), \
        command \
    ]
    atpic.log.debug(yy,"part1",part_1)
    part_2 = []
    atpic.log.debug(yy,"args",args)
    for arg in args:
        atpic.log.debug(yy,"arg",arg)
        # arg = str(arg)
        part_2.append(b"$" + int2bytes(len(arg)))
        part_2.append(arg)

    atpic.log.debug(yy,part_1,part_2)
    message = b"\r\n".join(part_1 + part_2) + b"\r\n"
    atpic.log.debug(yy,"will send message:", message)
    # return message.encode("utf8")
    return message
