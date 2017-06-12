#!/usr/bin/env python

#    Copyright (C) 2001  Jeff Epler  <jepler@unpythonic.dhs.org>
#    Copyright (C) 2006  Csaba Henk  <csaba.henk@creo.hu>
#
#    This program can be distributed under the terms of the GNU LGPL.
#    See the file COPYING.
#
# python fuse1.py mnt

import os
import sys
import stat
from errno import *
from stat import *
import fcntl

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
        self.st_mode = stat.S_IFDIR | 0755
        # self.st_mode = 0755
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 2
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
        mylog("called getattr on %s" % path)
        st = MyStat()
        return st
        # return -errno.ENOENT

    def readlink(self, path):
        # return os.readlink("." + path)
        mylog("called readlink on %s" % path)

    def readdir(self, path, offset):
        mylog("called readdir on path=%s, offset=%s" % (path,offset))
        # for e in os.listdir("." + path):
        #     yield fuse.Direntry(e)

    def unlink(self, path):
        mylog("called unlink on %s" % path)
        # os.unlink("." + path)

    def rmdir(self, path):
        mylog("called rmdir on %s" % path)
        # os.rmdir("." + path)

    def symlink(self, path, path1):
        mylog("called symlink on path=%s, path1=%s" % (path,path1))
        # os.symlink(path, "." + path1)

    def rename(self, path, path1):
        mylog("called rename on path=%s, path1=%s" % (path,path1))
        # os.rename("." + path, "." + path1)

    def link(self, path, path1):
        # os.link("." + path, "." + path1)
        mylog("called link on path=%s, path1=%s" % (path,path1))

    def chmod(self, path, mode):
        # os.chmod("." + path, mode)
        mylog("called chmod on path=%s, mode=%s" % (path,mode))

    def chown(self, path, user, group):
        # os.chown("." + path, user, group)
        mylog("called chown on path=%s, user=%s, group=%s" % (path, user, group))

    def truncate(self, path, len):
        # f = open("." + path, "a")
        # f.truncate(len)
        # f.close()
        mylog("called chmod on path=%s, len=%s" % (path, len))

    def mknod(self, path, mode, dev):
        # os.mknod("." + path, mode, dev)
        mylog("called mknod on path=%s, mode=%s, dev=%s" % (path,mode,dev))

    def mkdir(self, path, mode):
        # os.mkdir("." + path, mode)
        mylog("called mkdir on path=%s, mode=%s" % (path,mode))

    def utime(self, path, times):
        # os.utime("." + path, times)
        mylog("called chmod on path=%s, times=%s" % (path,times))

#    The following utimens method would do the same as the above utime method.
#    We can't make it better though as the Python stdlib doesn't know of
#    subsecond preciseness in acces/modify times.
#  
#    def utimens(self, path, ts_acc, ts_mod):
#      os.utime("." + path, (ts_acc.tv_sec, ts_mod.tv_sec))

    def access(self, path, mode):
        # if not os.access("." + path, mode):
        #     return -EACCES
        mylog("called chmod on path=%s, mode=%s" % (path,mode))


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
    server.multithreaded=False
    # call my functon setup(0 to check the values of the parsed parameters
    server.setup()
    server.main()
    
    
    
    
if __name__ == '__main__':
    # see http://www.diveintopython.org/scripts_and_streams/command_line_arguments.html
    # main(sys.argv[1:])
    main()
    
