#!/usr/bin/python3
import math
import re

import atpic.log
import atpic.mybytes

xx=atpic.log.setmod("INFO","aperture")


# give an aperture F number
# b'5.6'
# returns an integer (byte, short, long)
# byte 8 , short 16, integer 32, and long 64
# suitable for elasticsearch
# intergers are signed, so il N bits lenght
# between -2^(N-1) and 2^(N-1)-1
# ./_site/guide/reference/mapping/core-types.html

def aperture_clean(a):
    # input can be any common f representation:
    # f/8.0, 8.0 80/10
    # output is the number itself in a float representation
    yy=atpic.log.setname(xx,'aperture_clean')
    atpic.log.debug(yy,a)
    if re.match(b'[^0-9]{2}',a):
        a=a[2:]
    elif re.match(b'[^0-9]{1}',a):
        a=a[1:]
    if re.search(b'/',a):
        atpic.log.debug(yy,'match')
        numbers=a.split(b'/')
        atpic.log.debug(yy,'numbers',numbers)
        if len(numbers)==2:
            (b,c)=numbers
            bn=atpic.mybytes.bytes2float(b)
            cn=atpic.mybytes.bytes2float(c)
            an=bn/cn
            a=atpic.mybytes.float2bytes(an,fmt='%0.1f')
    return a

def fnumber2int(f):
    return fnumber2int_withbits(f,8)

def fnumber2int_withbits(f,bitsnb):
    yy=atpic.log.setname(xx,'fnumber2int')
    atpic.log.debug(yy,'input',f,bitsnb)
    # get the allowed range of values
    mini=-math.pow(2,bitsnb-1)
    maxi=+math.pow(2,bitsnb-1)-1
    atpic.log.debug(yy,mini,maxi)
    # f mini and maxi
    # fmini=1
    # fmaxi=64
    nmini=0 # sqrt(2)^0=1
    nmaxi=12 # sqrt(2)^12=64
    # convert input f to float

    af=atpic.mybytes.bytes2float(f)
    if af<1.0:
        af=1.0
    elif af> 64:
        af=64.0
    # x^(n/2)=f
    # n=log2(f)
    n=2*math.log(af,2)
    atpic.log.debug(yy,n)

    # scale
    # 0 -> 12
    # -mini -> maxi
    sn=(n*(math.pow(2,bitsnb)-1)/12) - math.pow(2,bitsnb-1)
    atpic.log.debug(yy,sn)
    roundsn=round(sn)
    
    theint=atpic.mybytes.int2bytes(roundsn)
    return theint


def f4elasticsearch(a):
    return fnumber2int(aperture_clean(a))


if __name__ == "__main__":
    f=f4elasticsearch(b'5.6')
    print(f)
