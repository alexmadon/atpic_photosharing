# wrapper around the dcraw utility

# dcraw -i : identifies


import subprocess
import re
import sys
import time


import atpic.log

xx=atpic.log.setmod("INFO","dcraw")


def identify(filename):
    (output,outerr) = subprocess.Popen(["dcraw", "-i",filename], stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
    output=str(output)
    output=output.strip(" \n\t\r")

    p = re.compile('(.*) is a ([^ ]+) (.*) image')
    m = p.match(output)
    if (m):
        output="<israw/><make>%s</make><model>%s</model>" % (m.group(2),m.group(3))
    else:
        output="<noraw/>"
    return output



def ufraw_convert(infile,outfile):

    """
    ufraw-batch --help
    --out-type=ppm|tiff|tif|png|jpeg|jpg|fits
    Output file format (default ppm).
    --output=FILE         Output file name, use '-' to output to stdout.
    """
    yy=atpic.log.setname(xx,'ufraw_convert')
    atpic.log.debug(yy,'input=',(infile,outfile))
    time1=time.time()

    p1=subprocess.Popen(["ufraw-batch", "--out-type=jpg","--output="+outfile.decode('utf8'),"--overwrite",infile.decode('utf8')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

    (outdata,outerror)=p1.communicate()
    # print(dir(p1)) 
    atpic.log.debug(yy,'return code=',p1.returncode) # should be zero 0
    time2=time.time()
    ittook=time2-time1
    atpic.log.debug(yy,"It took (seconds):",ittook)

    if p1.returncode==0:
        atpic.log.debug(yy,"Everything OK")
        atpic.log.debug(yy,"(outdata,outerror)=",(outdata,outerror))
    else:
        atpic.log.debug(yy,"There was an error", (outdata,outerror))
    return (outdata,outerror)
