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

"""

rm test01.swf
./ming3k.py
swfdec-player test01.swf




"""

class SWFMovie_s(ctypes.Structure):
    pass
SWFMovie = ctypes.POINTER(SWFMovie_s)
SWFMovie_s._fields_ = [
]


class SWFAction_s(ctypes.Structure):
    pass
SWFAction = ctypes.POINTER(SWFAction_s)
SWFAction_s._fields_ = [
]

class SWFInitAction_s(ctypes.Structure):
    pass
SWFInitAction_s._fields_ = [
]
SWFInitAction = ctypes.POINTER(SWFInitAction_s)

byte = ctypes.c_ubyte


libming.Ming_useSWFVersion.restype = None
libming.Ming_useSWFVersion.argtypes = [ctypes.c_int]

libming.newSWFMovie.restype = SWFMovie
libming.newSWFMovie.argtypes = []

libming.SWFMovie_setDimension.restype = None
libming.SWFMovie_setDimension.argtypes = [SWFMovie, ctypes.c_float, ctypes.c_float]

libming.SWFMovie_setBackground.restype = None
libming.SWFMovie_setBackground.argtypes = [SWFMovie, byte, byte, byte]


libming.SWFMovie_setRate.restype = None
libming.SWFMovie_setRate.argtypes = [SWFMovie, ctypes.c_float]

libming.newSWFAction.restype = SWFAction
libming.newSWFAction.argtypes = [ctypes.c_char_p]

libming.newSWFInitAction.restype = SWFInitAction
libming.newSWFInitAction.argtypes = [SWFAction]


someas=b"trace('hi');"


someas1=b"""
_root.createEmptyMovieClip ('conteneur1',1);
_root.createEmptyMovieClip ('conteneur2',2);


function fadeout(acontainer){
acontainer._alpha-=10;
}

conteneur1.onRelease = function() {
    this.swapDepths(conteneur2);
};
conteneur2.onRelease = function() {
    this.swapDepths(conteneur1);
};


//conteneur.loadMovie('dsc_0001s.jpg');
//conteneur.loadMovie('http://88.198.67.36/atpic/1692/9420/0/366333/350.jpg');

function plot(){
  conteneur1.loadMovie('http://88.198.67.36/atpic/1863/9519/0/372951/350.jpg');
  fadeout(conteneur1);
  conteneur1.swapDepths(conteneur2);
}
function plot2(){
  conteneur2.loadMovie('http://88.198.67.36/atpic/1692/9420/0/366333/350.jpg');
  conteneur2.swapDepths(conteneur1);
}

//setInterval(this,'plot', 3000);
"""










someas2=b"""_root.createEmptyMovieClip("box", 1);
box.lineStyle(5, 0x00FF00, 50);
//makes the line 5 pixels wide, pure green, and has an alpha of 50
box.beginFill(0xFF0000, 70);
//starts to fill "box" with pure red with an alpha of 70
box.curveTo(12.5, -12.5, 25, 0);
box.curveTo(37.5, 12.5, 25, 25);
box.curveTo(12.5, 37.5, 0, 25);
box.curveTo(-12.5, 12.5, 0, 0);
//first 2 coordinates state where each line is curving to, the 2nd 2 state where the line 
//is going to (where it ends)
box.endFill();
//stops the filling of the box
"""


if __name__ == "__main__":
    
    if libming.Ming_init() != 0:
        raise Exception("Ming_init failed.");


    libming.Ming_useSWFVersion(6)
    movie = libming.newSWFMovie();
    libming.SWFMovie_setDimension(movie,600,600)
    libming.SWFMovie_setBackground(movie, 0xff, 0x00, 0xff)
    libming.SWFMovie_setRate(movie,24)

    action=libming.newSWFAction(someas)
    init = libming.newSWFInitAction(action);
    libming.SWFMovie_add(movie, init);

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
