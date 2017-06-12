#!/usr/bin/python3
# py3k ctypes wrapper
# from /usr/include/tidy/tidy.h
# h2xml header.h -o out_c.xml
# xml2py out_c.xml -o out_c.py

# h2xml /usr/include/tidy/tidy.h -o tidy.xml
# xml2py tidy.xml -o  tidy.py
import ctypes
from ctypes.util import find_library
import sys
import io
import gc

_libtidy = ctypes.CDLL("libtidy.so")


def _putByte(handle, c):
    return 0

PUTBYTEFUNC=ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_char)    
putByte=PUTBYTEFUNC(_putByte)

class _OutputSink(ctypes.Structure):
    _fields_=[("sinkData", ctypes.c_int),
              ("putByte", PUTBYTEFUNC),
              ]


def parseString(somestring,optionsdict):
    somebytes=somestring
    return parseStringBytes(somebytes,optionsdict)

def parseStringBytes(somebytes,optionsdict):
    """
    somebytes: a bytes of HTML soup
    optionsdict: a dictionary of tidy options
    """

    tdoc = _libtidy.tidyCreate();
    setoptions(tdoc,optionsdict)
    errsink=_OutputSink()
    errsink.putByte = putByte
    # print("errsink",errsink)
    _libtidy.tidySetErrorSink(tdoc, ctypes.byref(errsink))


    # _libtidy.tidySetErrorFile( tdoc, b'/dev/null')
    _libtidy.tidyParseString( tdoc, somebytes ); 

    stlen = ctypes.c_int(8192) # 8192
    st = ctypes.c_buffer(stlen.value)
    rc = _libtidy.tidySaveString(tdoc, st, ctypes.byref(stlen))
    while rc==-12:
        print("new loop")
        st = ctypes.c_buffer(stlen.value)
        rc = _libtidy.tidySaveString(tdoc, st, ctypes.byref(stlen))
    if rc==-12: # buffer too small
        print("buffer too small")
    else:
        out=st.value.strip()
        _libtidy.tidyRelease( tdoc ) # avoid memory leak!
        return out

def setoptions(document,adict):
    for (key, value) in adict.items():
        _libtidy.tidyOptParseValue(document,key,value)


# _libtidy.tidySaveStdout(tdoc)


if __name__ == "__main__":
    test="&lt;title&gt;Foo&lt;/title&gt;&lt;p&gt;Foo! Clara cet été là nnnn".encode('utf8')
    adic={}
    adic[b"output-encoding"]=b"utf8"
    adic[b"input-encoding"]=b"utf8"
    adic[b"output-xhtml"]=b"1"
    adic[b"output-xml"]=b"1"
    adic[b"add-xml-decl"]=b"0"
    adic[b"indent"]=b"0"
    adic[b"tidy-mark"]=b"0"
    adic[b"wrap"]=b"0"
    adic[b"markup"]=b"1"
    adic[b"show-body-only"]=b"1"
    adic[b"quote-ampersand"]=b"1"
    adic[b"escape-cdata"]=b"1"
    news=parseString(test,adic)
    print('news=',news)
    a=gc.collect()
    print(a)
    # test memory leak with 'free'
    # http://bugs.python.org/issue7959
    # while 1:
    #     news=parseString(test,adic)
        
