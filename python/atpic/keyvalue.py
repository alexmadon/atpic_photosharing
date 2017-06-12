"""
KEY,VALUE

alexmadon|1:ctime:atime
u1|alexmadon


ug1:/|9999:ctime:atime (uid:path|gid:ctime:atime)
ug1:/dir1/dir2/dir3|99:ctime:atime (uid:path|gid:ctime:atime)


g99|subdir1,subdir2,subdir3 (readdir)


KEY,VALUE + ala keyspace (prune getlist)



======for keyspace=====

keyspace has prune and listkeyvalues



getattr (stat)

u:alexmadon,1|999 (uid,root gid)
U:1,alexmadon,999



u:1:g:999:/dir1,ctime,atime

u:1:/,G,gid,ctime,atime
u:1:/dir1,G,gid,ctime,atime
u:1:/dir2,G,gid,ctime,atime
u:1:/dir3,G,gid,ctime,atime
u:1:/dir1/dir3,G,gid,ctime,atime
u:1:/dir1/dir5,G,gid,ctime,atime
u:1:/dir1/dir6,G,gid,ctime,atime



u:1:g:66:pic1,p,pid,ctime,atime
u:1:g:66:pic2,p,pid,ctime,atime
u:1:g:66:pic3,p,pid,ctime,atime



readdir is difficult to implement

u1:g:99,folder1,folder2,......
or
u1:g:99:folder1,dummy
u1:g:99:folder2,dummy
and then a GET listkeys (no GET listkeyvalues necessary as dummy value)

rename



unlink


rmdir



write

create a new picture

"""
