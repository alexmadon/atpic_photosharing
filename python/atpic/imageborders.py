#!/usr/bin/python3
#
"""
convert -size 100x60 xc:black -fill white -stroke black \
-draw "roundrectangle 20,10 80,50 20,15" -write mpr:filmhole +delete \
-size 100x600 tile:mpr:filmhole -write mpr:holes +delete \
mpr:holes in.jpg mpr:holes +append aa.png

"""
import math
import subprocess
import time

import atpic.log
import atpic.mybytes


xx=atpic.log.setmod("INFO","imageborders")

def put_borders(infile,outfile,args):
    
    # put a film like performation borders
    yy=atpic.log.setname(xx,'put_borders')

    [fheight]=args
    height=atpic.mybytes.bytes2int(fheight)
    factorx=5
    factory=8
    size1=str(math.floor(height/factorx))+'x'+str(math.floor(height/factory))
    size2=str(math.floor(height/factorx))+'x'+str(height)
    factor3x=25 # gives the relative size of each hole
    factor3y=35 # gives the relative size of each hole
    factor2=60 # gives the curvature 
    rectangle=str(math.floor(height/factor3x))+','+str(math.floor(height/factor3y))
    rectangle+=" "
    rectangle+=str(math.floor(height/factorx-height/factor3x))+','+str(math.floor(height/factory-height/factor3y))
    rectangle+=" "
    rectangle+=str(math.floor(height/factor2))+','+str(math.floor(height/factor2))

    # 20,10 80,50 20,15"
    atpic.log.debug(yy,'input=',(infile,outfile))
    # options=[]
    time1=time.time()
    command=["convert",
         "-size",size1, "xc:black","-fill","white","-stroke","black",
         "-draw","roundrectangle "+rectangle,"-write","mpr:filmhole","+delete",
         "-size",size2,"tile:mpr:filmhole","-write","mpr:holes","+delete",
         "mpr:holes",
         infile.decode('utf8'),
         "mpr:holes","+append", 
         outfile.decode('utf8'),
         ]
    atpic.log.debug(yy,'command=',command)
    p1=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

    (outdata,outerror)=p1.communicate()
    # print(dir(p1)) 
    atpic.log.debug(yy,'return code=',p1.returncode) # should be zero 0
    time2=time.time()
    ittook=time2-time1
    atpic.log.debug(yy,"It took (seconds):",ittook)

    if p1.returncode==0:
        atpic.log.debug(yy,"Everything OK")
    else:
        atpic.log.debug(yy,"There was an error", (outdata,outerror))
    return (outdata,outerror)


if __name__ == "__main__":
    print("Hi")
    infile=b"/home/madon/tmp/in.jpg" # 360
    outfile=b"/tmp/border1.png"
    (outdata,outerror)=put_borders(infile,outfile,[360])
    print(outdata,outerror)


    infile=b"/home/madon/tmp/in1.png" # 144
    outfile=b"/tmp/border2.png"
    (outdata,outerror)=put_borders(infile,outfile,[144])
    print(outdata,outerror)
