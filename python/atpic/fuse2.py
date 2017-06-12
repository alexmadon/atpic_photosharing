#!/usr/bin/env python

#    Copyright (C) 2001  Jeff Epler  <jepler@unpythonic.dhs.org>
#    Copyright (C) 2006  Csaba Henk  <csaba.henk@creo.hu>
#
#    This program can be distributed under the terms of the GNU LGPL.
#    See the file COPYING.
#
# python fuse2.py mnt

"""
Usage:

python fuse2.py mnt

"""
# gmailfs uses a client cache 
# which is cleared with self.inodeCache = {}
# at unlink, rmdir, rename

# http://apps.sourceforge.net/mediawiki/fuse/index.php?title=Stat
# see also "man fstat"

# http://www.brandonhutchinson.com/ctime_atime_mtime.html
# In UNIX, it is not possible to tell the actual creation time of a file. 

# mtime -- The mtime--modify time--is the time when the actual contents of a file was last modified. This is the time displayed in a long directoring listing (ls -l).

# ctime --- The ctime--change time--is the time when changes were made to the file or directory's inode (owner, permissions, etc.). The ctime is also updated when the contents of a file change. It is needed by the dump command to determine if the file needs to be backed up. You can view the ctime with the ls -lc command.

# atime -- The atime--access time--is the time when the data of a file was last ac cessed. Displaying the contents of a file or executing a shell script will update a file's atime, for example. You can view the atime with the ls -lu command.






# error code
# http://apps.sourceforge.net/mediawiki/fuse/index.php?title=Errno_base

# ENOENT       2 /* No such file or directory */
# EINVAL      22 /* Invalid argument */


import os
import sys
import stat
import errno
from stat import *
import fcntl
import time

import fuse

fuse.fuse_python_api = (0, 2)


def mylog(str):
    file="/home/madon/alexfs.log"
    FILE = open(file,"a")
    FILE.write(str)
    FILE.write("\n")
    FILE.close()


class MyStat(fuse.Stat):
    def __init__(self):

        # http://apps.sourceforge.net/mediawiki/fuse/index.php?title=Stat
        self.st_mode = stat.S_IFDIR | 0755
        # self.st_mode = 0755
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 1   # used with the 'find' command 
        # http://www.cygwin.com/ml/cygwin-developers/2008-04/msg00112.html
        # Do we really need correct st_nlink count for directories?
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 4096
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0



class AlexFS(fuse.Fuse):

    def __init__(self, *args, **kw):

        mylog("=====__init__======")
        fuse.Fuse.__init__(self, *args, **kw)
        # could set self.file_class and self.dir_class
        self.root="/tmp"
        mylog("multithreaded: %s" % self.multithreaded) # the original mountpoint
        for arg in args:
            mylog("Unnamed option:arg: " % (arg))

        for name, value in kw.items():
            mylog("Named option: %s: %s" % (name, value))
        mylog(repr(dir(self)))
        mylog("root: %s" % self.root)


    def setup(self):
        mylog("=====SETUP======")
        mylog("root: %s" % self.root)
        mylog("multithreaded: %s" % self.multithreaded) # the original mountpoint



    def getattr(self, path):
        # http://apps.sourceforge.net/mediawiki/fuse/index.php?title=Getattr()
        # REQUIRED
        # this returns a stat object (structure)
        # see
        # http://apps.sourceforge.net/mediawiki/fuse/index.php?title=Stat
        # for the fields
        mylog("**** called getattr on %s" % path)
        st = MyStat()
        mylog("A")
        pe = path.split('/')[1:]
        mylog("after split")

        st.st_atime = int(time.time())
        st.st_mtime = st.st_atime
        st.st_ctime = st.st_atime
        mylog("after time")
        mylog("pe-1: %s" % pe[-1])
        if path == '/':
            mylog("getattr on root path.....")
            st.st_mode = stat.S_IFDIR | 0755 # Directory
            st.st_nlink = 1
            st.st_size = 1024
        elif pe[-1]=="alex":
            mylog("match alex: %s" % pe[-1])
            st.st_mode = stat.S_IFREG | 0666 # Regular file
            st.st_nlink = 1
            st.st_size = 1024
        elif pe[-1]=="dir1":
            mylog("match dir1: %s" % pe[-1])
            st.st_mode = stat.S_IFDIR | 0755 # Directory
            st.st_nlink = 1
            st.st_size = 1024

        else:
            mylog("returning errno.ENOENT %s" % errno.ENOENT )
            return -errno.ENOENT # No such file or directory
            # return -2



        mylog("SUCCESS: returning st")

        return st
        # return -errno.ENOENT

    def readlink(self, path):
        # return os.readlink("." + path)
        mylog("**** called readlink on %s" % path)

    def readdir(self, path, offset):
        # http://apps.sourceforge.net/mediawiki/fuse/index.php?title=Readdir()
        # REQUIRED

        # could cache the result of the next getattr
        # or make gettatr very fast

        mylog("**** called readdir on path=%s, offset=%s" % (path,offset))
        directories=[".","..","alex","dir1"]
        # directories=os.listdir("/etc/")
        for e in directories:
            mylog("dir entry type %s" % type(e))
            mylog("dir entry %s" % e)
        
            yield fuse.Direntry(e)
        # for e in os.listdir("." + path):
        #     yield fuse.Direntry(e)

    def unlink(self, path):
        mylog("**** called unlink on %s" % path)
        # os.unlink("." + path)

    def rmdir(self, path):
        mylog("**** called rmdir on %s" % path)
        # os.rmdir("." + path)

    def symlink(self, path, path1):
        mylog("**** called symlink on path=%s, path1=%s" % (path,path1))
        # os.symlink(path, "." + path1)

    def rename(self, path, path1):
        mylog("**** called rename on path=%s, path1=%s" % (path,path1))
        # os.rename("." + path, "." + path1)

    def link(self, path, path1):
        # os.link("." + path, "." + path1)
        mylog("**** called link on path=%s, path1=%s" % (path,path1))

    def chmod(self, path, mode):
        # os.chmod("." + path, mode)
        mylog("**** called chmod on path=%s, mode=%s" % (path,mode))

    def chown(self, path, user, group):
        # os.chown("." + path, user, group)
        mylog("**** called chown on path=%s, user=%s, group=%s" % (path, user, group))

    def truncate(self, path, len):
        # f = open("." + path, "a")
        # f.truncate(len)
        # f.close()
        mylog("**** called truncate on path=%s, len=%s" % (path, len))

    def mknod(self, path, mode, dev):
        # os.mknod("." + path, mode, dev)
        mylog("**** called mknod on path=%s, mode=%s, dev=%s" % (path,mode,dev))

    def mkdir(self, path, mode):
        # os.mkdir("." + path, mode)
        mylog("**** called mkdir on path=%s, mode=%s" % (path,mode))

    def utime(self, path, times):
        # os.utime("." + path, times)
        mylog("**** called utime on path=%s, times=%s" % (path,times))

#    The following utimens method would do the same as the above utime method.
#    We can't make it better though as the Python stdlib doesn't know of
#    subsecond preciseness in acces/modify times.
#  
#    def utimens(self, path, ts_acc, ts_mod):
#      os.utime("." + path, (ts_acc.tv_sec, ts_mod.tv_sec))

    def access(self, path, mode):
        # if not os.access("." + path, mode):
        #     return -EACCES
        mylog("**** called access on path=%s, mode=%s" % (path,mode))


    def read(self, path, readlen, offset):
        mylog("**** called read on path=%s, readlen=%s, offset=%s" % (path, readlen, offset))
        return "This is some DATA"


    def write(self, path, buf, off):
        mylog("**** called write on path=%s, buff=%s, off=%s" % (path, buf, off))


#    This is how we could add stub extended attribute handlers...
#    (We can't have ones which aptly delegate requests to the underlying fs
#    because Python lacks a standard xattr interface.)
#
#    def getxattr(self, path, name, size):
#        val = name.swapcase() + '@' + path
#        if size == 0:
#            # We are asked for size of the value.
#            return len(val)
#        return val
#
#    def listxattr(self, path, size):
#        # We use the "user" namespace to please XFS utils
#        aa = ["user." + a for a in ("foo", "bar")]
#        if size == 0:
#            # We are asked for size of the attr list, ie. joint size of attrs
#            # plus null separators.
#            return len("".join(aa)) + len(aa)
#        return aa

    def statfs(self):
        """
        Should return an object with statvfs attributes (f_bsize, f_frsize...).
        Eg., the return value of os.statvfs() is such a thing (since py 2.2).
        If you are not reusing an existing statvfs object, start with
        fuse.StatVFS(), and define the attributes.

        To provide usable information (ie., you want sensible df(1)
        output, you are suggested to specify the following attributes:

            - f_bsize - preferred size of file blocks, in bytes
            - f_frsize - fundamental size of file blcoks, in bytes
                [if you have no idea, use the same as blocksize]
            - f_blocks - total number of blocks in the filesystem
            - f_bfree - number of free blocks
            - f_files - total number of file inodes
            - f_ffree - nunber of free file inodes
        """

        # return os.statvfs(".")
        pass

    def fsinit(self):
        # os.chdir(self.root)
        pass




def main():
    
    usage = """
Userspace nullfs-alike: mirror the filesystem tree from some point on.

""" + fuse.Fuse.fusage
    # call the constructor with default parameters
    server = AlexFS(
        version="%prog " + fuse.__version__,
        usage=usage,
        dash_s_do='setsingle',
        
        )
    server.parser.add_option(
        mountopt="root", metavar="PATH", default='/', help="mirror filesystem from under PATH [default: %default]",
        )
    server.parse(values=server, errex=1)
    # server.multithreaded=False # needs to be multithreaded
    # call my functon setup(0 to check the values of the parsed parameters
    server.setup()
    server.main()
    
    
    
    
if __name__ == '__main__':
    # see http://www.diveintopython.org/scripts_and_streams/command_line_arguments.html
    # main(sys.argv[1:])
    main()
    
