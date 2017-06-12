#!/usr/bin/python3
# python3.1 version
"""
Implement memcache protocol client side
as documented at:
http://code.sixapart.com/svn/memcached/trunk/server/doc/protocol.txt
"""
# WARNING: memcache protocol does NOT allow spaces in keys
# so not a good candidate to store path (path can have spaces)
# and you would need to escape them (aas in URLs)

import socket
import time
# import logging

import atpic.log


xx=atpic.log.setmod("INFO","memcached3")



def connect(host='127.0.0.1',port=11211):
    # HOST = '127.0.0.1'    # The remote host
    # PORT = 11211             # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s



def get_line(sock): # from red/pie getLine (redis)
    """
    get one line from the socket
    """
    # yy=atpic.log.setname(xx,'get_line')
    line = b""
    while True:
        next_byte = sock.recv(1)  # read a byte
        if next_byte == b"\r":    # if it's end of line, break
            break                  
        line += next_byte         # otherwise, istick it with the rest
    sock.recv(1)                  # Consume the remaining \n character
    # atpic.log.debug(yy,'line',line)
    return line

# =========================
#      storage commands
# =========================
def store(con,command,key,value,flags=0,exptime=0):
    """
    command should be one of "set","add","replace","append","prepend"
    aliases are defined below
    we do not test the validity of the commands for performance reasons 
    (one test less)
    """
    # yy=atpic.log.setname(xx,'store')
    if isinstance(value,int):
        value="{0}".format(value)
        
    commandb=command.encode('utf-8')
    keyb=key.encode('utf-8')
    valueb=value.encode('utf-8')
    bytesnb=len(valueb)
    thecommand="{command} {key} {flags} {exptime} {bytes}\r\n{value}\r\n".format(command=command,key=key,flags=flags,exptime=exptime,bytes=bytesnb,value=value) 
    # atpic.log.debug(yy,'thecommand --->',thecommand,'<---')
    con.send(thecommand.encode('utf-8'))
    response=get_line(con)
    # atpic.log.debug(yy,'response',response)
    return response


# ====================================
#      storage commands aliases
# ====================================

def set(con,key,value,flags=0,exptime=0):
    return store(con,"set",key,value,flags=0,exptime=0)

def add(con,key,value,flags=0,exptime=0):
    return store(con,"add",key,value,flags=0,exptime=0)

def replace(con,key,value,flags=0,exptime=0):
    return store(con,"replace",key,value,flags=0,exptime=0)

def append(con,key,value,flags=0,exptime=0):
    return store(con,"append",key,value,flags=0,exptime=0)

def prepend(con,key,value,flags=0,exptime=0):
    return store(con,"prepend",key,value,flags=0,exptime=0)

# ====================================
#      retrieval commands
# ====================================



def gets(con,*keys):
    """
    Expects a variable number of keys and return an array of key->values,
    the length of the ouput can be less thatn the length of the input 
    as some keys may not be found
    """
    keyss=" ".join(keys)
    #    print(keyss)
    thecommand="get {keyss}\r\n".format(keyss=keyss)
    con.send(thecommand.encode('utf-8'))
    # http://stackoverflow.com/questions/2716788/reading-http-server-push-streams-with-python
    # need a readline like
    # f = con.makefile("rb") # converts a socket to a file
    response={}
    while 1:
        (akey,avalue)=parse_value(con)
        # print("got akey",akey,avalue)
        if (akey==None):
            # f.close()
            break
        else:
            response[akey]=avalue
    return response



def parse_value(con,alist):
    # yy=atpic.log.setname(xx,'parse_value')
    line=get_line(con)
    # atpic.log.debug(yy,'line1',line)

    if line==b"END":
        pass
    else:
        (keyword,akey,aflags,abytes)=line.split()
        # atpic.log.debug(yy,'kw',keyword,'akey',akey,'afalags',aflags,'abytes',abytes)
        abytesi=int(abytes)
        datablock=con.recv(abytesi)
        con.recv(2)  # the "\r\n"
        datablock=datablock.decode("utf8")
        akey=akey.decode("utf8")
        alist.append((akey,datablock))
        alist=parse_value(con,alist)
    return alist

def get(con,key):
    """Expects ONE key and returns one bytes string (or None)"""
    # yy=atpic.log.setname(xx,'get')
    thecommand="get {key}\r\n".format(key=key)
    # atpic.log.debug(yy,'get command:',thecommand)
    con.send(thecommand.encode('utf-8'))
    # line=get_line(con)
    # line=get_line(con)

    alist=parse_value(con,[])
    
    return alist

# ====================================
#      deletion commands
# ====================================

def delete(con,key,time=0):
    # yy=atpic.log.setname(xx,'delete')
    thecommand="delete {key} {time}\r\n".format(key=key,time=time)
    # atpic.log.debug(yy,thecommand)
    con.send(thecommand.encode('utf-8'))
    response = get_line(con)
    # atpic.log.debug(yy,'response',response)
    return response

    # print(data)

# ====================================
#      increment/decrement commands
# ====================================
def incrdecr(con,command,key,value=1):
    """
    command is one of 'incr' or 'decr'
    """
    # yy=atpic.log.setname(xx,'incrdecr')
    thecommand="{command} {key} {value}\r\n".format(command=command,key=key,value=value)
    con.send(thecommand.encode('utf-8'))
    line=get_line(con)
    # atpic.log.debug(yy,line)
    if line==b'NOT_FOUND':
        return None
    else:
        return int(line.strip())


def increment(con,key,value=1):
    return incrdecr(con,"incr",key,value)

def decrement(con,key,value=1):
    return incrdecr(con,"decr",key,value)

if __name__ == "__main__":
    # logging.basicConfig(level=logging.WARN)
    con=connect()
    set(con,"key1","value1")
    print("key1",get(con,"key1"))
    delete(con,"key1")
    print("key1",get(con,"key1"))


    set(con,"counter",0)
    counter=get(con,"counter")
    print("x counter=",counter)
    counter=increment(con,"counter")
    print("counter=",counter)
    counter=get(con,"counter")
    print("counter=",counter)
    set(con,"counter2",0)
    counter2=increment(con,"counter2")
    print("counter2=",counter2)

    start = time.clock()
    for i in range(1,10000):
        counter2=increment(con,"counter2")
    elapsed = time.clock() - start
    print("counter2=",counter2)
    print(elapsed)

    for j in range(0,5):
        start = time.clock()
        for i in range(1,10000):
            alex=set(con,"alexété","madonClara cet été là")
        elapsed = time.clock() - start
        alex=get(con,"alexété")
        # print("alex=",alex)
        print(elapsed)

    con.close()
