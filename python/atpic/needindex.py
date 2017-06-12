#!/usr/bin/python3

import atpic.redis_index_client

import atpic.log

"""
checks if one need to index
after HTTP
of fuse

can exppect:
uwsgi messages
fs zmq messages
asyncdone zmq messages
"""


xx=atpic.log.setmod("INFO","needindex")

def blank():
    """
    initilize decision vector
    """
    pid=b''
    gid=b''
    uid=b''
    needindex=False
    return (needindex,uid,gid,pid)

def process_needindex(needindex,uid,gid,pid,idxsocket):
    """
    Function that actually sends the message to ZMQ index frontend
    Difficult to UNIT test
    """
    yy=atpic.log.setname(xx,'process_needindex')
    atpic.log.debug(yy,'input=',(needindex,uid,gid,pid,idxsocket))
    if needindex:
        atpic.log.debug(yy,'we do need to index, sending to zmq redis frontend')
        tosend=b'|'.join((uid,gid,pid))
        atpic.log.debug(yy,'sending tosend=',tosend)
        atpic.zmq_index_client.send(idxsocket,tosend)
    else:
        atpic.log.debug(yy,'nothing to send')


# ===================================================
#               asyncdone functions
# ===================================================

def index_asyncdone(message,idxsocket):
    # socket needed to unit test
    yy=atpic.log.setname(xx,'index_asyncdone')
    atpic.log.debug(yy,'input=',(message,idxsocket))
    (needindex,(uid,gid,pid))=check_asyncdone(message)
    atpic.log.debug(yy,'needindex=',(needindex,(uid,gid,pid)))
    process_needindex(needindex,uid,gid,pid,idxsocket)


def check_asyncdone(message):
    """
    we parse the asyncdone message to extract uid, pid
    Easy to uinit test
    """
    # example input:
    #  b'T|1419582387.0531254|1|2737234|a|n/2014/12/26/08/26/1_2737234_0.jpg'

    yy=atpic.log.setname(xx,'check_asyncdone')
    atpic.log.debug(yy,'input=',message)
    splitted=message.split(b'|')
    alen=len(splitted)
    atpic.log.debug(yy,'alen',alen)
    (needindex,uid,gid,pid)=blank()
    if alen==6 and splitted[0]==b'T':
        uid=splitted[2]
        pid=splitted[3]
        needindex=True
    atpic.log.debug(yy,'output=',(needindex,(uid,gid,pid)))
    return (needindex,(uid,gid,pid))

# ===================================================
#               filesystem functions
# ===================================================
def needindexfs(command,path,result):
    """
    can be unit tested.
    """
    yy=atpic.log.setname(xx,'needindexfs')
    atpic.log.debug(yy,'input=',(command,path,result))
    (needindex,uid,gid,pid)=blank()
    if len(result)>0:
        needindex=True
        arow=result[0]
        if command in [b'mkdir',b'rmdir']:
            uid=arow[b'_user']
            gid=arow[b'id']
        elif command==b'rename':
            if b'_gallery' in arow.keys():
                uid=arow[b'_user']
                gid=arow[b'_gallery']
                pid=arow[b'id']
            else:
                uid=arow[b'_user']
                gid=arow[b'id']
        elif command==b'unlink':
            uid=arow[b'_user']
            gid=arow[b'_gallery']
            pid=arow[b'id']
            
      
    atpic.log.debug(yy,'output=',(needindex,(uid,gid,pid)))
    return (needindex,(uid,gid,pid))

def indexfs_basic(command,path,result,idxsocket):
    yy=atpic.log.setname(xx,'indexfs_basic')
    (needindex,(uid,gid,pid))=needindexfs(command,path,result)
    process_needindex(needindex,uid,gid,pid,idxsocket)

def indexfs(command,path,result,idxsocket):
    """
    idxsocket: a zmq socket thin wrapper in front of redis
    """
    yy=atpic.log.setname(xx,'indexfs')
    response=b''
    try:
        response=indexfs_basic(command,path,result,idxsocket)
    except:
        atpic.log.error(yy,traceback.format_exc())


def needindexweb(hxplo,pxplo,actions):
    # can be unit tested
    (needindex,uid,gid,pid)=blank()
    # now consider all cases
    return (needindex,(uid,gid,pid))

def indexweb(rediscon,hxplo,pxplo,actions):
    yy=atpic.log.setname(xx,'indexweb')
    atpic.log.debug(yy,'input=',(rediscon,hxplo,pxplo,actions))
    # 
    (needindex,(uid,gid,pid))=needindexweb(hxplo,pxplo,actions)
    if needindex:
        atpic.log.debug(yy,'we need to index, sending to redis')
        # send to redis
        atpic.redis_index_client.put_in_queue(rediscon,uid,gid,pid)
    else:
        atpic.log.debug(yy,'no need to index')

# ===================================================
#               web index functions
# ===================================================
# we connect directly to redis as web has alreayd one connection
 
if __name__ == "__main__":
    print('hi')
