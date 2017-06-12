#!/usr/bin/python3
# some utilities to a wider use of bytes
# import logging
# import atpic.log



# xx=atpic.log.setmod("INFO","mybytes")

def bytes2int(i):
    return int(i)

def int2bytes(i):
    """
    Converts a number to a bytes string
    """
    return str(i).encode('utf8')

def bytes2float(i):
    if i==b'': # empty
        i=b'0.0'
    if i == None:
        i=b'0.0'
    return float(i)

def float2bytes(i,fmt='%0.30f'):
    # s=i.__repr__()
    # s=fmt % i
    s=str(i)
    return s.encode('utf8')

def list2bytes(alist):
    newlist=[]
    for a in alist:
        newlist.append(a.encode('utf8'))
    return newlist

def list2string(alist):
    newlist=[]
    for a in alist:
        newlist.append(a.decode('utf8'))
    return newlist


def env2bytes(environ):
    # make all keys and values bytes
    newenv={}
    for key in environ.keys():
        nkey=key.encode('utf8')

        if type(environ[key])==str:
            newenv[nkey]=environ[key].encode('utf8')
        else:
            newenv[nkey]=environ[key]
    del environ

    return newenv

def env2string(environ):
    # make all keys and values strings (from bytes)
    newenv={}
    for key in environ.keys():
        nkey=key.decode('utf8')

        if type(environ[key])==bytes:
            newenv[nkey]=environ[key].decode('utf8')
        else:
            newenv[nkey]=environ[key]
    del environ

    return newenv

def headers2string(headers):
    newheaders=[]
    for (key,val) in headers:
        newheaders.append((key.decode('utf8'),val.decode('utf8')))
    return newheaders


if __name__ == "__main__":
    a=float2bytes(0.99876984384389348948387438348348)
    print(a)
