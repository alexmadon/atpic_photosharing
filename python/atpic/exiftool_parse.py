#!/usr/bin/python3
"""
Parses the xml long output (-X -l)
of exiftool to extract the relevant info necessary for SQL and further processing

mime, video or image, size (for conversion)
"""

import atpic.xmlutils
import atpic.log

xx=atpic.log.setmod("INFO","exiftool_parse")

def parse(thexml):
    yy=atpic.log.setname(xx,'parse')
    important=atpic.xmlutils.get_exif(thexml)
    atpic.log.debug(yy,'important=',important)
    sizes=important[1]
    sizes_splitted=sizes.split(b'x')
    if len(sizes_splitted)==2:
        (width,height)=sizes_splitted
    else:
        (width,height)=(b'',b'')
    important2=important[0:1]+(width,height)+important[2:]
    atpic.log.debug(yy,'important2=',important2)
    return important2
