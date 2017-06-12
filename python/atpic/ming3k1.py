#!/usr/bin/python3
# http://www.advogato.org/person/follower/diary.html?start=83
# http://code.google.com/p/pyming
import ctypes
# dpkg -L libming1
libming = ctypes.CDLL("libming.so.1")

# h2xml.py
# dpkg -L libming-dev 
# h2xml /usr/include/ming.h -o ming.xml
# xml2py.py ming.xml -o ming1.py
# xml2py.py ming.xml -o ming2.py -k d -k e -k f -k s -k t
# PHP equivalent:
# gallery_slideshow_flash.php

# By way of a simple example based on test/Movie/new/test01.c: (Note: Change library name as appropriate.) 





if __name__ == "__main__":
    
    if libming.Ming_init() != 0:
        raise Exception("Ming_init failed.");
    
    movie = libming.newSWFMovie();
    libming.SWFMovie_setBackground(movie, 0xff, 0x00, 0xff)
    bytesout = libming.SWFMovie_save(movie,b"test01.swf");

    print("Bytes written:", bytesout)

"""
madon@amadon:~/tmp/strk-libming-06fdef9/test/Movie$ grep SWFAction */*
add/test01.c:SWFMovie_add(m, (SWFBlock)newSWFAction("var a = 1;"));
add/test01-cxx.C:               m->add(new SWFAction("var a = 1;\
add/test01.php:$m->add(new SWFAction("var a = 1;
add/test01.py:m.add( SWFAction("var a = 1;\
nextFrame/test01.c:SWFMovie_add(m, (SWFBlock)newSWFAction("var a = 1;"));
nextFrame/test01-cxx.C:m->add(new SWFAction("var a = 1;\
nextFrame/test01.php:$m->add(new SWFAction("var a = 1;
nextFrame/test01.py:m.add( SWFAction("var a = 1;\
nextFrame/test01.tcl:add $m (new SWFAction("var a = 1;\
nextFrame/test02.c:SWFMovie_add(m, (SWFBlock)newSWFAction("var a = 1;"));
nextFrame/test02-cxx.C:m->add(new SWFAction("var a = 1;\
nextFrame/test02.php:$m->add(new SWFAction("var a = 1;
nextFrame/test02.py:m.add( SWFAction("var a = 1;\
"""
