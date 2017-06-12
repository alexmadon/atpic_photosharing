#!/usr/bin/python3
# get the video thumb

# totem-video-thumbnailer
# see ../phplib/library_wrapper.php:    $thecommand="totem-video-thumbnailer file://".pic_dir($artistid,$galleryid,$secret,$picid)."/0.".$extension."  ".pic_dir($artistid,$galleryid,$secret,$picid)."/160.png  2>&1";


"""
       
    //transcode -i swimming.mpg -y jpg -o pics/back -c 0-1
    // to flip: -z (mpg)
    //transcode -i animation.avi -y jpg -Z 720x480 --export_asr 2 -o pics/background -D0 -J modfps --export_fps 29.97
    if ($background) $todevnull="> /dev/null";  // this is to send in background
    mymkdir(pic_dir($artistid,$galleryid,$secret,$picid)."/vf");  // vf=video frame
    //$thecommand="totem-video-thumbnailer file://".pic_dir($artistid,$galleryid,$secret,$picid)."/0.".$extension."  ".pic_dir($artistid,$galleryid,$secret,$picid)."/160.png  2>&1";
    $thecommand="ffmpegthumbnailer -f -s 160 -i ".pic_dir($artistid,$galleryid,$secret,$picid)."/0.".$extension."  -o ".pic_dir($artistid,$galleryid,$secret,$picid)."/160.png  2>&1";

    //print "$thecommand<br />";
    exec($thecommand,$results);
    
"""

import subprocess
import time

import atpic.log

xx=atpic.log.setmod("INFO","videothumb")

# film strip perforation imagemagick
# http://www.fmwconcepts.com/imagemagick/perforations/index.php
"""

# create a white rounded rectangle on black background 
convert -size 100x60 xc:black -fill white -stroke black \
          -draw "roundrectangle 20,10 80,50 20,15"  draw_rrect.png

convert -size 100x60 xc:black -fill white \
          -draw "roundrectangle 20,10 80,50 20,15"  draw_rrect.png


# a vertical bar 
# use mpr:{label} (memory program register)
convert -size 100x60 xc:black -fill white -stroke black \
        -draw "roundrectangle 20,10 80,50 20,15" -write mpr:filmhole +delete \
        -size 100x600 tile:mpr:filmhole oo.png


# put it as borders
# concatenate:
# http://superuser.com/questions/290656/combine-multiple-images-using-imagemagick


convert -size 100x60 xc:black -fill white -stroke black \
-draw "roundrectangle 20,10 80,50 20,15" -write mpr:filmhole +delete \
-size 100x600 tile:mpr:filmhole -write mpr:holes +delete \
mpr:holes in.jpg mpr:holes +append aa.png

"""

def totemvideothumbnailer(infile,outfile):
    yy=atpic.log.setname(xx,'totemvideothumbnailer')
    atpic.log.debug(yy,'input=',(infile,outfile))
    # options=[]
    time1=time.time()
    
    p1=subprocess.Popen(["totem-video-thumbnailer","--raw",infile.decode('utf8'),outfile.decode('utf8'),],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    
    (outdata,outerror)=p1.communicate()
    if p1.returncode!=0:
        atpic.log.debug(yy,"FAILURE on totem-video-thumbnailer, Trying ffmpegthumbnailer")
        p1=subprocess.Popen(["ffmpegthumbnailer","-s0","-i",infile.decode('utf8'),"-o",outfile.decode('utf8'),],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        
        (outdata,outerror)=p1.communicate()
    
    atpic.log.debug(yy,'return code=',p1.returncode) # should be zero 0
    time2=time.time()
    ittook=time2-time1
    atpic.log.debug(yy,"It took (seconds):",ittook)

    if p1.returncode==0:
        atpic.log.debug(yy,"Everything OK")
    else:
        atpic.log.debug(yy,"There was an error", (outdata,outerror))
    return (outdata,outerror)


def videothumbnailer(infile,outfile,size=0):
    try:
        program="ffmpegthumbnailer"
        output = subprocess.Popen(program, stdout=subprocess.PIPE).communicate()[0]
    except:
        try:

            # $thecommand="ffmpegthumbnailer -f -s 160 -i ".pic_dir($artistid,$galleryid,$secret,$picid)."/0.".$extension."  -o ".pic_dir($artistid,$galleryid,$secret,$picid)."/160.png  2>&1";
            # the -f adds film like borders
            program="totem-video-thumbnailer"
            output = subprocess.Popen(program, stdout=subprocess.PIPE).communicate()[0]
        except:
            try:
                program="totem-gstreamer-video-thumbnailer"
                output = subprocess.Popen(program, stdout=subprocess.PIPE).communicate()[0]
            except:
                # print "Error: you need totem-video-thumbnailer or totem-gstreamer-video-thumbnailer"
                raise Exception("Error: you need totem-video-thumbnailer or totem-gstreamer-video-thumbnailer")
    if size:
        list=[program, "-s", size, "file://"+infile, outfile]
    else:
        list=[program, "file://"+infile, outfile];
    output = subprocess.Popen(list, stdout=subprocess.PIPE).communicate()[0]
    # output=output.strip(" \n\t\r")
    print (output)
    return output


if __name__ == "__main__":
    print("Hi")
    infile=b"/home/madon/public_html/perso/entreprise/sql_current/site/atpic/python/tests/fixture/videos/better_MVI_5848.AVI"
    outfile=b"/tmp/vid1.png"
    totemvideothumbnailer_raw(infile,outfile)
