#!/usr/bin/python3
# image magick scaling and rotate forks
# should be run in a virtual machine for security

import subprocess
import re
import time
import sys

import atpic.log

xx=atpic.log.setmod("INFO","convert_image")


def convert_convert_1024(infile,outfile):
    convert_convert(infile,outfile,scale=b"1024x1024")
def convert_convert_600(infile,outfile):
    convert_convert(infile,outfile,scale=b"600x600")
def convert_convert_350(infile,outfile):
    convert_convert(infile,outfile,scale=b"350x350")
def convert_convert_160(infile,outfile):
    convert_convert(infile,outfile,scale=b"160x160")
def convert_convert_70(infile,outfile):
    convert_convert(infile,outfile,scale=b"70x70")


def convert_convert(infile,outfile,scale=b"600x600"):
    yy=atpic.log.setname(xx,'convert_convert')
    
    atpic.log.debug(yy,"input",(infile,outfile,scale))
    time1=time.time()

    p1=subprocess.Popen(["convert", "-scale",scale,"-quality","95",infile.decode('utf8'),outfile.decode('utf8')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

    (outdata,outerror)=p1.communicate()
    # print(dir(p1)) 
    atpic.log.debug(yy,"p1.returncode=",p1.returncode) # should be zero 0
    if p1.returncode==0:
        atpic.log.debug(yy,"Everything OK")
        atpic.log.debug(yy,"(outdata,outerror)=",(outdata,outerror))
    else:
        atpic.log.debug(yy,"There was an error", (outdata,outerror))

    time2=time.time()
    ittook=time2-time1
    atpic.log.debug(yy,"It took (seconds):",ittook)
    return (outdata,outerror)


if __name__ == "__main__":

    infile=b'/home/madon/jpg/866475.jpg'
    outfile=b'/tmp/tt.jpg'
    convert_convert(infile,outfile)
