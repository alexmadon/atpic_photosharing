#!/usr/bin/python3
# import logging
import sys

import atpic.log

xx=atpic.log.setmod("INFO","pdns_pipe.old1")



"""
Python 3.1 added io.TextIOBase.detach(), with a note in the documentation for sys.stdout:

    The standard streams are in text mode by default. To write or read binary data to these, use the underlying binary buffer. For example, to write bytes to stdout, use sys.stdout.buffer.write(b'abc'). Using io.TextIOBase.detach() streams can be made binary by default. This function sets stdin and stdout to binary:

    def make_streams_binary():
        sys.stdin = sys.stdin.detach()
        sys.stdout = sys.stdout.detach()



"""



def getLine(afile):
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
        next_byte = afile.read(1)  # read a byte
        print('next_byte',next_byte)
        if next_byte == b"\n":    # if it's end of line, break
            print('got newline, breaking')
            break                  
        line += next_byte         # otherwise, istick it with the rest
    return line
    

infile = sys.stdin
outfile = sys.stdout

while True:
    # inline=infile.readline()
    # outfile.write(inline)
    inline=getLine(infile.buffer)
    print('inline',inline)
    outfile.buffer.write(inline+b'\n')
    outfile.buffer.flush()
