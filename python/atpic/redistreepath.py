#!/usr/bin/python3
"""
======even better
use hashes:
advantages:
1) fast delete
2) gain 33% on pic alls as make 2 calls (path+pic) instead of 3 calls (user+path+pic), and no version check
store the whole gallery tree for one user in a hash:
when a change is made delete it.
populate it when needed.

(t_ = tree)
t_alex:/:(mount,uid,gid,perm,ctime,mtime) or DEAD
t_alex:/france:(mount,uid,gid,perm,ctime,mtime)
t_alex:/france/paris:(mount,uid,gid,perm,ctime,mtime)

then one big hash for all the pics in one gallery:
g_999:dama.jpg:(mount,uid,pid,ctime,mtime) (gid id stored in the key)

# and some DNS oriented data:

t_alex:ip:10.66.66.78
t_alex:mount:/sda1
t_alex:id:1
"""

# import logging
import atpic.log
import atpic.dispatcher
import atpic.redis_pie


xx=atpic.log.setmod("INFO","redistreepath")



# uname + pathname oriented

def serialize_path(mount,uid,gid,perm,ctime,mtime):
    serial_list=[mount,uid,gid,perm,ctime,mtime]
    return b'|'.join(serial_list)

def unserialize_path(chunk):
    return tuple(chunk.split(b'|'))

def unamepath_set(db,uname,path,mount,uid,gid,perm,ctime,mtime):
    key=b't_'+uname
    field=path
    value=serialize_path(mount,uid,gid,perm,ctime,mtime)
    db._hset(key, field, value)
    pass

def unamepath_get(db,uname,path):
    key=b't_'+uname
    field=path
    res=db._hget(key,field)
    return res

def uname_delete(db,uname):
    pass

# gallery gid+picname oriented
def gidfname_set(db,gid,fname,mount,uid,pid,ctime,mtime):
    pass

def gidfname_get(db,gid,fname):
    pass

def gid_delete(db,gid):
    pass

if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    rediscon=atpic.dispatcher.get_rediscon()
