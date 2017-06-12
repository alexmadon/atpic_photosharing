#!/usr/bin/python3

# this is used 
# 1) by idbased filesystems
# 2) and by the presentation XML layer


import hashlib
import base64


import atpic.opensslat

import atpic.log

xx=atpic.log.setmod("INFO","hashat")
def getkey():
    return b'secretkey4picsVErYlong!'


def forge_pathstorehash(pid,resolutioncode,pathstore,partition,extension):
    # display full hash
    hashvalue=dohash(pid,resolutioncode,pathstore)
    hashvalue=partition+hashvalue+b'.'+extension
    return hashvalue

def dohash(pid,resolution,pathondisk):
    # this uses symmetric key encryption
    # + hash to randomize (?)
    # randomization is based on PID and resoklution 
    # as could get higher resolution from lower resolution if not
    yy=atpic.log.setname(xx,'dohash')
    m=hashlib.md5()
    m.update(pid+b'_'+resolution)
    hexd=m.hexdigest()
    randomizer=hexd[:4].encode('utf8') # take the first characters
    astring=randomizer+pathondisk
    key=getkey()
    astring_enc=atpic.opensslat.encrypt(astring,key)
    astring_b64 = base64.urlsafe_b64encode(astring_enc)
    atpic.log.debug(yy,'output=',astring_b64)
    return astring_b64

def undohash(ahash):
    yy=atpic.log.setname(xx,'undohash')
    astring = base64.urlsafe_b64decode(ahash)
    print(astring)
    key=getkey()
    astring_dec=atpic.opensslat.encrypt(astring,key,enc=0)

    return astring_dec

"""
def dohash(pid,resolution,year,month,day,hour,minute):
    # should it depend on 'extension'?
    # no, because if extension is wrong, then file will not be found anyway
    # why not a simple hash based on PID, resolution and store date?
    yy=atpic.log.setname(xx,'dohash')
    atpic.log.debug(yy,'input',(pid,resolution,year,month,day,hour,minute))
    m=hashlib.md5()
    toencode=b'gloseed'+b'_'+pid+b'_'+resolution+b'_'+year+b'_'+month+b'_'+day+b'_'+hour+b'_'+minute
    m.update(toencode)
    hexd=m.hexdigest()
    hash=hexd.encode('utf8')
    atpic.log.debug(yy,'return',hash)
    return hash

def checkhash(ahash,pid,resolution,year,month,day,hour,minute):
    # checks that the hash is valid
    # return True is valid, False if not valid
    yy=atpic.log.setname(xx,'checkhash')
    hashex=dohash(pid,resolution,year,month,day,hour,minute)
    if hashex==ahash:
        res=True
    else:
        res=False
    atpic.log.debug(yy,'output',res)
    return res
"""



# for elastic search:
# we have the datestore, the mode
# needs a function(mode,uid,aid) that returns
# authorized, watermarked (or not authorized but should never happen as we already filter)
# cf autorize.py




if __name__ == "__main__":
    print("hi")

    a=dohash(b'1236',b'600',b'/sda1/pic/133333333332347.jpg')
    print(a)
    print(undohash(a))
