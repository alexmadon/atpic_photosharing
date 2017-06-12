#!/usr/bin/python3
import os
# import logging
import atpic.log
from ctypes import *
from ctypes.util import find_library
from errno import *
import stat
import os
import time
import threading
from multiprocessing import Lock

import atpic.log


from atpic.fuse3at import *

xx=atpic.log.setmod("INFO","fuse3example")




# ============================
#
#
#
# ============================

# utilities
# print overloading: http://www.python.org/dev/peps/pep-3105/#id4
# http://docs.python.org/tutorial/controlflow.html#more-on-defining-functions


lock=Lock()

def my_print(*messages):
    mypid=threading.current_thread()
    spl=mypid.name.split('-')
    pname=spl[1]
    lock.acquire()
    print(mypid.name,"<<<<<<",end=' ')

    for i in range(0,10000):
        print(pname,sep=' ',end=' ')

    for message in messages:
        print(message,end=' ')
    print(mypid.name,">>>>>>")
    lock.release()

def has_dir_pattern(path):
    # expects a utf8 path
    import re
    if re.match(".*\.[a-zA-Z]{3}",path):
        return 0 # this is a file pattern
    else:
        return 1 # this is a directory pattern


def get_validdirs():
    return ["u_webdav","u_http","u_ftp","u_cookie","i_webdav","i_http","i_ftp","i_cookie"]




# top directories: http, ftp, webdav, htpassd (x2: uuid and uname)
def remove_cookies_info(path):
    # removes anythong beofore the /:: marker
    path2=re.sub("^.*\/::\/","",path)
    if path2==path:
        # there was no '::' in the path
        # eg: /u_cookie/http_lang:en-us,en;q=0.5/country:--
        path2=""
    return path2

def transform_path2tree(path):
    # can be unit tested easily
    splitted=path.split("/")
    if splitted[1] not in get_validdirs():
        raise Exception("path does not exist")
    else:
        print("--- this is a valid start of path ----")
        if splitted[1][0]=='u':
            startpath="/atpictree_ln"
        else:
            startpath="/atpictree"
        # now we have the real disk path
        joined="/".join(splitted[2:])
        print("joined",joined)
        joined=remove_cookies_info(joined)
        if joined != "":
            joined="/"+joined
        fullpath=startpath+joined
        print("++++FULLPATH",fullpath)
        return fullpath


def transform_path2node(treepath,base=""):
    # return uid, gid, pid for a user path, a gallery path and a pic path
    print("$$$$$$$$$$ Entering transform_path2node",treepath)
    # for pics, you could read the symlink and parse it to get all the info
    # for galleries, you need to read the .meta file
    # for users: if 'i': then read the name, if 'u' then read the symlink


def mylistdir(path):
    filelist=['.','..']
    if path=="/":
        filelist=filelist+get_validdirs()
    else:
        fullpath=transform_path2tree(path)
        print("fffffffffuuulllllpath=",fullpath)
        filelist=filelist+os.listdir(fullpath)
    return filelist
            
        


# =============================================================
#
#
#
# =============================================================

def myaccess(path, amode):
    my_print("ENTERING myaccess on",path,"mode=",amode)
    return 0

    



def mychmod(path,mode):
    my_print("ENTERING mychmod path=",path,"mode=",mode)
    return 0
    
def mychown(path, uid, gid):
    my_print("ENTERING mychown path=",path,"uid=",uid, "gid=",gid)
    return 0

def myflush(path, fh):
    my_print("ENTERING myflush",path, fh)
    return 0

def myfsync(path, datasync, fh):
    my_print("ENTERING myfsync path=",path, datasync, fh)
    return 0

def myfsyncdir(path, datasync, fh):
    my_print("ENTERING myfsyncdir",path, datasync, fh)
    return 0

def mycreate(path, mode, fileinfo):
    my_print("ENTERING mycreate", path, mode, fileinfo)
    return 0

def mydestroy(path):
    my_print("ENTERING mydestroy", path)
    return 0

def mygetattr(path,buf):
    # difficult to unit test
    # need a dispatcher to some (few) known cases
    my_print("ENTERING mygetattr on",path)
    path=path.decode("utf8") # decode early
    memset(buf, 0, sizeof(c_stat))
    if path=="/":
        st = buf.contents
        # st.st_mode = stat.S_IFDIR
        st.st_uid= 33
        st.st_size= 1
        st.st_nlink= 1
        st.st_mode= stat.S_IFDIR | 0o777
        return 0
    else:

        try:
            fullpath=transform_path2tree(path)
            nodepath=transform_path2node(path)
        except:
            return -ENOENT

        try:
            astat=os.stat(fullpath) # by default we follow links
        except:
            # return -ENOENT
            try:
                astat=os.lstat(fullpath) # if a link is orphaned, then get the link
                # astat.st_mode=stat.S_IFREG
                # astat.st_uid= 33 # astat.st_uid
                # astat.st_size= 0
            except:
              return -ENOENT
            
        st = buf.contents # Pointer instances have a contents attribute which returns the object to which the pointer points
        st.st_mode = astat.st_mode
        # if stat.S_ISLNK(st.st_mode):
        #    st.st_mode=st.st_mode 
        st.st_uid= 33 # astat.st_uid
        st.st_nlink= astat.st_nlink
        st.st_size= astat.st_size
        print("Typppe astat.st_atime",type(astat.st_atime)) # is a float
        st.st_atimespec.tv_sec= int(astat.st_atime) # convert from float to int
        st.st_mtimespec.tv_sec= int(astat.st_mtime)
        st.st_ctimespec.tv_sec= int(astat.st_ctime)
        print("mode",st.st_mode, type(st.st_mode))
        print("astat",astat)
        print("st.st_atimespec",st.st_atimespec.tv_sec)
        return 0
    # except:
    #     print("mygetattr erroralex1")
    #     return -ENOENT



def mygetxattr(path, name, position):
    my_print("ENTERING mygetxattr",path, name, position)
    return 0
    

def myinit(path):
    my_print("ENTERING myinit",path)
    return 0

def mylink(target, source):
    my_print("ENTERING mylink",target, source)
    return 0

def mylistxattr(path):
    my_print("ENTERING mylistxattr",path)
    return 0

def mymkdir(path, mode):
    my_print("ENTERING mymkdir",path, mode)
    return 0


def mymknod(path, mode, dev):
    my_print("ENTERING mymknod",path, mode, dev)
    return 0

def myopen(path, flags):
    my_print("ENTERING myopen",path, flags)
    return 0

def myopendir(path,fileinfo):
    my_print("ENTERING myopendir",path)
    return 0

def myread(path, size, offset, fh):
    my_print("ENTERING myread",path, size, offset, fh)
    return 0

def myreaddir(path,buf,filler,offset,info):
    # easy to unit test
    my_print("ENTERING myreaddir",path,buf,filler,offset,info)
    path=path.decode("utf8") # decode early

    # set the filelist
    try:
       filelist= mylistdir(path)
       print("----------filelist:",filelist)
       for afile in filelist:
           # filler(buf, afile.encode('utf-8'), None, offset)
           st = c_stat()
           # st.st_mode = S_IFDIR
           # st.st_mode = stat.S_IFDIR
           filler(buf, afile.encode('utf-8'), st, offset)
           
           # http://www.cs.hmc.edu/~geoff/classes/hmc.cs135.201001/homework/fuse/fuse_doc.html
       return 0
    except:
        return -ENOENT
    # return -ENOENT
    # ['.','..','somedir']

def myreadlink(path, buf, bufsize):
    my_print("ENTERING myreadlink",path,buf, bufsize)
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
    my_print("ENTERING myrelease",path, fh)
    return 0

def myreleasedir(path, fh):
    my_print("ENTERING myreleasedir",path, fh)
    time.sleep(1)
    return 0

def myremovexattr(path, name):
    my_print("ENTERING myremovexattr",path, name)
    return 0

def myrename(old, new):
    my_print("ENTERING myrename",old, new)
    return 0

    
def myrmdir(path):
    my_print("ENTERING myrmdir",path)
    return 0
    

def mysetxattr(path, name, value, options, position):
    my_print("ENTERING mysetxattr",path, name, value, options, position)
    return 0

def mystatfs(path,buf):
    # this is used in 'df' style commands
    my_print("ENTERING mystatfs",path,buf)
    return 0

def mysymlink(target, source):
    my_print("ENTERING mysymlink",target, source)
    return 0

def mytruncate(path, length, fh):
    my_print("ENTERING mytruncate",path, length, fh)
    return 0

def myunlink(path):
    my_print("ENTERING myunlink",path)
    return 0

def myutimens(path, times):
    my_print("ENTERING myutimens",path, times)
    return 0

def mywrite(path, data, offset, fh):
    my_print("ENTERING mywrite",path, data, offset, fh)
    return 0





if __name__ == "__main__":
    print("mounting....")
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
    argv = (c_char_p * len(args))(*args)
    
    # _libfuse.fuse_main_real(len(args), argv, pointer(fuse_ops), sizeof(fuse_ops), None)
    myfuse_main_real(args,fuse_ops)
