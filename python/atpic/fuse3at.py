#!/usr/bin/python3
# python3 script ctypes interface to fuse
# inspaired by http://code.google.com/p/fusepy/
# but lower level, no funny classes


# uses the on-disk tree created by atpictree3.py for directory info
# for pic info: query direct to SQL
# stored by unanme, (uid?)
# different access: htpp, webdav, ftp, passwd with different contraints and auth


# all read operations are disk operations
# secret is stored as .secret on the folder: you ned to check before displaying

# >>> base64.b64encode(b"sasassaassas")
# b'c2FzYXNzYWFzc2Fz'
# File name too long
# http://en.wikipedia.org/wiki/Base64
# Another variant called modified Base64 for filename uses '-' instead of '/',
# (filesystem limit, generally 255) 	


# Why don't other users have access to the mounted filesystem?
# ------------------------------------------------------------
# FUSE imposes this restriction in order to protect other users' processes from wandering into a FUSE filesystem that does nasty things to them such as stalling their system calls forever. (See this comment.)

# To lift this restriction for all users or for just root, mount the filesystem with the "-oallow_other" or "-oallow_root" mount option, respectively. Non-root users can only use these mount options if "user_allow_other" is specified in /etc/fuse.conf.


# http://stackoverflow.com/questions/2354417/c-socket-api-is-thread-safe
# http://stackoverflow.com/questions/1981372/are-parallel-calls-to-send-recv-on-the-same-socket-valid


from ctypes import *
from ctypes.util import find_library
from errno import *
from platform import machine, system


class c_timespec(Structure):
    _fields_ = [('tv_sec', c_long), ('tv_nsec', c_long)]

class c_utimbuf(Structure):
    _fields_ = [('actime', c_timespec), ('modtime', c_timespec)]

class c_stat(Structure):
    pass    # Platform dependent

_system = system()
if _system in ('Darwin', 'FreeBSD'):
    _libiconv = CDLL(find_library("iconv"), RTLD_GLOBAL)     # libfuse dependency
    ENOTSUP = 45
    c_dev_t = c_int32
    c_fsblkcnt_t = c_ulong
    c_fsfilcnt_t = c_ulong
    c_gid_t = c_uint32
    c_mode_t = c_uint16
    c_off_t = c_int64
    c_pid_t = c_int32
    c_uid_t = c_uint32
    setxattr_t = CFUNCTYPE(c_int, c_char_p, c_char_p, POINTER(c_byte),
        c_size_t, c_int, c_uint32)
    getxattr_t = CFUNCTYPE(c_int, c_char_p, c_char_p, POINTER(c_byte),
        c_size_t, c_uint32)
    c_stat._fields_ = [
        ('st_dev', c_dev_t),
        ('st_ino', c_uint32),
        ('st_mode', c_mode_t),
        ('st_nlink', c_uint16),
        ('st_uid', c_uid_t),
        ('st_gid', c_gid_t),
        ('st_rdev', c_dev_t),
        ('st_atimespec', c_timespec),
        ('st_mtimespec', c_timespec),
        ('st_ctimespec', c_timespec),
        ('st_size', c_off_t),
        ('st_blocks', c_int64),
        ('st_blksize', c_int32)]
elif _system == 'Linux':
    ENOTSUP = 95
    c_dev_t = c_ulonglong
    c_fsblkcnt_t = c_ulonglong
    c_fsfilcnt_t = c_ulonglong
    c_gid_t = c_uint
    c_mode_t = c_uint
    c_off_t = c_longlong
    c_pid_t = c_int
    c_uid_t = c_uint
    setxattr_t = CFUNCTYPE(c_int, c_char_p, c_char_p, POINTER(c_byte), c_size_t, c_int)
    getxattr_t = CFUNCTYPE(c_int, c_char_p, c_char_p, POINTER(c_byte), c_size_t)
    
    _machine = machine()
    if _machine == 'x86_64':
        c_stat._fields_ = [
            ('st_dev', c_dev_t),
            ('st_ino', c_ulong),
            ('st_nlink', c_ulong),
            ('st_mode', c_mode_t),
            ('st_uid', c_uid_t),
            ('st_gid', c_gid_t),
            ('__pad0', c_int),
            ('st_rdev', c_dev_t),
            ('st_size', c_off_t),
            ('st_blksize', c_long),
            ('st_blocks', c_long),
            ('st_atimespec', c_timespec),
            ('st_mtimespec', c_timespec),
            ('st_ctimespec', c_timespec)]
    elif _machine == 'ppc':
        c_stat._fields_ = [
            ('st_dev', c_dev_t),
            ('st_ino', c_ulonglong),
            ('st_mode', c_mode_t),
            ('st_nlink', c_uint),
            ('st_uid', c_uid_t),
            ('st_gid', c_gid_t),
            ('st_rdev', c_dev_t),
            ('__pad2', c_ushort),
            ('st_size', c_off_t),
            ('st_blksize', c_long),
            ('st_blocks', c_longlong),
            ('st_atimespec', c_timespec),
            ('st_mtimespec', c_timespec),
            ('st_ctimespec', c_timespec)]
    else:
        # i686, use as fallback for everything else
        c_stat._fields_ = [
            ('st_dev', c_dev_t),
            ('__pad1', c_ushort),
            ('__st_ino', c_ulong),
            ('st_mode', c_mode_t),
            ('st_nlink', c_uint),
            ('st_uid', c_uid_t),
            ('st_gid', c_gid_t),
            ('st_rdev', c_dev_t),
            ('__pad2', c_ushort),
            ('st_size', c_off_t),
            ('st_blksize', c_long),
            ('st_blocks', c_longlong),
            ('st_atimespec', c_timespec),
            ('st_mtimespec', c_timespec),
            ('st_ctimespec', c_timespec),
            ('st_ino', c_ulonglong)]
else:
    raise NotImplementedError('%s is not supported.' % _system)


class c_statvfs(Structure):
    _fields_ = [
        ('f_bsize', c_ulong),
        ('f_frsize', c_ulong),
        ('f_blocks', c_fsblkcnt_t),
        ('f_bfree', c_fsblkcnt_t),
        ('f_bavail', c_fsblkcnt_t),
        ('f_files', c_fsfilcnt_t),
        ('f_ffree', c_fsfilcnt_t),
        ('f_favail', c_fsfilcnt_t)]

if _system == 'FreeBSD':
    c_fsblkcnt_t = c_uint64
    c_fsfilcnt_t = c_uint64
    setxattr_t = CFUNCTYPE(c_int, c_char_p, c_char_p, POINTER(c_byte), c_size_t, c_int)
    getxattr_t = CFUNCTYPE(c_int, c_char_p, c_char_p, POINTER(c_byte), c_size_t)
    class c_statvfs(Structure):
        _fields_ = [
            ('f_bavail', c_fsblkcnt_t),
            ('f_bfree', c_fsblkcnt_t),
            ('f_blocks', c_fsblkcnt_t),
            ('f_favail', c_fsfilcnt_t),
            ('f_ffree', c_fsfilcnt_t),
            ('f_files', c_fsfilcnt_t),
            ('f_bsize', c_ulong),
            ('f_flag', c_ulong),
            ('f_frsize', c_ulong)]

class fuse_file_info(Structure):
    _fields_ = [
        ('flags', c_int),
        ('fh_old', c_ulong),
        ('writepage', c_int),
        ('direct_io', c_uint, 1),
        ('keep_cache', c_uint, 1),
        ('flush', c_uint, 1),
        ('padding', c_uint, 29),
        ('fh', c_uint64),
        ('lock_owner', c_uint64)]

class fuse_context(Structure):
    _fields_ = [
        ('fuse', c_voidp),
        ('uid', c_uid_t),
        ('gid', c_gid_t),
        ('pid', c_pid_t),
        ('private_data', c_voidp)]


# rewrite the above by with prototype names to be called:


prototype_getattr=CFUNCTYPE(c_int, c_char_p, POINTER(c_stat))
prototype_readlink=CFUNCTYPE(c_int, c_char_p, POINTER(c_byte), c_size_t)
prototype_getdir=c_voidp    # Deprecated, use readdir
prototype_mknod=CFUNCTYPE(c_int, c_char_p, c_mode_t, c_dev_t)
prototype_mkdir=CFUNCTYPE(c_int, c_char_p, c_mode_t)
prototype_unlink=CFUNCTYPE(c_int, c_char_p)
prototype_rmdir=CFUNCTYPE(c_int, c_char_p)
prototype_symlink=CFUNCTYPE(c_int, c_char_p, c_char_p)
prototype_rename=CFUNCTYPE(c_int, c_char_p, c_char_p)
prototype_link=CFUNCTYPE(c_int, c_char_p, c_char_p)
prototype_chmod=CFUNCTYPE(c_int, c_char_p, c_mode_t)
prototype_chown=CFUNCTYPE(c_int, c_char_p, c_uid_t, c_gid_t)
prototype_truncate=CFUNCTYPE(c_int, c_char_p, c_off_t)
prototype_utime=c_voidp     # Deprecated, use utimens
prototype_open=CFUNCTYPE(c_int, c_char_p, POINTER(fuse_file_info))
prototype_read=CFUNCTYPE(c_int, c_char_p, POINTER(c_byte), c_size_t, c_off_t, POINTER(fuse_file_info))
prototype_write=CFUNCTYPE(c_int, c_char_p, POINTER(c_byte), c_size_t, c_off_t, POINTER(fuse_file_info))
prototype_statfs=CFUNCTYPE(c_int, c_char_p, POINTER(c_statvfs))
prototype_flush=CFUNCTYPE(c_int, c_char_p, POINTER(fuse_file_info))
prototype_release=CFUNCTYPE(c_int, c_char_p, POINTER(fuse_file_info))
prototype_fsync=CFUNCTYPE(c_int, c_char_p, c_int, POINTER(fuse_file_info))
prototype_setxattr=setxattr_t
prototype_getxattr=getxattr_t
prototype_listxattr=CFUNCTYPE(c_int, c_char_p, POINTER(c_byte), c_size_t)
prototype_removexattr=CFUNCTYPE(c_int, c_char_p, c_char_p)
prototype_opendir=CFUNCTYPE(c_int, c_char_p, POINTER(fuse_file_info))
prototype_readdir=CFUNCTYPE(c_int, c_char_p, c_voidp, CFUNCTYPE(c_int, c_voidp, c_char_p, POINTER(c_stat), c_off_t), c_off_t, POINTER(fuse_file_info))
prototype_releasedir=CFUNCTYPE(c_int, c_char_p, POINTER(fuse_file_info))
prototype_fsyncdir=CFUNCTYPE(c_int, c_char_p, c_int, POINTER(fuse_file_info))
prototype_init=CFUNCTYPE(c_voidp, c_voidp)
prototype_destroy=CFUNCTYPE(c_voidp, c_voidp)
prototype_access=CFUNCTYPE(c_int, c_char_p, c_int)
prototype_create=CFUNCTYPE(c_int, c_char_p, c_mode_t, POINTER(fuse_file_info))
prototype_ftruncate=CFUNCTYPE(c_int, c_char_p, c_off_t, POINTER(fuse_file_info))
prototype_fgetattr=CFUNCTYPE(c_int, c_char_p, POINTER(c_stat), POINTER(fuse_file_info))
prototype_lock=CFUNCTYPE(c_int, c_char_p, POINTER(fuse_file_info), c_int, c_voidp)
prototype_utimens=CFUNCTYPE(c_int, c_char_p, POINTER(c_utimbuf))
prototype_bmap=CFUNCTYPE(c_int, c_char_p, c_size_t, POINTER(c_ulonglong))
# prototype_setattr=CFUNCTYPE(None,fuse_req_t, fuse_ino_t, c_stat_p, c_int, fuse_file_info_p) # lower level only used by chmod, call chmod (upper level)


class fuse_operations(Structure):
    _fields_ = [
        ('getattr',prototype_getattr),
        ('readlink',prototype_readlink),
        ('getdir',prototype_getdir),
        ('mknod',prototype_mknod),
        ('mkdir',prototype_mkdir),
        ('unlink',prototype_unlink),
        ('rmdir',prototype_rmdir),
        ('symlink',prototype_symlink),
        ('rename',prototype_rename),
        ('link',prototype_link),
        ('chmod',prototype_chmod),
        ('chown',prototype_chown),
        ('truncate',prototype_truncate),
        ('utime',prototype_utime),
        ('open',prototype_open),
        ('read',prototype_read),
        ('write',prototype_write),
        ('statfs',prototype_statfs),
        ('flush',prototype_flush),
        ('release',prototype_release),
        ('fsync',prototype_fsync),
        ('setxattr',prototype_setxattr),
        ('getxattr',prototype_getxattr),
        ('listxattr',prototype_listxattr),
        ('removexattr',prototype_removexattr),
        ('opendir',prototype_opendir),
        ('readdir',prototype_readdir),
        ('releasedir',prototype_releasedir),
        ('fsyncdir',prototype_fsyncdir),
        ('init',prototype_init),
        ('destroy',prototype_destroy),
        ('access',prototype_access),
        ('create',prototype_create),
        ('ftruncate',prototype_ftruncate),
        ('fgetattr',prototype_fgetattr),
        ('lock',prototype_lock),
        ('utimens',prototype_utimens),
        ('bmap',prototype_bmap),]
#        ('setattr',prototype_setattr),]

# http://bitbucket.org/vlasovskikh/fusepy-mirror/src/c421d4ddd8fb/fusell.py

def time_of_timespec(ts):
    return ts.tv_sec + ts.tv_nsec / 10 ** 9

def set_st_attrs(st, attrs):
    for key, val in attrs.items():
        if key in ('st_atime', 'st_mtime', 'st_ctime'):
            timespec = getattr(st, key + 'spec')
            timespec.tv_sec = int(val)
            timespec.tv_nsec = int((val - timespec.tv_sec) * 10 ** 9)
        elif hasattr(st, key):
            setattr(st, key, val)


_libfuse_path = find_library('fuse')
if not _libfuse_path:
    raise EnvironmentError('Unable to find libfuse')
_libfuse = CDLL(_libfuse_path)



_libfuse.fuse_get_context.restype = POINTER(fuse_context)


def fuse_get_context():
    """Returns a (uid, gid, pid) tuple"""
    ctxp = _libfuse.fuse_get_context()
    ctx = ctxp.contents
    return ctx.uid, ctx.gid, ctx.pid




# fuse_main_real (int argc, char *argv[], const struct fuse_operations *op, size_t op_size, void *user_data)
#    _libfuse.fuse_main_real(len(args), argv, pointer(fuse_ops), sizeof(fuse_ops), None)

def myfuse_main_real(args,fuse_ops):
    argv = (c_char_p * len(args))(*args)
    return _libfuse.fuse_main_real(len(args), argv, pointer(fuse_ops), sizeof(fuse_ops), None)


