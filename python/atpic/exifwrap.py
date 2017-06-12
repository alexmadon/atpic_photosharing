# this is a python3 ctypes libexif wrapper
from ctypes import *

# http://python.net/crew/theller/ctypes/tutorial.html#incomplete-typesclass 

# exif-ifd.h
# enum:
EXIF_IFD_0 = 0               
EXIF_IFD_1 = 1                 
EXIF_IFD_EXIF = 2                
EXIF_IFD_GPS = 3              
EXIF_IFD_INTEROPERABILITY = 4
EXIF_IFD_COUNT = 5 

# madon@amadon:~/tmp/libexif-0.6.19/libexif$ h2xml.py  /home/madon/tmp/libexif-0.6.19/libexif/exif-tag.h -o /home/madon/tmp/libexif-0.6.19/libexif/exif-tag.xml
# xml2py.py /home/madon/tmp/libexif-0.6.19/libexif/exif-tag.xml -l libexif.so
# xml2py.py /home/madon/tmp/libexif-0.6.19/libexif/exif-tag.xml -l libexif.so -o  /home/madon/tmp/libexif-0.6.19/libexif/exif-tag.py

class _ExifEntryPrivate(Structure):
    pass

class _ExifContentPrivate(Structure):
    pass

class _ExifDataPrivate(Structure):
    pass

class _ExifContent(Structure):
    pass

class _ExifData(Structure):
    pass

# exif-entry.h



class _ExifEntry(Structure):
    _fields_ = [
        ("tag", c_int), #_ExifTag), enum in exif-tag.h e.g.: 0x0002, 1hexa=4bits,byte=8bits,short=16bits
        ("format",c_int), # _ExifFormat), enum exif-format.h e.g.: 2
        ("components",c_ulong),
        ("data",POINTER(c_ubyte)),
        ("size",c_uint),
        ("parent",POINTER(_ExifContent)),
        ("priv",POINTER(_ExifEntryPrivate)),
        ]


# exif-content.h
# class _ExifContentPrivate(Structure):
#     pass

class _ExifContent(Structure):
    _fields_ = [
        ("entries",POINTER(POINTER(_ExifEntry))),
        ("count",c_uint),
        ("parent",POINTER(_ExifData)), # ExifData)),
        ("priv",POINTER(_ExifContentPrivate))
        ]
    

# exif-data.h

class _ExifData(Structure):
    _fields_ = [
        # ("ifd",_ExifContent*EXIF_IFD_COUNT), # Data for each IFD. 
        ('ifd', POINTER(_ExifContent) * 5),
        ("data",POINTER(c_ubyte)), # Pointer to thumbnail image, or NULL if not available. 
        ("size",c_uint), # Number of bytes in thumbnail image at data. 
        ("priv",POINTER(_ExifDataPrivate))
        ]




# package libexif12
# /usr/lib/libexif.so.12
# cdll.LoadLibrary("libexif.so.12")

# http://libexif.sourceforge.net/api/main.html

libexif= CDLL("libexif.so.12")  
exifloader=libexif.exif_loader_new()

# fname="/home/madon/jpg/coccinelle.jpg"
# fname=c_char_p("/home/madon/jpg/coccinelle.jpg")

# success=libexif.exif_loader_write_file(exifloader,fname)
# exifdata=libexif.exif_loader_get_data(exifloader)
# exifdata2=libexif.exif_data_new_from_file(fname)

# http://www.dalkescientific.com/writings/NBN/ctypes.html

fname="/home/madon/jpg/coccinelle.jpg"

libexif.exif_data_new_from_file.argtypes = [c_char_p]
libexif.exif_data_new_from_file.restype = POINTER(_ExifData)
exifdata2=libexif.exif_data_new_from_file(fname)




ed=exifdata2[0]
ec=ed.ifd[0]




libexif.exif_content_dump.restype = None
libexif.exif_content_dump.argtypes = [POINTER(_ExifContent), c_uint]

libexif.exif_content_dump(ec,0)



# type(exifdata2)
# <class '__main__.LP__ExifData'>
libexif.exif_data_dump(exifdata2)
ed=exifdata2[0]
# ed.data
ec=ed.ifd[0]



libexif.exif_content_dump(byref(ec),0)












ec.count

>>> ec=ed.ifd[2]
>>> ec.count
3079216736



for i in range(0,ec.count):
    entry=ec.entries[0][i]
    print(entry)
    print("size",entry.size)
    print("components",entry.components)
    print("format",entry.format)
    print("tag",entry.tag)
    print("0x%04x"%entry.tag)


# libexif.EXIF_IFD_COUNT

# see 
# cvs -z3 -d:pserver:anonymous@libexif.cvs.sourceforge.net:/cvsroot/libexif co -P exif
# exif/main.c for examples
# usage:  exif -x ~/jpg/coccinelle.jpg

# http://docs.python.org/dev/3.0/library/ctypes.html
# 15.15.1.17. Callback functions

