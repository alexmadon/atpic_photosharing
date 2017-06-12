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

_libtidy = ctypes.CDLL("libtidy.so")

def parseString(somestring,optionsdict):
    somebytes=somestring.encode("utf8")
    return parseStringBytes(somebytes,optionsdict)

def parseStringBytes(somebytes,optionsdict):
    """
    somebytes: a bytes of HTML soup
    optionsdict: a dictionary of tidy options
    """

    tdoc = _libtidy.tidyCreate();
    setoptions(tdoc,optionsdict)
    _libtidy.tidySetErrorFile( tdoc, b'/dev/null')
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
        out=st.value.decode('utf8').strip()
        _libtidy.tidyRelease( tdoc )
        return out
    # adic["input-encoding"]="utf8"
    # adic["output-encoding"]="utf8"

def setoptions(document,adict):
    for (key, value) in adict.items():
        _libtidy.tidyOptParseValue(document,key.encode("utf8"),value.encode("utf8"))


# _libtidy.tidySaveStdout(tdoc)


if __name__ == "__main__":
    test="&lt;title&gt;Foo&lt;/title&gt;&lt;p&gt;Foo! Clara cet été là nnnn"
    adic={}
    adic["output-encoding"]="utf8"
    adic["input-encoding"]="utf8"
    adic["output-xhtml"]="1"
    adic["output-xml"]="1"
    adic["add-xml-decl"]="0"
    adic["indent"]="0"
    adic["tidy-mark"]="0"
    adic["wrap"]="0"
    adic["markup"]="1"
    adic["show-body-only"]="1"
    adic["quote-ampersand"]="1"
    adic["escape-cdata"]="1"
    news=parseString(test,adic)
    print(news)
    while True:
        news=parseString(test,adic)
