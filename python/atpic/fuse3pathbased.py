#!/usr/bin/python3
# id based filesystem
"""
we import our own fuse * and ctypes *
this is a *read-write* file system
(idbased is read only)

should be used in ftp.

We *prohibit* directory manipulation (mkdir, mv, rm).
Directory manipulation should be done using the web API.

A directory /x/y/z will only be seen if there is a gallery with path /x/y

We do not use redis or SQL directly: we interface with a zmq service
to get data we either do a zmq call
or do a filesystem call (stats, write, etc..)

reason: as fuse is multithreaded, it's hard to program
advantage: zmq is easier to test, just write client


This fuse server is a ZMQ zmq_fs client:
syntax:
=======
S/path (to get the stats)
P/pathtofile (to send processing)
R/path (to readdir)



Limitation: name of path should not contain the dot

Problems: 
locks (performance?)
cache invalidation:
hint a content url is fixed, not update inplace, so at worst, you list a file that cannot be read.

Based on observation: make it simple:
we lie on directories
a 'ls' trigger a SQL list + a 1 second cache of stats on files
a stat of file triggers a call to the cache or a SQL:
cache stores a map filename2pasthstore, actual stats are read from filesystem
a mv on file delete the cache if any and update sql
a delete on file delete the cache and delete in sql
a mv or delete of dir is not supported
"""
import os
from ctypes import *
from ctypes.util import find_library
import errno
import random
import stat
import string
import traceback
from multiprocessing import Lock
import threading
import zmq
import tempfile

import atpic.log
import atpic.pathbased
from atpic.mybytes import *


from atpic.fuse3at import *

xx=atpic.log.setmod("INFO","fuse3pathbased")

# bug in vsftpd:
# https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=735191#10
# http://stackoverflow.com/questions/22420177/500-oops-vsftpd-refusing-to-run-with-writable-root-inside-chroot-login-faile
# 500 OOPS: vsftpd: refusing to run with writable root inside chroot()

# =============================================================
# socketb pool
# =============================================================
# zmq requires a context that gives a socket
# we define a 'pool', a hash of contexts where the key is the thread name

socket_pool={}

file_descriptors={} # a hashmap of FD (integers) to real path names

def zmq_send(command,path):
    yy=atpic.log.setname(xx,'zmq_send')
    atpic.log.debug(yy,'input=',(command,path))
    socket=get_socket()
    atpic.log.debug(yy,'socket=',socket)
    socket.send(command+b' '+path) # send
    response=socket.recv()
    atpic.log.debug(yy,'response=',response)
    return response

def get_socket():
    yy=atpic.log.setname(xx,'get_socket')
    mytid=threading.current_thread()
    key=mytid.name
    if key in socket_pool:
        atpic.log.debug(yy,'we know about key',key)
        socket =socket_pool[key]
    else:
        atpic.log.debug(yy,'need to create a new socket')
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect ("tcp://localhost:5555")
        atpic.log.debug(yy,'save it into the pool')
        socket_pool[key]=socket
    atpic.log.debug(yy,'output:',socket)
    return socket


# =============================================================
#
#  super simple, easy to unit test
#
# =============================================================


def my_readdir(path,offset=0):
    """
    returns a list of files under path, easy to unit test
    """
    # at the user list level should never be called
    # you could have 10000s of users under / !
    yy=atpic.log.setname(xx,'my_readdir')
    atpic.log.debug(yy,'input=',path,offset)
    filelist=[b'.',b'..']
    if path==b'/':
        filelist=[b'.',b'..',b'cannot_be_listed']
    else:
        # call a zmq service
        socket=get_socket()
        atpic.log.debug(yy,'socket=',socket)
        socket.send(b'readdir '+path) # send
        filelist_string=socket.recv()
        atpic.log.debug(yy,'filelist_string=',filelist_string)
        if filelist_string==b'':
            filelist=[]
        else:
            filelist=filelist_string.split(b'\n')
        filelist=[b'.',b'..']+filelist 
    atpic.log.debug(yy,'output=',filelist)
    return filelist

def my_getattr(path):
    """
    returns stats for path, easy to unit test
    """
    yy=atpic.log.setname(xx,'my_getattr_direct')
    atpic.log.debug(yy,'input:',path)
    (ptype,ptuple)=atpic.pathbased.path_split(path)
    atpic.log.debug(yy,'got path details:',(ptype,ptuple))
    if ptype==b'u' or ptype==b'g' or ptype==b's': # user, gallery, or 'slash'
        atpic.log.debug(yy,'ISDIR: lets get some info......')
        dirtype=zmq_send(b'dirtype',path)
        atpic.log.debug(yy,'dirtype=',dirtype)

        uid=33 # 33
        gid=33 # 33
        size=1
        nlink=1
        mtime=0
        atime=mtime
        ctime=mtime
        if dirtype==b'isreal':
            mode=stat.S_IFDIR | 0o777 # rwx
        elif dirtype==b'isvirtual':
            mode=stat.S_IFDIR | 0o555 # r_x
        elif dirtype==b'missingroot': # should never happen!
            atpic.log.info(yy,'missing root for',path)
            mode=stat.S_IFDIR | 0o555 # r_x
        else:
            atpic.log.debug(yy,'directory does not exist')
            raise
    elif ptype==b'p':
        atpic.log.debug(yy,'ISFILE......')
        uid=33
        gid=33
        nlink=1
        mode=stat.S_IFREG | 0o777 #  this is a file
        mtime=0
        atime=mtime
        ctime=mtime
        size=0 # BAD!
        # try:
        storepath=zmq_send(b'realpath',path)
        sstat=os.stat(storepath)
        size=sstat.st_size
        # except:
        #    atpic.log.debug(yy,'could not find the file!',storepath)
        #    size=0
            
    # we need integers not bytes:
    atime=bytes2int(atime)
    mtime=bytes2int(mtime)
    ctime=bytes2int(ctime)

    atpic.log.debug(yy,'will return:',uid,gid,size,nlink,mode,atime,mtime,ctime)
    return (uid,gid,size,nlink,mode,atime,mtime,ctime)



# =============================================================
#
#  my prototypes
#
# =============================================================

def myaccess(path, amode):
    yy=atpic.log.setname(xx,'myaccess')
    atpic.log.debug(yy,"ENTERING myaccess on ",path,"mode",amode)
    return 0


def mychmod(path,mode):
    yy=atpic.log.setname(xx,'mychmod')
    atpic.log.debug(yy,"ENTERING mychmod path=",path,"mode",mode)
    return 0
    
def mychown(path, uid, gid):
    yy=atpic.log.setname(xx,'mychown')
    atpic.log.debug(yy,"ENTERING mychown path=",path,"uid=",uid,"gid",gid)
    return 0

def myflush(path, fh):
    # Purpose: This function is called to let the file system clean up any data buffers and to pass any errors in the process of closing a file to the user application. 
    yy=atpic.log.setname(xx,'myflush')
    atpic.log.debug(yy,"ENTERING myflush ",path, fh)
    return 0

def myfsync(path, datasync, fh):
    yy=atpic.log.setname(xx,'myfsync')
    atpic.log.debug(yy,"ENTERING myfsync path=",path, datasync, fh)
    return 0

def myfsyncdir(path, datasync, fh):
    yy=atpic.log.setname(xx,'myfsyncdir')
    atpic.log.debug(yy,"ENTERING myfsyncdir",path, datasync, fh)
    return 0

def mycreate(path, mode, fip):
    # Create and open a file
    # related to myopen
    yy=atpic.log.setname(xx,'mycreate')
    atpic.log.debug(yy,"ENTERING mycreate", path, mode, fip)

    # create it
    storepath=zmq_send(b'create',path) # createfile
    # os.mknod(storepath)
    atpic.log.debug(yy,"have created",path,'as',storepath)

    # open it
    myflags=fip.contents.flags
    fd=os.open(storepath,myflags) 
    atpic.log.debug(yy,'fd',fd)
    fip.contents.fh = fd
    file_descriptors[fd]=storepath
    atpic.log.debug(yy,'returning success')
    return 0 # success
 
def mydestroy(path):
    yy=atpic.log.setname(xx,'mydestroy')
    atpic.log.debug(yy,"ENTERING mydestroy", path)
    return 0

def mygetattr(path,buf):
    yy=atpic.log.setname(xx,'mygetattr')
    # difficult to unit test
    # need a dispatcher to some (few) known cases
    atpic.log.debug(yy,"ENTERING mygetattr on path=",path,"buf=",buf)

    memset(buf, 0, sizeof(c_stat))
    try:
        st = buf.contents # Pointer instances have a contents attribute which returns the object to which the pointer points
        (uid,gid,size,nlink,mode,atime,mtime,ctime)=my_getattr(path)
        # st.st_uid= 33
        # st.st_size= 1
        # st.st_nlink= 1
        # st.st_mode= stat.S_IFDIR | 0o777
        st.st_uid= uid
        st.st_gid= gid
        st.st_size= size
        st.st_nlink= nlink
        st.st_mode= mode
        # convert from float to int
        st.st_atimespec.tv_sec= atime # int(astat.st_atime) 
        st.st_mtimespec.tv_sec= mtime # int(astat.st_mtime)
        st.st_ctimespec.tv_sec= ctime # int(astat.st_ctime)
        return 0
    except:
        atpic.log.error(yy,'error getting', path)
        atpic.log.error(yy,traceback.format_exc())
        return -errno.ENOENT



def mygetxattr(path, name, position):
    yy=atpic.log.setname(xx,'mygetxattr')
    atpic.log.debug(yy,"ENTERING mygetxattr",path, name, position)
    return 0
    

def myinit(path):
    yy=atpic.log.setname(xx,'myinit')
    atpic.log.debug(yy,"ENTERING myinit",path)
    return 0

def mylink(target, source):
    yy=atpic.log.setname(xx,'mylink')
    atpic.log.debug(yy,"ENTERING mylink",target, source)
    return 0

def mylistxattr(path):
    yy=atpic.log.setname(xx,'mylistxattr')
    atpic.log.debug(yy,"ENTERING mylistxattr",path)
    return 0

def mymkdir(path, mode):
    yy=atpic.log.setname(xx,'mymkdir')
    atpic.log.debug(yy,"ENTERING mymkdir",path, mode)
    response=zmq_send(b'mkdir',path)
    response_int=bytes2int(response)
    return -response_int
    


def mymknod(path, mode, dev):
    yy=atpic.log.setname(xx,'mymknod')
    atpic.log.debug(yy,"ENTERING mymknod",path, mode, dev)
    return 0

def myopen(path, fip): # myopen(path, flags)
    yy=atpic.log.setname(xx,'myopen')
    atpic.log.debug(yy,"ENTERING myopen",path, fip)
    myflags=fip.contents.flags
    try:
        storepath=zmq_send(b'realpath',path) # this also tests permission
        atpic.log.debug(yy,'storepath',storepath)
        fd=os.open(storepath,myflags) 
        atpic.log.debug(yy,'fd',fd)
        fip.contents.fh = fd
        file_descriptors[fd]=storepath
        atpic.log.debug(yy,'returning success')
        return 0 # success
    except OSError as e:
        atpic.log.error(yy,'OSError getting', path,e)
        atpic.log.error(yy,'OSError errno is', e.errno)
        return -e.errno
    except:
        atpic.log.error(yy,'general error getting', path)
        atpic.log.error(yy,traceback.format_exc())
        return -errno.ENOENT # no such file or directory
    # return -errno.ENOENT # no such file or directory
    # return -errno.EACCES # permission denied

def myopendir(path,fip):
    yy=atpic.log.setname(xx,'myopendir')
    atpic.log.debug(yy,"ENTERING myopendir",path)
    return 0



def myread(path, buf,size, offset, fip): # myread(path, size, offset, fh)
    # http://code.google.com/p/fusepy/source/browse/trunk/fuse.py
    yy=atpic.log.setname(xx,'myread')
    atpic.log.debug(yy,"ENTERING myread",(path, buf,size, offset, fip))
    try:
        atpic.log.debug(yy,'fip.contents',fip.contents)
        atpic.log.debug(yy,'fip.contents.fh',fip.contents.fh)
        fi = fip.contents
        atpic.log.debug(yy,'FIFLAGShex',hex(fi.flags))
        # see hello.py
        fd=fip.contents.fh
        os.lseek(fd, offset,os.SEEK_SET)
        ret=os.read(fd, size)
        # atpic.log.debug(yy,'ret',ret)
        data = create_string_buffer(ret[:size], size)
        memmove(buf, data, size)
        return size
    #  return -errno.EACCES # negative indicates an error
    except:
        atpic.log.error(yy,'error getting', path)
        atpic.log.error(yy,traceback.format_exc())
        return -errno.EACCES # negative indicates an error



"""

http://fuse.sourceforge.net/doxygen/structfuse__operations.html
int(* fuse_operations::readdir)(const char *, void *, fuse_fill_dir_t, off_t, struct fuse_file_info *)

Read directory

This supersedes the old getdir() interface. New applications should use this.

The filesystem may choose between two modes of operation:

1) The readdir implementation ignores the offset parameter, and passes zero to the filler function's offset. The filler function will not return '1' (unless an error happens), so the whole directory is read in a single readdir operation. This works just like the old getdir() method.

2) The readdir implementation keeps track of the offsets of the directory entries. It uses the offset parameter and always passes non-zero offset to the filler function. When the buffer is full (or an error happens) the filler function will return '1'.

Introduced in version 2.3 
"""
def myreaddir(path,buf,filler,offset,info):
    yy=atpic.log.setname(xx,'myreaddir')
    # easy to unit test
    atpic.log.debug(yy,"ENTERING myreaddir path=",path,"buf=",buf,"filler=",filler,"offset=",offset,"info=",info)

    # set the filelist
    try:
       filelist= my_readdir(path,offset=offset)
       atpic.log.debug(yy,"----------filelist:",filelist)
       for afile in filelist:
           # filler(buf, afile.encode('utf-8'), None, offset)
           st = c_stat()
           # st.st_mode = S_IFDIR
           # st.st_mode = stat.S_IFDIR
           # filler(buf, afile, st, offset)
           resfiller=filler(buf, afile, None, 0)
           atpic.log.debug(yy,'resfiller',resfiller)
           # http://www.cs.hmc.edu/~geoff/classes/hmc.cs135.201001/homework/fuse/fuse_doc.html
       return 0
    except:
        atpic.log.debug(yy,"could not get file list!",path)
        atpic.log.error(yy,traceback.format_exc())
        return -errno.ENOENT



def myreadlink(path, buf, bufsize):
    yy=atpic.log.setname(xx,'myreadlink')
    atpic.log.debug(yy,"ENTERING myreadlink",path,buf, bufsize)
    path=transform_path2tree(path)
    print("path2LINK1",path)

    try:
        # path=transform_path2tree(path)
        print("path2LINK2",path)
        thelink=os.readlink(path) # should be string
        print("theLINK is",thelink)
        data = create_string_buffer(thelink[:bufsize - 1])
        memmove(buf, data, len(data))
        return 0
    except:
        return -errno.ENOENT

def myrelease(path, fip):
    yy=atpic.log.setname(xx,'myrelease')
    atpic.log.debug(yy,"ENTERING myrelease path=",path,"fip=",fip)

    myflags=fip.contents.flags
    atpic.log.debug(yy,"myflags",myflags)
    atpic.log.debug(yy,"getting file descriptor local path...")
    fd=fip.contents.fh
    atpic.log.debug(yy,"fd",fd)
    storepath=file_descriptors[fd]
    atpic.log.debug(yy,"releasing storepath",storepath)
    afile=file_descriptors.pop(fd)
    atpic.log.debug(yy,"popped",afile)
    atpic.log.debug(yy,"LEAVING")
    os.close(fd) # free the FD, last one, to avoid concurrency issues
    zmq_send(b'process',path)
    return 0

def myreleasedir(path, fh):
    yy=atpic.log.setname(xx,'myreleasedir')
    atpic.log.debug(yy,"ENTERING myreleasedir",path, fh)
    return 0

def myremovexattr(path, name):
    yy=atpic.log.setname(xx,'myremovexattr')
    atpic.log.debug(yy,"ENTERING myremovexattr",path, name)
    return 0

def myrename(old, new):
    yy=atpic.log.setname(xx,'myrename')
    atpic.log.debug(yy,"ENTERING myrename",old, new)
    response=zmq_send(b'rename',old+b'\0'+new) # use NULL asa separator (could use \n, \t)
    response_int=bytes2int(response)
    return -response_int

    
def myrmdir(path):
    yy=atpic.log.setname(xx,'myrmdir')
    atpic.log.debug(yy,"ENTERING myrmdir",path)
    response=zmq_send(b'rmdir',path)
    response_int=bytes2int(response)
    return -response_int
    
    

def mysetxattr(path, name, value, options, position):
    yy=atpic.log.setname(xx,'mysetxattr')
    atpic.log.debug(yy,"ENTERING mysetxattr",path, name, value, options, position)
    return 0

def mystatfs(path,buf):
    yy=atpic.log.setname(xx,'mystatfs')
    # this is used in 'df' style commands
    atpic.log.debug(yy,"ENTERING mystatfs",path,buf)
    return 0

def mysymlink(target, source):
    yy=atpic.log.setname(xx,'mysymlink')
    atpic.log.debug(yy,"ENTERING mysymlink",target, source)
    return 0

def mytruncate(path, length):
    yy=atpic.log.setname(xx,'mytruncate')
    atpic.log.debug(yy,"ENTERING mytruncate",path, length)
    return 0

def myunlink(path):
    yy=atpic.log.setname(xx,'myunlink')
    atpic.log.debug(yy,"ENTERING myunlink",path)
    response=zmq_send(b'unlink',path)
    response_int=bytes2int(response)
    return -response_int
    

def myutimens(path, times):
    yy=atpic.log.setname(xx,'myutimens')
    atpic.log.debug(yy,"ENTERING myutimens",path, times)
    return 0


def mywrite(path, buf, size, offset, fip):
    # returns the nb of bytes written
    yy=atpic.log.setname(xx,'mywrite')
    atpic.log.debug(yy,"ENTERING mywrite",(path, buf, size, offset, fip))
    try:
        data = string_at(buf, size)
        atpic.log.debug(yy,"data=",data)
        fh=fip.contents.fh
        atpic.log.debug(yy,"fh=",fh)
        nbofbytes_written=os.write(fh,data)
        atpic.log.debug(yy,"wrote",nbofbytes_written,'bytes')
        if nbofbytes_written < size:
            atpic.log.error(yy,"wrote less bytes that data length",nbofbytes_written,'<',size)
        else:
            atpic.log.debug(yy,"wrote all data")
        return nbofbytes_written # success if could write
    except OSError as e:
        atpic.log.error(yy,'OSError getting', path,e)
        atpic.log.error(yy,'OSError errno is', e.errno)
        return -e.errno
    except:
        atpic.log.error(yy,'unkown error',traceback.format_exc())
        return 0


if __name__ == "__main__":
    print("mounting....")
    # logging.basicConfig(level=logging.DEBUG)



    # global variables:
    lock=Lock()
    


    fuse_ops = fuse_operations() # create a structure

    # implement some prototypes
    fuse_ops.access=prototype_access(myaccess)
    fuse_ops.chmod=prototype_chmod(mychmod)
    fuse_ops.chown=prototype_chown(mychown)
    fuse_ops.create=prototype_create(mycreate)
    fuse_ops.destroy=prototype_destroy(mydestroy)
    fuse_ops.flush=prototype_flush(myflush)
    fuse_ops.fsync=prototype_fsync(myfsync)
    fuse_ops.fsyncdir=prototype_fsyncdir(myfsyncdir)
    fuse_ops.getattr=prototype_getattr(mygetattr) # yes 1
    # fuse_ops.getxattr=prototype_getxattr(mygetxattr)
    fuse_ops.init=prototype_init(myinit)
    fuse_ops.link=prototype_link(mylink)
    # fuse_ops.listxattr=prototype_listxattr(mylistxattr)
    fuse_ops.mkdir=prototype_mkdir(mymkdir)
    fuse_ops.mknod=prototype_mknod(mymknod)
    fuse_ops.open=prototype_open(myopen)
    fuse_ops.opendir=prototype_opendir(myopendir)
    fuse_ops.read=prototype_read(myread)
    fuse_ops.readdir=prototype_readdir(myreaddir) # yes 2
    fuse_ops.readlink=prototype_readlink(myreadlink)
    fuse_ops.release=prototype_release(myrelease)
    fuse_ops.releasedir=prototype_releasedir(myreleasedir)
    # fuse_ops.removexattr=prototype_removexattr(myremovexattr)
    fuse_ops.rename=prototype_rename(myrename)
    fuse_ops.rmdir=prototype_rmdir(myrmdir)
    # fuse_ops.setxattr=prototype_setxattr(mysetxattr)
    fuse_ops.statfs=prototype_statfs(mystatfs)
    fuse_ops.symlink=prototype_symlink(mysymlink)
    fuse_ops.truncate=prototype_truncate(mytruncate)
    fuse_ops.unlink=prototype_unlink(myunlink)
    fuse_ops.utimens=prototype_utimens(myutimens)
    fuse_ops.write=prototype_write(mywrite)


    # http://www.mjmwired.net/kernel/Documentation/filesystems/fuse.txt
    args = [b'fuse']


    # DO NOT USE IN PROD:
    args.append(b'-f') # foreground
    args.append(b'-d') # debug
   
    # args.append(b'-s') # single threaded
    args.append(b'-o') # further options
    args.append(b'fsname=myatpicfs,allow_other')
    # Note: you still need to put the 33 user in the fuse group
    # usermod -G fuse www-data
    # and set in /etc/fuse.conf
    # user_allow_other
    # chown www-data: /ftpusers/





    # mountpoint=b"/atpicpathbased"
    mountpoint=b"/ftpusers"
    # mount -o bind /atpicpathbased /ftpusers
    args.append(mountpoint) # finally the mount point

    # http://bugs.python.org/issue13665
    # http://stackoverflow.com/questions/3494598/passing-a-list-of-strings-to-from-python-ctypes-to-c-function-expecting-char
    # argv = (c_char_p * len(args))(*args)
    
    # _libfuse.fuse_main_real(len(args), argv, pointer(fuse_ops), sizeof(fuse_ops), None)
    myfuse_main_real(args,fuse_ops)


"""
OK
root@x61s:~# ls -alh /ftpusers/alexmadon
total 8.0K
drwxr-xr-x 2 root root 4.0K Aug  5 13:14 .
drwxr-xr-x 3 root root 4.0K Aug  5 13:14 ..
root@x61s:~# chmod a+rwx /ftpusers/alexmadon/

NOT OK

root@x61s:~# ls -alh /ftpusers/alexmadon/
total 8.0K
drwxrwxrwx 2 root root 4.0K Aug  5 13:14 .
drwxr-xr-x 3 root root 4.0K Aug  5 13:14 ..


"""
