#!/usr/bin/python3
import math

import atpic.log
import atpic.signed
import atpic.mybytes

xx=atpic.log.setmod("INFO","coordinates")


# we put a 0 if on the left, and a 1 if on the right
# we put a 0 if on the bottom, and a 1 if on the top
# resolution is the number of bits
# depending on the resolution (wordlen), you can store in bool, byte, short, int, long
# lon -180,+180
# lat -90, +90

# int are unsigned, packed unsiged,
# then stored in elasticesearch packed and signed

def binhelp(nb,wlen):
    yy=atpic.log.setname(xx,'binhelp')
    # converts a nb to bits help
    if wlen<=8:
        wlenl=8
    elif  wlen<=16:
        wlenl=16
    elif  wlen<=32:
        wlenl=32
    elif  wlen<=64:
        wlenl=64

    st=bin(nb)
    sts=st[2:]
    stsj=sts.rjust(wlenl,'0')
    stsjf='0b'+stsj
    # atpic.log.debug(yy,'bits',stsjf)
    return stsjf

def large_len(wlen):
    yy=atpic.log.setname(xx,'large_len')
    if wlen<=4:
        wlenw=8
    elif  wlen<=8:
        wlenw=16
    elif  wlen<=16:
        wlenw=32
    elif  wlen<=32:
        wlenw=64
    return wlenw

# ====================================================
#
#   conversion between degree and int for lon OR lat
#
# ====================================================
def get_delta(wlen,maxcoord):
    yy=atpic.log.setname(xx,'get_delta')
    maxunsigned=(1<<wlen)-1
    delta=2*maxcoord/(maxunsigned+1)
    atpic.log.debug(yy,'delta',delta)
    return delta

def get_one_interval(coord,wlen,maxcoord=180):
    # returns an interval, one to one map
    yy=atpic.log.setname(xx,'convert_one_interval')
    # test: f(180)=f(-180)
    atpic.log.debug(yy,'input=',coord,wlen)
    epsilon=0.00000000001
    if coord>=maxcoord:
        coord=maxcoord-epsilon
    maxunsigned=(1<<wlen)-1
    delta=get_delta(wlen,maxcoord)
    i=int((((coord+maxcoord)/delta))%(maxunsigned+1))
    j=int((((coord+maxcoord)/delta)+1)%(maxunsigned+1))
    xi=i*delta - maxcoord
    xj=j*delta - maxcoord
    if xj<xi:
        atpic.log.debug(yy,'warn:',xj,'<',xi)
        xj=-xj
        j=maxunsigned+1
    atpic.log.debug(yy,'(i,j),(xi,xj)',(i,j),(xi,xj))
    return ((i,j),(xi,xj))

def identify_facet(xmin,xmax,maxcoord=180):
    # given a facet, get the resolution and integer encoding
    # get the resolution:
    yy=atpic.log.setname(xx,'identify_facet')
    atpic.log.debug(yy,'input',(xmin,xmax,maxcoord))
    dx=xmax-xmin
    atpic.log.debug(yy,'dx',dx)
    dxlog=round(math.log(2*maxcoord/dx,2))
    wlen=dxlog
    # first get the center
    xcenter=(xmax+xmin)/2
    ((i,j),(xi,xj))=get_one_interval(xcenter,wlen,maxcoord=maxcoord)
    atpic.log.debug(yy,'output',(wlen,(i,j),(xi,xj)))
    return  (wlen,(i,j),(xi,xj))

def identify_bounds2facet(xmin,xmax,ymin,ymax):
    yy=atpic.log.setname(xx,'identify_bounds2facet')
    (wlenx,(xi,xj),(xxi,xxj))=identify_facet(xmin,xmax,maxcoord=180)
    (wleny,(yi,yj),(yyi,yyj))=identify_facet(ymin,ymax,maxcoord=90)
    if wlenx!=wleny:
        raise Exception('both resolutions should be the same!')
    packed=pack(xi,yi,wlenx)
    return (packed,wlenx)

# in practice:
# googlemaps send a xmin,ymin,xmax,ymax
# we need exact facets 
# first get the resolution

def get_facets(xmin,xmax,ymin,ymax,nbmin=6,nbmax=19):
    # first get the resolution
    yy=atpic.log.setname(xx,'get_facets')
    dx=xmax-xmin
    dy=ymax-ymin
    dxlog=math.log(360/dx,2)
    dylog=math.log(180/dy,2)

    mylog=round(max(dxlog,dylog))
    # then we get the interval containing the center at this resolution

    zonelist=[]
    pathlist=[]
    res=None
    found=False
    afound=False
    for alog in range(mylog,mylog+4): # try several resolutions
        if not found:
            atpic.log.debug(yy,'doing resolution ------ ',alog)
            if alog>26 or alog==0:
                pass
            else:
                wlen=alog
                ((xi_min,xj_min),(xci_min,xcj_min))=get_one_interval(xmin,wlen,maxcoord=180)
                ((xi_max,xj_max),(xci_max,xcj_max))=get_one_interval(xmax,wlen,maxcoord=180)
                
                ((yi_min,yj_min),(yci_min,ycj_min))=get_one_interval(ymin,wlen,maxcoord=90)
                ((yi_max,yj_max),(yci_max,ycj_max))=get_one_interval(ymax,wlen,maxcoord=90)
                atpic.log.debug(yy,xi_min,'<xi<',xj_max,' (',xci_min,'<x<',xcj_max,')')
                atpic.log.debug(yy,yi_min,'<yi<',yj_max,' (',yci_min,'<y<',ycj_max,')')
                nb=(xj_max-xi_min)*(yj_max-yi_min)
                atpic.log.debug(yy,'nb',nb)
                # now you can calculate how many factes you have in the rectangle
                
                if nb>nbmin:
                    found=True
                    deltax=get_delta(wlen,180)
                    deltay=get_delta(wlen,90)
                    for i in range(xi_min,xj_max):
                        for j in range(yi_min,yj_max):
                            atpic.log.debug(yy,'(i,j)',(i,j))
                            zonelist.append(pack(i,j,wlen))
                    for i in range(xi_min,xj_max):
                        for j in range(yi_min,yj_max):
                            xi=atpic.mybytes.float2bytes(i*deltax-180)
                            yj=atpic.mybytes.float2bytes(j*deltay-90)
                            xid=atpic.mybytes.float2bytes((i+1)*deltax-180)
                            yjd=atpic.mybytes.float2bytes((j+1)*deltay-90)
                            # ERROR at 180 and 90?
                            pathlist.append(b'/'+xi+b'/'+xid+b'/'+yj+b'/'+yjd)
                    res=(wlen,zonelist,pathlist)

    atpic.log.debug(yy,'res',res)
    atpic.log.debug(yy,'output',pathlist)
    return pathlist












# =====================================================
#
#  Packing/Unpaking bits: this is not lossy
#
# =====================================================

def pack(lonb,latb,wlen):
    # stores two int coord into one
    # we pack each bit alternatively, one from log, one from lat
    # wlen is the length of the coding of each lon
    # so pack length is the double
    # 
    yy=atpic.log.setname(xx,'pack')
    

    # now package:
    # this is NOT lossy
    atpic.log.debug(yy,'packing',(lonb,binhelp(lonb,wlen),latb,binhelp(latb,wlen),wlen))
    res=0
    wlenw=large_len(wlen)

    maxint=(1<<wlen)-1
    if lonb>maxint or latb>maxint:
        raise Exception('WARNING!!!! maxint',maxint,'while max',lonb,latb)
    for i in range(0,wlenw):
        # http://stackoverflow.com/questions/2643722/how-to-get-nth-bit-from-right-in-a-binary-equivalent-of-an-integer-in-php
        # extract the i-th bit:
        loni=lonb & (1<<i)
        lati=latb & (1<<i)
        atpic.log.debug(yy,'i',i,'loni',loni,'lati',lati,end= ' ')
        # now slide it
        lonit=loni << i
        latit=lati << (i+1) 
        atpic.log.debug(yy,'lonit',lonit,binhelp(lonit,wlenw),'latit',latit,binhelp(latit,wlenw))
        res=res | lonit | latit # combine
    reshelp=binhelp(res,wlenw)
    atpic.log.debug(yy,'packed:',res,reshelp)
    # convert to signed:
    res=atpic.signed.unsigned2signed(res,wlenw)

    atpic.log.debug(yy,'will return',res,bin(res))
    return res

# this is like a vector:
# units on X axis, tens on the Y axis
# average of vector is the average of the sums.

def unpack(packed, wlen):
    # http://en.wikipedia.org/wiki/Integer_%28computer_science%29
    # http://en.wikipedia.org/wiki/Signed_number_representations
    # http://stackoverflow.com/questions/1375897/how-to-get-the-signed-integer-value-of-a-long-in-python
    # Two's complement
    # ctypes 
    # c_byte 	char 	int/long
    # c_ubyte 	unsigned char 	int/long
    # c_short 	short 	int/long
    # c_ushort 	unsigned short 	int/long
    # c_int 	int 	int/long
    # c_uint 	unsigned int 	int/long
    # c_long 	long 	int/long
    # c_ulong 	unsigned long 	int/long



    # unpacks a packed bits sequence into lon and lat
    # sould be idempotent with pack()
    yy=atpic.log.setname(xx,'unpack')
    atpic.log.debug(yy,'input(packed, wlen)',(packed, wlen))
    # convert signed to unsigned:
    wlenw=large_len(wlen)
    packed=atpic.signed.signed2unsigned(packed,wlenw)
    atpic.log.debug(yy,binhelp(packed,wlenw))
    lonb=0
    latb=0
    for i in range(0,wlenw):
         rest=i%2
         pc= packed & (1<<i)
         shifter=(int(i/2)+rest)
         pcc= pc >> shifter
         atpic.log.debug(yy,'(i,rest,shifter)',(i,rest,shifter))
         if rest==1:
             latb=latb|pcc
         else:
             lonb=lonb|pcc
         atpic.log.debug(yy,'i',i,binhelp(pc,wlenw),binhelp(pcc,wlenw))
    atpic.log.debug(yy,'unpacked (lon,lat)',(binhelp(lonb,wlen),binhelp(latb,wlen)))
    atpic.log.debug(yy,'output=(lonb,latb)',(lonb,latb))
    return (lonb,latb)

def facet2square(packed,wlen):
    # return a square xmin, ymin, xmax, ymax
    # /resolution/packed
    # /resolution/xint/yint

    yy=atpic.log.setname(xx,'facet2square')
    packed=atpic.mybytes.bytes2int(packed)
    wlen=atpic.mybytes.bytes2int(wlen)



    (lonb,latb)=unpack(packed, wlen)
    atpic.log.debug(yy,lonb,latb)
    (lon1,lat1)=unconvert_coord_int2degree(lonb,latb, wlen)
    atpic.log.debug(yy,lon1,lat1)
    (lon2,lat2)=unconvert_coord_int2degree(lonb+1,latb+1, wlen)
    lon1=atpic.mybytes.int2bytes(lon1)
    lat1=atpic.mybytes.int2bytes(lat1)
    lon2=atpic.mybytes.int2bytes(lon2)
    lat2=atpic.mybytes.int2bytes(lat2)
    path=b'/'+lon1+b'/'+lat1+b'/'+lon2+b'/'+lat2
    return path

if __name__=="__main__":
    print('hi3')

