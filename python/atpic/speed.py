#!/usr/bin/python3
import math
import re

import atpic.log
import atpic.mybytes

xx=atpic.log.setmod("INFO","speed")


# give an aperture F number
# b'5.6'
# returns an integer (byte, short, long)
# byte 8 , short 16, integer 32, and long 64
# suitable for elasticsearch
# intergers are signed, so il N bits lenght
# between -2^(N-1) and 2^(N-1)-1
# ./_site/guide/reference/mapping/core-types.html

def speed_clean(a):
    # converts b'10/500' to a float represented a bytes
    yy=atpic.log.setname(xx,'speed_clean')
    atpic.log.debug(yy,a)
    if re.search(b'/',a):
        atpic.log.debug(yy,'match')
        numbers=a.split(b'/')
        atpic.log.debug(yy,'numbers',numbers)
        if len(numbers)==2:
            (b,c)=numbers
            bn=atpic.mybytes.bytes2float(b)
            cn=atpic.mybytes.bytes2float(c)
            an=bn/cn
            a=atpic.mybytes.float2bytes(an,fmt='%0.8f')
    return a

def speed2int(f):
    return speed2int_withbits(f,8)

def speed2int_withbits(speed,bitsnb):
    yy=atpic.log.setname(xx,'speed2int')
    atpic.log.debug(yy,'input',speed,bitsnb)
    # 256 seconds = 2^8
    # 64 seconds = 2^6
    # .000061 seconds = 2^-14
    speedf=atpic.mybytes.bytes2float(speed)
    speedlog2=math.log(speedf,2)
    atpic.log.debug(yy,'speedlog2',speedlog2)
    # scale between -14 and +8
    nmaxi=8
    nmini=-14
    scaledmaxi=math.pow(2,bitsnb-1)-1
    scaledmini=-math.pow(2,bitsnb-1)
    n=speedlog2
    # (n-nmini)/(nmaxi-nmini)=(s-scaledmini)/(scaledmaxi-scaledmini)
    speedscaled=(n-nmini)*(scaledmaxi-scaledmini)/(nmaxi-nmini)+scaledmini
    # no overflow
    if speedscaled > scaledmaxi:
        speedscaled=scaledmaxi
    elif speedscaled < scaledmini:
        speedscaled=scaledmini
    atpic.log.debug(yy,speedscaled)
    roundss=round(speedscaled)
    theint=atpic.mybytes.int2bytes(roundss)

    return theint


def speed4elasticsearch(s):
    return speed2int(speed_clean(s))
