#!/usr/bin/python3
# id based filesystem
"""
we import our own fuse * and ctypes *
"""
import os
# import logging
import atpic.log
from ctypes import *
from ctypes.util import find_library
from errno import *
import stat

import atpic.log


from atpic.fuse3at import *

xx=atpic.log.setmod("INFO","fuse3example2")
xx=atpic.log.setmod("INFO","fuse3example2")




# =============================================================
#
#  my_* functions: super simple, easy to unit test
#
# =============================================================

# /atpicfuse/uid/gid/
# points to:
# /mount/2012/31/12/23/59/uid_pid_gid.extension
# see processinfiles.py

def my_readdir(path,offset=0):
    """
    returns a list of files under path, easy to unit test
    """
    filelist=[b'.',b'..',b'alex',b'Clara cet \xc3\xa9t\xc3\xa9 l\xc3\xa0']
    return filelist

def my_getattr(path):
    """
    returns stats for path, easy to unit test
    """
    uid=33
    gid=33
    size=1
    nlink=1
    mode=stat.S_IFDIR | 0o777
    atime=0
    mtime=0
    ctime=0
    return (uid,gid,size,nlink,mode,atime,mtime,ctime)

# =============================================================
#
#  my* prototypes
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

def mycreate(path, mode, fileinfo):
    yy=atpic.log.setname(xx,'mycreate')
    atpic.log.debug(yy,"ENTERING mycreate", path, mode, fileinfo)
    return 0

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
        return -ENOENT


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
    return 0


def mymknod(path, mode, dev):
    yy=atpic.log.setname(xx,'mymknod')
    atpic.log.debug(yy,"ENTERING mymknod",path, mode, dev)
    return 0

def myopen(path, flags):
    yy=atpic.log.setname(xx,'myopen')
    atpic.log.debug(yy,"ENTERING myopen",path, flags)
    return 0

def myopendir(path,fileinfo):
    yy=atpic.log.setname(xx,'myopendir')
    atpic.log.debug(yy,"ENTERING myopendir",path)
    return 0

def myread(path, size, offset, fh):
    yy=atpic.log.setname(xx,'myread')
    atpic.log.debug(yy,"ENTERING myread",path, size, offset, fh)
    return 0

def myreaddir(path,buf,filler,offset,info):
    yy=atpic.log.setname(xx,'myreaddir')
    # easy to unit test
    atpic.log.debug(yy,"ENTERING myreaddir path=",path,"buf=",buf,"filler=",filler,"offset=",offset,"info=",info)

    # set the filelist
    try:
       filelist= my_readdir(path,offset=offset)
       atpic.log.debug(yy,"----------filelist:",filelist)
       for afile in filelist:
           st = c_stat()
           # st.st_mode = stat.S_IFDIR
           filler(buf, afile, st, offset)
           # http://www.cs.hmc.edu/~geoff/classes/hmc.cs135.201001/homework/fuse/fuse_doc.html
       return 0
    except:
        return -ENOENT

def myreadlink(path, buf, bufsize):
    yy=atpic.log.setname(xx,'myreadlink')
    atpic.log.debug(yy,"ENTERING myreadlink",path,buf, bufsize)
    path=path.decode("utf8") # decode early
    path=transform_path2tree(path)
    print("path2LINK1",path)

    try:
        # path=transform_path2tree(path)
        print("path2LINK2",path)
        thelink=os.readlink(path) # should be string
        print("theLINK is",thelink)
        thelink=thelink.encode('utf-8') # encode late
        data = create_string_buffer(thelink[:bufsize - 1])
        memmove(buf, data, len(data))
        return 0
    except:
        return -ENOENT

def myrelease(path, fh):
    yy=atpic.log.setname(xx,'myrelease')
    atpic.log.debug(yy,"ENTERING myrelease",path, fh)
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
    return 0

    
def myrmdir(path):
    yy=atpic.log.setname(xx,'myrmdir')
    atpic.log.debug(yy,"ENTERING myrmdir",path)
    return 0
    

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

def mytruncate(path, length, fh):
    yy=atpic.log.setname(xx,'mytruncate')
    atpic.log.debug(yy,"ENTERING mytruncate",path, length, fh)
    return 0

def myunlink(path):
    yy=atpic.log.setname(xx,'myunlink')
    atpic.log.debug(yy,"ENTERING myunlink",path)
    return 0

def myutimens(path, times):
    yy=atpic.log.setname(xx,'myutimens')
    atpic.log.debug(yy,"ENTERING myutimens",path, times)
    return 0

def mywrite(path, data, offset, fh):
    yy=atpic.log.setname(xx,'mywrite')
    atpic.log.debug(yy,"ENTERING mywrite",path, data, offset, fh)
    return 0


if __name__ == "__main__":
    print("mounting....")
    # logging.basicConfig(level=logging.DEBUG)

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
    args.append(b'-f') # foreground
    args.append(b'-d') # debug
    # args.append(b'-s') # single threaded
    args.append(b'-o') # further options
    args.append(b'fsname=myatpicfs,allow_other')
    mountpoint=b"/atpicfuse"
    args.append(mountpoint) # finally the mount point

    # http://bugs.python.org/issue13665
    # http://stackoverflow.com/questions/3494598/passing-a-list-of-strings-to-from-python-ctypes-to-c-function-expecting-char
    # argv = (c_char_p * len(args))(*args)
    
    # _libfuse.fuse_main_real(len(args), argv, pointer(fuse_ops), sizeof(fuse_ops), None)
    myfuse_main_real(args,fuse_ops)
