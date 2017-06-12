# this is a python3 ctypes libexif wrapper
from ctypes import *

libexif= CDLL("libexif.so.12")  


# exif-data.h.xml.py

STRING = c_char_p

class _ExifData(Structure):
    pass

ExifData = _ExifData

class _ExifDataPrivate(Structure):
    pass

_ExifDataPrivate._fields_ = [
]

ExifDataPrivate = _ExifDataPrivate

class _ExifContent(Structure):
    pass

ExifContent = _ExifContent

_ExifData._fields_ = [
    ('ifd', POINTER(ExifContent) * 5),
    ('data', POINTER(c_ubyte)),
    ('size', c_uint),
    ('priv', POINTER(ExifDataPrivate)),
]





class _ExifContentPrivate(Structure):
    pass

ExifContentPrivate = _ExifContentPrivate
_ExifContentPrivate._fields_ = [
]

class _ExifEntry(Structure):
    pass

ExifEntry = _ExifEntry

_ExifContent._fields_ = [
    ('entries', POINTER(POINTER(ExifEntry))),
    ('count', c_uint),
    ('parent', POINTER(ExifData)),
    ('priv', POINTER(ExifContentPrivate)),
]

# values for enumeration 'ExifTag'
ExifTag = c_int # enum

# values for enumeration 'ExifIfd'
ExifIfd = c_int # enum


class _ExifEntryPrivate(Structure):
    pass

_ExifEntryPrivate._fields_ = [
]

ExifEntryPrivate = _ExifEntryPrivate

# values for enumeration 'ExifFormat'
ExifFormat = c_int # enum

_ExifEntry._fields_ = [
    ('tag', ExifTag),
    ('format', ExifFormat),
    ('components', c_ulong),
    ('data', POINTER(c_ubyte)),
    ('size', c_uint),
    ('parent', POINTER(ExifContent)),
    ('priv', POINTER(ExifEntryPrivate)),
]



libexif.exif_data_new_from_file.restype = POINTER(ExifData)
libexif.exif_data_new_from_file.argtypes = [STRING]


fname="/home/madon/jpg/coccinelle.jpg"
exifdata2=libexif.exif_data_new_from_file(fname)

ed=exifdata2[0]
ec=ed.ifd[0]




libexif.exif_content_dump.restype = None
libexif.exif_content_dump.argtypes = [POINTER(ExifContent), c_uint]

libexif.exif_content_dump(ec,0)
