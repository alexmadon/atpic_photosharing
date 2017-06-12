#!/usr/bin/python3
# a fast server that replies to a fuse client:
# advantage of this: loose coupling
# we can choose the number of zmq servers to run, and do not have to open a pg socket for each fuse thread, or just use one (easy to program) here we can size exactky as we want, easily.
# http://zeromq.org/blog:multithreading-magic
# we have two engines talking to each other: fuse server and path server (redis+sql)
# note that socket can be Unix Domain
# this zmq server provides a simple service.
# we do pooling here
# a very simple pooling is necessary for fuse: 
# just open as many zmq context to unix domain as we have thread names

# each zmq server can be very specialized:
# e.g a XSLT service can parse the XSL only once

import errno
import os
import time
import traceback
import zmq


import atpic.forgesql
import atpic.log
import atpic.redis_pie
import atpic.libpqalex
import atpic.needindex
import atpic.pathbased
import atpic.processinfiles
import atpic.mybytes
import atpic.zmq_index_client


xx=atpic.log.setmod("INFO","zmq_fs_server")

# First slash is irrelevant:
# /alexmadon/italia2006
# /alexalexmadon/italia2006/firenze
# alexmadon/italia2006/firenze
"""
atpic.forgesql.forge_dirlist(path)
atpic.forgesql.forge_piclist(path)
atpic.forgesql.forge_picpathstore(path)
"""
# alexmadon/italia2006/firenze/immagine_292.jpg

# protocol is simple:
# first letter is the type of request:
# R: readdir (returns a list of children)
# e.g R/alex/europe/paris
# S: retruns the file on disk the virtual image path maps to:
# e.g: S/alex/europe/paris/eiffel_tower.jpg -> /a/fastdir/1/0/1234/399999.jpg 
# (stats are then retrieved from disk)
# for the moment, we lie for directories

# serverside, a readdir, retrieves from SQL but also persists temporarly in Redis
# during 1 sec, as a listdir usually is followed byt a stat on each entry

#  a stat (S) is 1st tried in redis, if not we hit the DB


# for stats of directories:
# could send a r_x only on virtual directories
# rwx on real ones
# not exist on not exist
# root should always exist
"""
Path utilities:
converts path to gallery
gallery to path, etc...


cache is stored in two classes:
1) the directory tree for one user in one redis hash
2) for each gallery, one redis hash storing the pictures details
(lists are not cached and are gotten from SQL (faster?)) 


NEW:
we have no path anymore: we use SQL regex for list of dirs

select id,_path from _user_gallery where _user=1;
select id,_path from _user_gallery where _user=1 and _path ~ 'ita.*';
select id,_path from _user_gallery where _user=1 and _path ~ '^ita[^/]+$';

"""

def serror(ecode):
    """
    Returns the byte representation of an error code (package errno)
    """
    return atpic.mybytes.int2bytes(ecode)


# =========================================
#      operations requiring reindexing
# =========================================

def process_mkdir(path,db,idxsocket):
    yy=atpic.log.setname(xx,'process_mkdir')
    response=b'0'
    try:
        (query,query_args)=atpic.forgesql.forge_mkdir(path)
        atpic.log.debug(yy,'(query,query_args)=',(query,query_args))
        ps=atpic.libpqalex.pq_prepare(db,b'',query)
        result=atpic.libpqalex.pq_exec_prepared(db,b'',query_args)
        result=atpic.libpqalex.process_result(result)
        atpic.needindex.indexfs('mkdir',path,result,idxsocket)
        if len(result)>0:
            response=b'0'
        else:
            response=serror(errno.EACCES)
    except:
        atpic.log.error(yy,traceback.format_exc())
        response=serror(errno.EACCES)

    atpic.log.debug(yy,'response=',response)
    return response

def process_unlink(path,db,idxsocket):
    yy=atpic.log.setname(xx,'process_unlink')
    try:
        (query,query_args)=atpic.forgesql.forge_unlink(path)
        atpic.log.debug(yy,'(query,query_args)=',(query,query_args))
        ps=atpic.libpqalex.pq_prepare(db,b'',query)
        result=atpic.libpqalex.pq_exec_prepared(db,b'',query_args)
        result=atpic.libpqalex.process_result(result)
        atpic.needindex.indexfs('unlink',path,result,idxsocket)
        if len(result)>0:
            response=b'0'
        else:
            response=serror(errno.EACCES)

    except:
        atpic.log.error(yy,traceback.format_exc())
        response=serror(errno.EACCES)

    atpic.log.debug(yy,'response=',response)
    return response




def process_rmdir(path,db,idxsocket):
    yy=atpic.log.setname(xx,'process_rmdir')
    try:
        (query,query_args)=atpic.forgesql.forge_rmdir(path)
        atpic.log.debug(yy,'(query,query_args)=',(query,query_args))
        ps=atpic.libpqalex.pq_prepare(db,b'',query)
        result=atpic.libpqalex.pq_exec_prepared(db,b'',query_args)
        result=atpic.libpqalex.process_result(result)
        atpic.needindex.indexfs('rmdir',path,result,idxsocket)

        if len(result)>0:
            response=b'0'
        else:
            response=serror(errno.EACCES)

    except:
        atpic.log.error(yy,traceback.format_exc())
        response=serror(errno.EACCES)

    atpic.log.debug(yy,'response=',response)
    return response




def process_rename(path,db,idxsocket):
    # path is the virtual path old+NULL+new
    # can do files and directories
    # see 
    # http://linux.die.net/man/2/rename
    # need pkg manpages-dev
    # for errors
    # http://fuse.sourceforge.net/doxygen/fusexmp_8c.html
    yy=atpic.log.setname(xx,'process_rename')
    atpic.log.debug(yy,'input path=',path)
    response=b'0' # success
    try:
        # path is in fact a serialization of 'old+NULL+new'
        (path_old,path_new)=path.split(b'\0')
        atpic.log.debug(yy,'old',path_old,'new',path_new)

        (ptype_old,ptuple_old)=atpic.pathbased.path_split(path_old)
        atpic.log.debug(yy,'got path_old details:',(ptype_old,ptuple_old))

        (ptype_new,ptuple_new)=atpic.pathbased.path_split(path_new)
        atpic.log.debug(yy,'got path_new details:',(ptype_new,ptuple_new))

        if ((ptype_old==b'g' and ptype_new==b'g') or (ptype_old==b'p' and ptype_new==b'p')):
            atpic.log.debug(yy,'rename a gallery or pic...')
            atpic.log.debug(yy,'checking no cross-user renames...')
            if ptuple_new[0]!=ptuple_old[0]: # check if usernames are different
                atpic.log.info(yy,'cross-user renames NOT allowed',path_old,path_new)
                response=serror(errno.EFAULT)
            else:
                atpic.log.debug(yy,'not a cross-user renames, continuing...')
                if (ptype_old==b'g' and ptype_new==b'g'):
                    atpic.log.debug(yy,'rename a gallery...')
                    # can rename a gallery only if old is a real gallery and new does not exist (virtual?)

                    (query,query_args)=atpic.forgesql.forge_rename_gallery(path_old,path_new)
 
                elif (ptype_old==b'p' and ptype_new==b'p'):
                    atpic.log.debug(yy,'rename a picture...')
                    # can rename a pic if old exist and new gallery is real and filename does not exist
                    # could rely on unique key on files
                    # differs from man 2 rename
                    (query,query_args)=atpic.forgesql.forge_rename_picture(path_old,path_new)

                ps=atpic.libpqalex.pq_prepare(db,b'',query)
                result=atpic.libpqalex.pq_exec_prepared(db,b'',query_args)
                result=atpic.libpqalex.process_result(result)
                atpic.needindex.indexfs('rename',path,result,idxsocket)
                atpic.log.debug(yy,"result from sql",result) 
                if len(result)>0:
                    response=b'0'
                else:
                    response=serror(errno.EACCES)

        else:
            atpic.log.info(yy,'rename prohibited...',path_old,path_new) # u:user and s:slash are prohibited
            response=serror(errno.EFAULT)

        # if ptype==b'u' or ptype==b'g' or ptype==b's': # user, gallery, or 'slash'
        # dirtype=zmq_send(b'dirtype',path)
        # elif ptype==b'p':
        
    except:
        atpic.log.error(yy,traceback.format_exc())
        response=serror(errno.EFAULT) # generic error?
    return response



# =========================================
#
# =========================================

def get_dirlist(path,db):
    yy=atpic.log.setname(xx,'get_dirlist')
    
    try:
        (query,query_args)=atpic.forgesql.forge_dirlist(path)
        atpic.log.debug(yy,'(query,query_args)=',(query,query_args))
        ps=atpic.libpqalex.pq_prepare(db,b'',query)
        result=atpic.libpqalex.pq_exec_prepared(db,b'',query_args)
        result=atpic.libpqalex.process_result(result)
    except:
        atpic.log.error(yy,traceback.format_exc())
    # atpic.libpqalex.close(db)
    dirlist=[]
    for ahash in result:
        dirlist.append(ahash[b'dirname'])
    atpic.log.debug(yy,'output=',dirlist)
    return dirlist


def get_piclist(path,db):
    yy=atpic.log.setname(xx,'get_piclist')
    
    try:
        (query,query_args)=atpic.forgesql.forge_piclist(path)
        atpic.log.debug(yy,'(query,query_args)=',(query,query_args))
        ps=atpic.libpqalex.pq_prepare(db,b'',query)
        result=atpic.libpqalex.pq_exec_prepared(db,b'',query_args)
        result=atpic.libpqalex.process_result(result)
    except:
        atpic.log.error(yy,traceback.format_exc())
    
    piclist=[]
    picstore=[]
    for ahash in result:
        atpic.log.debug('yy','ahash=',ahash)
        piclist.append(ahash[b'originalname'])
        picstore.append(ahash[b'fullpathstore'])
    atpic.log.debug(yy,'output=',(piclist,picstore))
    return (piclist,picstore)



def process_readdir(path,db):
    yy=atpic.log.setname(xx,'process_readdir')
    res=[]
    res=res+get_dirlist(path,db)
    (piclist,picstore)=get_piclist(path,db)
    res=res+piclist
    # you can save to redis for faster performance
    response=b'\n'.join(res)
    return response

def process_dirtype(path,db):
    yy=atpic.log.setname(xx,'process_dirtype')
    atpic.log.debug(yy,"Input=", path)
    
    try:
        (query,query_args)=atpic.forgesql.forge_dirtype(path)
        ps=atpic.libpqalex.pq_prepare(db,b'',query)
        result=atpic.libpqalex.pq_exec_prepared(db,b'',query_args)
        result=atpic.libpqalex.process_result(result)
        atpic.log.debug(yy,"result=", result)
        if len(result)>0:
            response=result[0][b'res']
        else:
            response=b''
    except:
        atpic.log.error(yy,traceback.format_exc())
        response=b''
    return response



def process_stat(path,db):
    yy=atpic.log.setname(xx,'process_stat')
    # returns a true pathstore from a virtual path
    # (query,query_args)=atpic.forgesql.forge_picpathstore(path)
    # this pathstore can then be used to get the fstats on-disk
    # this is SQL only at the moment, no cache
    atpic.log.debug(yy,"Input=", path)
    
    try:
        (query,query_args)=atpic.forgesql.forge_picpathstore(path)
        ps=atpic.libpqalex.pq_prepare(db,b'',query)
        result=atpic.libpqalex.pq_exec_prepared(db,b'',query_args)
        result=atpic.libpqalex.process_result(result)
        atpic.log.debug(yy,"result=", result)
        if len(result)>0:
            response=result[0][b'_fullpathstore']
        else:
            response=b''
    except:
        atpic.log.error(yy,traceback.format_exc())
        response=b''
    return response





def process_createfile(path,db):
    yy=atpic.log.setname(xx,'process_createfile')
    # returns a true pathstore from a virtual path
    # (query,query_args)=atpic.forgesql.forge_picpathstore(path)
    # this pathstore can then be used to get the fstats on-disk
    # this is SQL only at the moment, no cache
    atpic.log.debug(yy,"Input=", path)
    
    try:
        atpic.log.debug('try upsert')
        (query,query_args)=atpic.forgesql.forge_fuseupsert(path)
        ps=atpic.libpqalex.pq_prepare(db,b'',query)
        result=atpic.libpqalex.pq_exec_prepared(db,b'',query_args)
        result=atpic.libpqalex.process_result(result)
        atpic.log.debug(yy,"result from sql",result) 
        if len(result)>0:
                response=b'/'+result[0][b'_partition']+b'/'+result[0][b'_pathstore']
        else:
            response=b''
    except:
        atpic.log.error(yy,traceback.format_exc())
        response=b''
    return response




 
def process_processfile(path,db):
    # path is the virtual path
    # May need to refuse at first if file name does not oberty restrictions
    yy=atpic.log.setname(xx,'process_processfile')
    atpic.log.debug(yy,'input path=',path)

    # reuse samequery as in stats
    (query,query_args)=atpic.forgesql.forge_picpathstore(path)
    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    result=atpic.libpqalex.pq_exec_prepared(db,b'',query_args)
    result=atpic.libpqalex.process_result(result)
    atpic.log.debug(yy,"result=", result)
    res=result[0]
    afile=res[b'_fullpathstore']
    partition=res[b'_partition']
    uid=res[b'_user']
    original_name=res[b'_originalname']
    gid=res[b'_gallery']
    pid=res[b'id']
    pathstore=res[b'_pathstore']
    atpic.log.debug(yy,'pathstore',pathstore)
    if pathstore.startswith(b'atpicfs_'):
        atpic.log.debug(yy,'This is a tmp file, that needs to be processed (artefacts)')
        atpic.log.debug(yy,"sending=", (afile,original_name,partition,uid,gid,pid,db))
        atpic.processinfiles.process_onefile(afile,original_name,partition,uid,gid,pid,db)
    else:
        atpic.log.debug(yy,'this is not a new file, no processing needed')
    return b'ok'


# mkdir /alex
# stats /image.jpg
# (split on first space)




def process_request_wrap(request,db,idxsocket):
    # a wrapper that catches exceptions as we don't want to kill the server
    yy=atpic.log.setname(xx,'process_request_wrap')
    response=b''
    try:
        response=process_request(request,db,idxsocket)
    except:
        atpic.log.error(yy,traceback.format_exc())
    return response


def process_request(request,db,idxsocket):
    yy=atpic.log.setname(xx,'process_request')
    atpic.log.debug(yy,"Input=", request)
    atpic.log.info(yy,">>", request)
    # get the first letter
    splitted=request.split(b' ')
    command=splitted[0]
    path=b' '.join(splitted[1:])
    atpic.log.debug(yy,"command=", command,'path=',path)
    if command==b'realpath': # transforms virtualpath to realpath
        response=process_stat(path,db)
    elif command==b'dirtype': # transforms virtualpath to realpath
        response=process_dirtype(path,db)
    elif command==b'readdir':
        response=process_readdir(path,db)
    elif command==b'process':
        response=process_processfile(path,db)
    elif command==b'create':
        response=process_createfile(path,db)
    # now, the operations requiring reindex
    elif command==b'mkdir':
        response=process_mkdir(path,db,idxsocket)
    elif command==b'rmdir':
        response=process_rmdir(path,db,idxsocket)
    elif command==b'rename':
        response=process_rename(path,db,idxsocket)
    elif command==b'unlink':
        response=process_unlink(path,db,idxsocket)
    else:
        atpic.log.debug(yy,"Unknown command",command,"for request",request)
    atpic.log.debug(yy,"will return",response)
    return response



def main_loop():
    yy=atpic.log.setname(xx,'main_loop')


    # run as user www-data
    os.setuid(33)

    # open a socket to redis
    rediscon=atpic.redis_pie.connect_first()
    # open a socket to postgresql
    db=atpic.libpqalex.db_native()
    
    idxsocket=atpic.zmq_index_client.get_socket()

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    atpic.log.info(xx,'starting zmq fs')
    socket.bind("tcp://127.0.0.1:5555")

    while True:
        # Wait for next request from client
        request = socket.recv()
        atpic.log.debug(yy,"Received request: ", request)
        response=process_request_wrap(request,db,idxsocket)
        # Send reply back to client
        socket.send(response)

if __name__ == "__main__":
    print('starting')#
    main_loop()
