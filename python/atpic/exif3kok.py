#!/usr/bin/python3

# import logging
import atpic.log
import re
import struct


import atpic.exif3k as exif3k

xx=atpic.log.setmod("INFO","exif3kok")





def bytes2int(thebytes,intel):
    yy=atpic.log.setname(xx,'bytes2int')
    # atpic.log.debug(yy,"bytes2int",thebytes,"intel %s" % intel)
    if intel:
        return bytes2int_intel(thebytes)
    else:
        return bytes2int_motorola(thebytes)
# extract multibyte integer in Motorola format (little endian) LSB
def bytes2int_motorola(thebytes):
    yy=atpic.log.setname(xx,'bytes2int_motorola')
    x = 0
    for c in thebytes:
        x = (x << 8) | c
    return x

# extract multibyte integer in Intel format (big endian) MSB
def bytes2int_intel(thebytes):
    yy=atpic.log.setname(xx,'bytes2int_intel')
    x = 0
    y = 0
    for c in thebytes:
        x = x | c << y
        y = y + 8
    return x

def bytes_per_component(value):
    yy=atpic.log.setname(xx,'bytes_per_component')
    if value in (1,2,6,7):
        return 1
    elif value in (3,8):
        return 2
    elif value in (4,9,11):
        return 4
    elif value in (5,10,12):
        return 8
    else:
        return 0

# ratio object that eventually will be able to reduce itself to lowest
# common denominator for printing
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def display_data_value(tag_number,new_data_value_bytes,data_format,bytes_per_compo,components_nb,adic,intel):
    yy=atpic.log.setname(xx,'display_data_value')

    atpic.log.info(yy,"display_data_value( %s %s %s %s %s %s)" % (adic[tag_number],new_data_value_bytes,data_format,bytes_per_compo,components_nb,intel))
        

    """
    Type
    The following types are used in Exif:
    1 = BYTE            An 8-bit unsigned integer.,
    2 = ASCII           An 8-bit byte containing one 7-bit ASCII code. The final byte is terminated with NULL.,
    3 = SHORT           A 16-bit (2 -byte) unsigned integer,
    4 = LONG            A 32-bit (4 -byte) unsigned integer,
    5 = RATIONAL       Two LONGs. The first LONG is the numerator and the second LONG expresses the denominator.,
    7 = UNDEFINED       An 8-bit byte that can take any value depending on the field definition,
    9 = SLONG           A 32-bit (4 -byte) signed integer (2's complement notation),
   10 = SRATIONAL       Two SLONGs. The first SLONG is the numerator and the second SLONG is the denominator.

                        """

    if data_format==1:
        atpic.log.info(yy,"BYTE") # An 8-bit unsigned integer.
    elif data_format==2:
        atpic.log.info(yy,"ASCII") # An 8-bit byte containing one 7-bit ASCII code. The final byte is terminated with NULL.,
        data_string=new_data_value_bytes.decode('utf8')
        data_string=data_string.strip(' \t\n')
        atpic.log.info(yy,"ASCII '%s'" % data_string)
    elif data_format==3:
        atpic.log.info(yy,"SHORT") # A 16-bit (2 -byte) unsigned integer,
    elif data_format==4:
        atpic.log.info(yy,"LONG") # A 32-bit (4 -byte) unsigned integer,
    elif data_format==5:
        atpic.log.info(yy,"RATIONAL") # Two LONGs. The first LONG is the numerator and the second LONG expresses the denominator.,
        num=new_data_value_bytes[0:4]
        den=new_data_value_bytes[4:8]
        atpic.log.info(yy,"RATIONAL %s %s" % (num,den))
        num=bytes2int(num,intel)
        den=bytes2int(den,intel)
        atpic.log.info(yy,"RATIONAL %s/%s" % (num,den))
        div = gcd(num, den)
        if div > 1:
            num = int(num / div)
            den = int(den / div)
        atpic.log.info(yy,"RATIONAL %s/%s" % (num,den))

    # elif data_format==6:
    #    atpic.log.info(yy,"")An 8-bit byte that can take any value depending on the field definition,
    elif data_format==7:
        atpic.log.info(yy,"UNDEFINED") # An 8-bit byte that can take any value depending on the field definition,
    # elif data_format==8:
    #    atpic.log.info(yy,"")
    elif data_format==9:
        atpic.log.info(yy,"SLONG") # A 32-bit (4 -byte) signed integer (2's complement notation),
    elif data_format==10:
        atpic.log.info(yy,"SRATIONAL") # Two SLONGs. The first SLONG is the numerator and the second SLONG is the denominator.




def process_ifd_entry(f,tiffstart,offset_ifd,offset_ifd_entry,intel,adic):
    yy=atpic.log.setname(xx,'process_ifd_entry')
    f.seek(tiffstart+offset_ifd_entry)
    entry=f.read(12)
    tag_number_bytes=entry[0:2]
    data_format_bytes=entry[2:4]
    components_nb_bytes=entry[4:8]
    datavalue_bytes=entry[8:12]
    atpic.log.debug(yy,"Entry %s %s %s %s" % (tag_number_bytes,data_format_bytes,components_nb_bytes,datavalue_bytes))
    tag_number=bytes2int(tag_number_bytes,intel)
    atpic.log.debug(yy,"tag: 0x{:04X}".format(tag_number))

    # special case where you have to follow
    if tag_number==0x8769:
        atpic.log.debug(yy,"FOUND EXif Offset to Exif SubIFD******")
        new_exif_offset=bytes2int(datavalue_bytes,intel)
        process_ifd(f,tiffstart,new_exif_offset,intel,adic)
    elif tag_number==0x8825:
        atpic.log.debug(yy,"FOUND GPS Offset******")
        new_exif_offset=bytes2int(datavalue_bytes,intel)
        process_ifd(f,tiffstart,new_exif_offset,intel,exif3k.GPS_TAGS)

    elif tag_number in adic.keys():
        atpic.log.debug(yy,"tag_number is  %s" % (adic[tag_number],))
        data_format=bytes2int(data_format_bytes,intel)
        atpic.log.debug(yy,"data_format %s" % data_format)
        bytes_per_compo=bytes_per_component(data_format)
        atpic.log.debug(yy,"bytes_per_compo %s" % bytes_per_compo)
        components_nb=bytes2int(components_nb_bytes,intel)
        atpic.log.debug(yy,"components_nb %s" % components_nb)
        bytes2store=components_nb*bytes_per_compo
        if bytes2store> 4:
            datavalue=bytes2int(datavalue_bytes,intel)
            atpic.log.debug(yy,"value is a memory address %s" % datavalue)
            # lets go to pick up the long value
            f.seek(tiffstart+datavalue)
            new_data_value_bytes=f.read(bytes2store)
            atpic.log.debug(yy,"long value %s" % new_data_value_bytes)
        else:
            atpic.log.debug(yy,"value is a value %s" % datavalue_bytes)
            new_data_value_bytes=datavalue_bytes
        display_data_value(tag_number,new_data_value_bytes,data_format,bytes_per_compo,components_nb,adic,intel)
    else:
        atpic.log.debug(yy,"!!!!! tag_number 0x{:04X} does not match".format(tag_number))

def process_ifd_entries(f,tiffstart,offset_ifd,ifd_entries_nb,intel,adic):
    yy=atpic.log.setname(xx,'process_ifd_entries')
    for i in range(0,ifd_entries_nb):
        atpic.log.debug(yy,"+++++++++++ processing entry %s ++++++++++++++++" % i)
        offset_ifd_entry=offset_ifd+2+12*i # relative to tiffstart
        process_ifd_entry(f,tiffstart,offset_ifd,offset_ifd_entry,intel,adic)


def process_ifd(f,tiffstart,offset_ifd,intel,adic=exif3k.EXIF_TAGS):
    yy=atpic.log.setname(xx,'process_ifd')
    f.seek(tiffstart+offset_ifd)
    ifd_entries_nb_bytes=f.read(2)
    ifd_entries_nb=bytes2int(ifd_entries_nb_bytes,intel)
    atpic.log.debug(yy,"There are %s %s) entries in IFD at offset %s in TIFF started at %s" % (ifd_entries_nb,ifd_entries_nb_bytes,offset_ifd,tiffstart))
    # ifd_entries=f.read(12*ifd_entries_nb)
    process_ifd_entries(f,tiffstart,offset_ifd,ifd_entries_nb,intel,adic)
    f.seek(tiffstart+offset_ifd+2+12*ifd_entries_nb)
    offset_to_next_ifd_bytes=f.read(4)
    offset_to_next_ifd=bytes2int(offset_to_next_ifd_bytes,intel)
    if offset_to_next_ifd == 0:
        atpic.log.debug(yy,"No more IFD to process")
    else:
        atpic.log.debug(yy,"offset to next IFD %s" % offset_to_next_ifd)
        process_ifd(f,tiffstart,offset_to_next_ifd,intel,adic)

def process_tiff(f,tiffstart,adic):
    yy=atpic.log.setname(xx,'process_tiff')
    f.seek(tiffstart)
    tiff_header=f.read(8)
    atpic.log.debug(yy,"tiff_header %s" % tiff_header)
    endian=tiff_header[0:2]
    intel=True
    if endian == b'II':
        atpic.log.debug(yy,"Endian Intel")
        intel=True
    if endian == b'MM':
        atpic.log.debug(yy,"Endian Motorola")
        intel=False
    offset_to_first_ifd=bytes2int(tiff_header[4:],intel)
    atpic.log.debug(yy,"offset_to_first_ifd %s" % offset_to_first_ifd)
    process_ifd(f,tiffstart,offset_to_first_ifd,intel,adic)


def process_exif_header(f,offset,adic):
    yy=atpic.log.setname(xx,'process_exif_header')
    f.seek(offset) # we start at offset
    appmarker=f.read(2)
    if appmarker==b'\xff\xe1':
        atpic.log.debug(yy,"Confirming APP1: EXIF at  %s" % offset)
    sizea=f.read(2)
    exifsize=sizea[0]*256+sizea[1]
    atpic.log.debug(yy,"size of APP1: %s" % exifsize)
    exifs=f.read(6)
    if exifs == b'Exif\x00\x00':
        atpic.log.debug(yy,"Confirming EXIF string  %s" % exifs)
    tiffstart=f.tell()
    atpic.log.debug(yy,"TIFF starts at %s" % tiffstart)
    process_tiff(f,tiffstart,adic)
    return (exifsize,tiffstart)

def look_for_exif(f,offset):
    yy=atpic.log.setname(xx,'look_for_exif')
    f.seek(offset) # we start at offset
    appmarker=f.read(2) # appmarker should be xFFE0 ~ xFFEF
    atpic.log.debug(yy,"appmarker %s" % appmarker)
    if appmarker==b'\xff\xe1':
        atpic.log.debug(yy,"Found APP1: EXIF at  %s" % offset)
        return (True,offset)
    elif appmarker==b'\xff\xe0':
        atpic.log.debug(yy,"Found APP0: JFIF at  %s" % offset)
        # get the size of the APP0:
        sizea=f.read(2)
        sizeaN=sizea[0]*256+sizea[1]
        atpic.log.debug(yy,"size of APP0: %s" % sizeaN)
        newoffset=offset+sizeaN+2
        return look_for_exif(f,newoffset)
    else:
        atpic.log.debug(yy,"I am at offset %s an giving up" %  offset)
        return (True,offset)



def process_mrw_block(f,offset,intel,adic):
    """minolta mrw block"""
    yy=atpic.log.setname(xx,'process_mrw_block')
    # 4 bytes: block name, 4 bytes: lenght of block 
    # use Intel by default
    intel=False
    f.seek(offset)
    blockheaders=f.read(8)
    blockname=blockheaders[0:4]
    blocksize_bytes=blockheaders[4:8]
    blocksize=bytes2int(blocksize_bytes,intel)
    atpic.log.debug(yy,"MRW block name is %s" % blockname)
    atpic.log.debug(yy,"MRW block size is %s %s" % (blocksize_bytes,blocksize))
    if blockname==b'\x00TTW':
        atpic.log.debug(yy,"Found TTW block (TIFF big endian)")
        tiffstart=offset+8
        process_tiff(f,tiffstart,adic)
    if blockname not in [ b'\x00MRM',b'\x00PRD',b'\x00TTW',b'\x00WBG',b'\x00RIF',b'\x00PAD']:
        atpic.log.debug(yy,"no more known blocks")
        # quit()
    else:
        # get the next block
        offset=offset+blocksize+8
        process_mrw_block(f,offset,intel,adic)

def process_mrw(f,offset,intel,adic):
    """minolta mrw"""
    yy=atpic.log.setname(xx,'process_mrw')
    # 4 bytes: block name, 4 bytes: lenght of block 
    # use Intel by default
    f.seek(offset)
    blockheaders=f.read(8)
    blockname=blockheaders[0:4]
    atpic.log.debug(yy,"MRM block name is %s" % blockname)

    offset=8
    process_mrw_block(f,offset,intel,adic)


def process_raf(f,adic):
    yy=atpic.log.setname(xx,'process_raf')
    atpic.log.debug(yy,"processing raf")
    """
    http://libopenraw.freedesktop.org/wiki/Fuji_RAF
    """
    f.seek(0)
    start=f.read(148)
    jpeg_offset_pointer=48+36
    jpeg_offset_bytes=start[jpeg_offset_pointer:jpeg_offset_pointer+4]
    atpic.log.debug(yy,"jpeg_offset_bytes %s" % jpeg_offset_bytes)
    # jpeg_offset=bytes2int(jpeg_offset_bytes,True)
    # atpic.log.debug(yy,"jpeg_offset %s" % jpeg_offset)
    jpeg_offset=bytes2int(jpeg_offset_bytes,False)
    atpic.log.debug(yy,"jpeg_offset %s" % jpeg_offset)
    (foundexif,offset)=look_for_exif(f,jpeg_offset+2)  # discard the SOI (Start of Image marker xFFD8)
    if foundexif:
        (exifsize,tiffstart)=process_exif_header(f,offset,adic)

def identify(f,adic=exif3k.EXIF_TAGS): # adic=exif3k.EXIF_ATPIC_TAGS


    yy=atpic.log.setname(xx,'identify')
    # see /usr/share/perl5/Image/ExifTool.pm
    foundtype="unkown"
    #data = f.read(12)
    data = f.read(60)
    atpic.log.debug(yy,"data %s" % data)
    # a dictionary of regex to identfy the filetype
    matchers={
        "jpeg":b"\xff\xd8\xff", # 
        "mrw":b'\0MR[MI]', # minolta
        "x3f":b"FOVb", # sigma
        "raf":b"FUJIFILM", # fuji
        "tiff":b"(II|MM)", # nikon, sony, canon, olypus orf, pentax pef
        }
    for filetype,reg in matchers.items():
        # atpic.log.debug(yy,"testing %s" % filetype,reg)
        if re.match(reg,data):
            atpic.log.debug(yy,"FOUND %s" % filetype)
            foundtype=filetype
            break
    if foundtype=="unkown":
        atpic.log.debug(yy,"NOT FOUND!!!!!!!!!!!!!!!!!!!!!")


    if foundtype=="jpeg":
        foundexif=False
        offset=2
        (foundexif,offset)=look_for_exif(f,offset)  # discard the SOI (Start of Image marker xFFD8)
        if foundexif:
            (exifsize,tiffstart)=process_exif_header(f,offset,adic)


    elif foundtype=="tiff":
        tiffstart=0
        process_tiff(f,tiffstart,adic)

    elif foundtype=="mrw":
        process_mrw(f,0,True,adic)

    elif foundtype=="raf": # fuji
        process_raf(f,adic)

    atpic.log.info(yy,"foundtype %s" % foundtype)

    return foundtype


if __name__ == "__main__":
    pass
