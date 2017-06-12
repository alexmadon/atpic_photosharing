#!/usr/bin/python3
import socket
# import logging
# from red.utils import comm
import atpic.redis_pie_comm as comm
from atpic.mybytes import *
import atpic.log
xx=atpic.log.setmod("INFO","redis_pie")


def connect_first():
    """ Sets up a TCP connection to the redis server
    
    The only reliable way to check if there is an active connection
    to the Redis server, is by sending a message (even an empty
    bytearray). If the message doesn't arrive, it means that the
    connection is either damaged or the socket has closed.
    If for example, the server closes the connection, but we still have
    an open socket, we can't detect it otherwise.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect(("localhost", 6379)) # hostname = "localhost", port = 6379
    return sock


def reconnect(sock):
    """
    The only reliable way to check if there is an active connection
    to the Redis server, is by sending a message (even an empty
    bytearray). If the message doesn't arrive, it means that the
    connection is either damaged or the socket has closed.
    If for example, the server closes the connection, but we still have
    an open socket, we can't detect it otherwise.
    """
    yy=atpic.log.setname(xx,'reconnect')
    """
    try:
        sock.send(b'')
    except socket.error:
        atpic.log.debug(yy,'socket lost, reconnecting')
        sock=connect_first()
    """
    return sock


# ======================================================
#
#   data commands
#
# ======================================================

def _del(rsock, key):
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"DEL", [key]))
    return handleResponse(rsock)


def _exists(rsock, key):
    """ Test if the specified key exists.
    
    @return: Integer reply.
    1, if the key exists
    0, otherwise
    
    """
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"EXISTS", [key]))
    return handleResponse(rsock)

def _expire(rsock, key,value):
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"EXPIRE", [key,value]))
    return handleResponse(rsock)

def _incr(rsock, key):
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"INCR", [key]))
    return handleResponse(rsock)

def _incrby(rsock, key):
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"INCRBY", [key,by]))
    return handleResponse(rsock)

def _decr(rsock, key):
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"DECR", [key]))
    return handleResponse(rsock)

def _decrby(rsock, key,by):
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"DECRBY", [key,by]))
    return handleResponse(rsock)

def _set(rsock,key,value):           
    """ Set the string value of a key. If key already holds its 
    value, its overwritten, regardless of its type
    
    @return: Status code reply. 
    Always OK
    """
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"SET", [key,value]))
    return handleResponse(rsock)

def _sadd(rsock,key,value):           
    """ Set the string value of a key. If key already holds its 
    value, its overwritten, regardless of its type
    
    @return: Status code reply. 
    Always OK
    """
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"SADD", [key,value]))
    return handleResponse(rsock)

def _scard(rsock,key):           
    """ Set the string value of a key. If key already holds its 
    value, its overwritten, regardless of its type
    
    @return: Status code reply. 
    Always OK
    """
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"SCARD", [key]))
    return handleResponse(rsock)

def _spop(rsock,key):           
    """ Set the string value of a key. If key already holds its 
    value, its overwritten, regardless of its type
    
    @return: Status code reply. 
    Always OK
    """
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"SPOP", [key]))
    return handleResponse(rsock)


def _sinterstore(rsock,destination,keys):           
    """ Set the string value of a key. If key already holds its 
    value, its overwritten, regardless of its type
    
    @return: Status code reply. 
    Always OK
    """
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"SINTERSTORE", [destination]+keys))
    return handleResponse(rsock)

def _smembers(rsock,aset):           
    """ Set the string value of a key. If key already holds its 
    value, its overwritten, regardless of its type
    
    @return: Status code reply. 
    Always OK
    """
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"SMEMBERS", [aset]))
    return handleResponse(rsock)

def _srem(rsock,aset,key):           
    """ Set the string value of a key. If key already holds its 
    value, its overwritten, regardless of its type
    
    @return: Status code reply. 
    Always OK
    """
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"SREM", [aset,key]))
    return handleResponse(rsock)

def _get(rsock, key):
    """ Get the value of a key. If the key does not exist, the special 
    value nil is returned. 
    
    @return: Bulk reply. 
    The value of key, or None when key does not exist.
    """ 
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"GET", [key]))
    return handleResponse(rsock)

def _keys(rsock, pattern = None):
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"KEYS", [pattern]))
    return handleResponse(rsock)

def _hset(rsock, key, field, value):
    """  Sets the field in the hash stored at key, to value.
    
    @return: Integer reply. 
    1 if field is new and the value was set.
    0 if field already exists in the hash and the value was updated.
    """  
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"HSET", [key, field, value]))
    return handleResponse(rsock)

def _hexists(rsock, key, field): # alex
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"HEXISTS", [key, field,]))
    return handleResponse(rsock)

def _hdel(rsock, key, field): # alex
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"HDEL", [key, field,]))
    return handleResponse(rsock)

def _hget(rsock, key, field):
    """ Returns the value associated with field, in the hash at key.
    
    @return: Bulk reply.
    The value associated with field, or None if field is not present or
    key does not exist
    """ 
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"HGET", [key,field]))
    return handleResponse(rsock)

def _hmset(rsock, key, *field_value):
    """ Sets the specified fields to their respective values in the hash
    stored at key.
    
    @param field_value: Tuple of arguments. field1, value1, field2,
    value2, ...
    @return: Status code reply 
    """        
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"HMSET", [key] + list(field_value)))
    return handleResponse(rsock)

def _hkeys(rsock, key):
    """ Returns all field names in the hash stored at key.
    
    @return: Multi-bulk reply.
    List of fields in the hash, or an empty list when key does not
    exist.
    """
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"HKEYS", [key]))
    return handleResponse(rsock)

def _hgetall(rsock, key):
    """ Returns all fields and values of the hash stored at key
    
    @return: Multi-bulk reply.
    A dictionary of field:value pairs stored at key.
    """
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"HGETALL", [key]))
    # Returns a list
    response = handleResponse(rsock)
    # Which I transform to a dictionary
    dic = {} 
    if isinstance(response, list):
        for i in range(0, len(response), 2):
            dic[response[i]] = response[i+1]
            return dic
    return False

# ======================================================
#
#   admin commands
#
# ======================================================

def select(rsock, index):
    """ Selects the DB which has the specified zero-based
    numeric index.
    
    @return: Status code reply. OK if connection was successful
    """
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"SELECT",[index]))
    return handleResponse(rsock)

def save(rsock):
    """ Synchronously save the dataset to disk.
    """
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"SAVE"))
    return handleResponse(rsock)

def flushdb(rsock):
    """ Remove all keys from the current database.
    
    @return: Status code reply.
    """
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"FLUSHDB"))
    return handleResponse(rsock)

def dbsize(rsock):
    """ Returns the number of keys in the currently selected database
    
    @return: Integer reply            
    """
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"DBSIZE"))
    return handleResponse(rsock)

def _quit(rsock): # redis close
    """ Asks the server to close the connection. The socket closes.
    Subsequent connections will use different sockets.
    
    @return: Status code reply. Always returns OK
    """               
    rsock=reconnect(rsock)
    rsock.sendall(comm.constructMessage(b"QUIT"))
    rsock.close() # close the redis socket
    return "OK"



def handleResponse(rsock):
    """ Handles the response returned from the redis server
    """
    yy=atpic.log.setname(xx,"handleResponse")
    
    out=False
    byte = rsock.recv(1)
    
    # Bulk reply
    if byte == b"$":
        # Construct the first line of reply.
        # It is either -1 or a number, indicating the length(in bytes)
        # of the actual response
        response = comm.getLine(rsock)
        
        # line is still in bytes. I don't even need
        # to decode to ascii, since I will only interpret
        # what i read as an int. The conversion from bytes
        # to int is done automatically in int(line)
        length = int(response)
        if length == -1:
            out=None
        else:
            # We need to read length bytes
            value = rsock.recv(length)
            # consume the 2 remaning bytes(\r\n)
            rsock.recv(2)
            out=value

    # Single line reply
    # Status code
    elif byte == b"+":
        response = comm.getLine(rsock)
        out=response
        
    # Single line reply
    # Error Code
    elif byte == b"-":
        response = comm.getLine(rsock)
        out=response

    # Single line reply
    # Integer Reply
    elif byte == b":":
        response = comm.getLine(rsock)
        out=response

    # Multibulk reply
    elif byte == b"*":
        response = comm.getLine(rsock)
        num_res = int(response)     # number of results
        if num_res != -1:
            results = []
            for i in range(num_res):
                length = int(comm.getLine(rsock)[1:])    # Length of result in bytes
                results.append( rsock.recv(length))
                rsock.recv(2)                            # Consume the \r\n
            out=results
        else:
            out=None
    atpic.log.debug(yy,'will return',out)
    return out



if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)

    rsock = connect_first()


    akey=_get(rsock,b"key")
    print(b"akey",akey)

    _sadd(rsock,b'myset',b'one')
    _sadd(rsock,b'myset',b'two')
    b=_smembers(rsock,b'myset')
    print(b)
    _sadd(rsock,b'myset2',b'one')
    c=_sinterstore(rsock,b'myset3',[b'myset',b'myset2'])
    print(c)
    d=_smembers(rsock,b'myset3')
    print(d)
    _sinterstore(rsock,b'myset4',[b'myset'])
    e=_smembers(rsock,b'myset4')
    print(e)
    # server.select(rsock,b'5')

    # simple key-value
    _set(rsock,b"key",b"value")
    akey=_get(rsock,b"key")
    print(b"akey",akey)

    
    # utf8
    _set(rsock,"Clara cet été".encode('utf8'),"là".encode('utf8'))
    value=_get(rsock,"Clara cet été".encode('utf8'))
    print('utf8',value)


    _hset(rsock,b"word",b"field",b"value")
    _hset(rsock,b"word",b"fielr",b"value")
    a=_hget(rsock,b"word",b"field")
    print(a)
    a=_hgetall(rsock,b"word")
    print(a)

    a=_hexists(rsock,b"word",b"field")
    print(a)
    a=_hdel(rsock,b"word",b"field")
    print(a)
    a=_hexists(rsock,b"word",b"field")
    print(a)

    a=_exists(rsock,b"word")
    print(a)
    a=_del(rsock,b"word")
    print(a)
    a=_exists(rsock,b"word")
    print(a)

