#!/usr/bin/python3
# import logging
import atpic.log
from atpic.mybytes import *
import atpic.libpqalex
from atpic.redisconst import *
import atpic.hashat

# NOT USED ANYMORE!!!!!!!!!!!!!!!!!!!!!!!!!!!1

xx=atpic.log.setmod("INFO","idbased")

# ======== new =========
# alex.atpiccontent.com/123_xxxxxxxxxxxx.jpg
# DNSname               PID encrypted (hash(PID)+path_on_disk)
# xxxxx encrypt(hash(PID)+pathondisk)
# this is the minimum URL
# no resolution needed (?)
# PID is there to randomize
# extension is there to be able to serve without MIME

# transforms normalized URLs into parameters
# example of url normalized:
# b'alex/3333_1024_2012_12_31_23_59_aghhdjkskdslsdlsdllsdlsdldsd.jpg'
# HTTP:
# http://alex.w.atpic.com/3333_1024_2012_12_31_23_59_aghhdjkskdslsdlsdllsdlsdldsd.jpg
# that is:
# http://{uname}.w.atpic.com/{pid}_{resolution}_{year}_{month}_{day}_{hour}_{minute}_{hash}.{extension}
# NO webdav, no FTP on ID based!
# Notes:
# 1) there is no gallery ID in the URL (that allows quick moves from one gallery to another)
# 2) there is no permission info in the URL (like mode or secret) except the permission hash
# 
# ###############################################
# whole process is:
# 1) HTTP: http://alex.w.atpic.com/3333_1024_2012_12_31_23_59_aghhdjkskdslsdlsdllsdlsdldsd.jpg
# 2) Fuse FS ID based: /atpicidbased/alex/3333_1024_2012_12_31_23_59_aghhdjkskdslsdlsdllsdlsdldsd.jpg
#  a) Redis ID based: 
#    u_alex [uid,partition] [{status,IPs,partition,version}]
#      - [uid and partion] are necessary as file is stored using it on filisesystem
# check the hash
#  b) SQL
# 3) ext3 filesystem: /sdc1/store/2012/12/31/23/59/1_3333_1024.jpg




# ========================
# storepath functions:
# ========================

# better scheme:
# just an encrypted string that gives once decoded everything
# or limit to uid, pid, resolution, extension
# that won't change
# i.e call
# XX=encrypt(uid, pid, resolution, extension,real_path)
# call uid_pid_res_XX.jpg
# WARNING: real_path may change?
# partition may change? or is that stored in redis?
# with real path it is mnore flexible, as allows things like bulk upload

def idpath2storepath(path,uid,partition):
    """ 
    transforms:
    b'/alex/3333_1024_2012_12_31_23_59_assaasasasasasaaaasas.jpg'
    into:
    b'/sdc1/store/2012/12/31/23/59/1_222_3333_1024.jpg'
    Just need to check permission and partition
    """
    yy=atpic.log.setname(xx,'idpath2storepath')
    atpic.log.debug(yy,'input',(path,uid,partition))
    splitted=path.split(b'/')
    atpic.log.debug(yy,splitted)
    (empty,uname,fname)=splitted
    atpic.log.debug(yy,'uname,fname',uname,fname)
    (pid,resolution,year,month,day,hour,minute,ahashext)=fname.split(b'_')
    (ahash,extension)=ahashext.split(b'.')

    # validate the hash
    isvalid=atpic.hashat.checkhash(ahash,pid,resolution,year,month,day,hour,minute)
    atpic.log.debug(yy,'isvalid',isvalid)
    if not isvalid:
        raise Exception("hash is not valid! not authorized")
    storepath_list=[]
    storepath_list.append(partition)
    storepath_list.append(b'store')
    storepath_list.append(year)
    storepath_list.append(month)
    storepath_list.append(day)
    storepath_list.append(hour)
    storepath_list.append(minute)
    storepath_list.append(uid+b'_'+pid+b'_'+resolution+b'.'+extension)
    storepath=b'/'.join(storepath_list)
    atpic.log.debug(yy,'return',storepath)
    return (isvalid,storepath)

# transforms parameters into URLs
# IS Really time necessary for a read only filesystem?????
# in fact it seems we only need a) partition of user
# for this ultra simple fuse filesystem

# conclusion: NOT NECESSARY!!!!

if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    pass
