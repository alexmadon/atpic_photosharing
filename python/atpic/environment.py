#!/usr/bin/python3
import re

import urllib.parse
import traceback
from http import cookies

import atpic.log

xx=atpic.log.setmod("INFO","environment")

def get_cookies(environ):
    # gets the list of keys
    cookieheader=environ.get(b"HTTP_COOKIE",b"")
    C = cookies.SimpleCookie()
    C.load(cookieheader.decode('utf8'))
    mykeys=[]
    for key in C.keys():
        mykeys.append(key.encode('utf8'))
    return mykeys

def get_cookie(environ,name):
    # return a simple cookie value
    cookieheader=environ.get(b"HTTP_COOKIE",b"")
    C = cookies.SimpleCookie()
    C.load(cookieheader.decode('utf8'))
    lang=C.get(name.decode('utf8'))
    try:
        return lang.value.encode('utf8')
    except:
        return b''

def get_map(environ,key):
    # look for a 'map' variable in the environ
    # if exists, search for a mapping for the key
    yy=atpic.log.setname(xx,'get_map')
    newkey=key
    try:
        themap=get_qs_key_basic(environ,b'map',b'')
        splitted=themap.split(b';')
        for key2key in splitted:
            [fkey,newfkey]=key2key.split(b',')
            if fkey==key:
                newkey=newfkey
    except:
        # atpic.log.debug(yy,traceback.format_exc())
        atpic.log.debug(yy,'could not find a map')
    return newkey

def get_qs_redirect(environ,defval):
    # used for redirect
    yy=atpic.log.setname(xx,'get_qs_redirect')
    theval=defval
    try:
        query_string=environ[b'QUERY_STRING']
        atpic.log.debug(yy,'searching redirect in:',defval,query_string)
        match=re.match(b'.*redirect=(.+)$',query_string)
        if match:
            theval=match.group(1)
    except:
        atpic.log.debug(yy,traceback.format_exc())
        pass
    atpic.log.debug(yy,'will return',theval)
    return theval


def get_qs_key(environ,key,defval):
    newkey=get_map(environ,key)
    thevalue=get_qs_key_basic(environ,newkey,defval)
    return thevalue
    # mapping=get_qs_key_basic(environ,key,b'')

def get_qs_key_basic(environ,key,defval):
    """
    parses the query_string in 'environ' and sets it to default value or the first element
    """
    yy=atpic.log.setname(xx,'get_qs_basic')
    atpic.log.debug(yy,'input=',environ,key,defval)
    theval=defval
    try:
        query_string=environ[b'QUERY_STRING']
        atpic.log.debug(yy,'ask for',key,defval,query_string)
        qssplitted=query_string.split(b'&')
        for pair in qssplitted:
            pair_splitted=pair.split(b'=')
            if pair_splitted[0]==key:
                theval=pair_splitted[1]
                break
        atpic.log.debug(yy,'before replace',theval)
        theval=theval.replace(b'+',b' ')
        atpic.log.debug(yy,'before unquote',theval)
        theval=urllib.parse.unquote_to_bytes(theval)
    except:
        atpic.log.debug(yy,traceback.format_exc())
        pass
    # adic=urllib.parse.parse_qs(query_string) # /usr/lib/python3/urllib/parse.py

    # if key in adic:
    #    astartlist=adic[key]
    #    if len(astartlist)>0:
    #        theval=astartlist[0] # we take only the first!

    atpic.log.debug(yy,'will return',theval)
    return theval






def get_qs_list(environ):
    """
    parses the query_string in 'environ' and returns a list of duplet (name,value)
    """
    yy=atpic.log.setname(xx,'get_qs_list')
    atpic.log.debug(yy,'input=',environ)
    out=[]
    try:
        query_string=environ[b'QUERY_STRING']
        atpic.log.debug(yy,'ask for',query_string)
        qssplitted=query_string.split(b'&')
        for pair in qssplitted:
            pair_splitted=pair.split(b'=')
            thename=pair_splitted[0]
            theval=pair_splitted[1]
        
            atpic.log.debug(yy,'before replace',theval)
            theval=theval.replace(b'+',b' ')
            atpic.log.debug(yy,'before unquote',theval)
            theval=urllib.parse.unquote_to_bytes(theval)
            out.append((thename,theval))
    except:
        atpic.log.debug(yy,traceback.format_exc())
        pass
    # adic=urllib.parse.parse_qs(query_string) # /usr/lib/python3/urllib/parse.py
    atpic.log.debug(yy,'output=',out)
    return out


if __name__ == "__main__":
    redir=get_qs_redirect({b'QUERY_STRING':b'aaaa&redirect=http://host.com/ddd?aa=bb'},b'')
    print(redir)
