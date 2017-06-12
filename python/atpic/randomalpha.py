#!/usr/bin/python3
import random
import string

import atpic.log
xx=atpic.log.setmod("INFO","randomalpha")

def possible():
    return [b'a',b'b',b'c',b'd',b'e',b'f',b'g',b'h',b'i',b'j',b'k']

def store():
    # returns a string of characters to store in elastice search
    # the string contains each of thepossible chars at least once
    stp=possible()
    maxi=20
    out=[]
    for achar in stp:
        rndlen=random.randint(1, maxi)
        for i in range(1,rndlen):
            out.append(achar)
    outs=b' '.join(out)
    # print(outs)
    return outs

def search():
    # returns a string of char to search
    stp=possible()
    out=[]
    randnb=random.randint(1,len(stp)-1)
    for i in range(0,randnb):
        j=random.randint(0,len(stp)-1)
        achar=stp[j]
        out.append(achar)
    # outs=b' '.join(out)
    # print(outs)
    return out



def myrandomfile():
    # do not use the tempfile module as it will cfreate the file
    yy=atpic.log.setname(xx,'myrandomfile')
    out=[]
    chars = string.ascii_lowercase + string.digits + string.ascii_uppercase
    for i in range(0,40):
        out.append(random.choice(chars))
    rfile=b'atpicfs_'+''.join(out).encode('utf8')
    atpic.log.debug(yy,'output=',rfile)
    return rfile

if __name__ == "__main__":
    print("alex","madon",sep="")
    for i in range(0,20):
        print(search())

    for i in range(0,20):
        print(store())
    print(myrandomfile())
