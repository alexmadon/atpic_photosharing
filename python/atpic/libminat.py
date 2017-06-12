# Requires `libming.0.4.0.dylib` in the current directory
# or in the search path.
#
# from ctypes import *
# libming = cdll.load("libming.0.4.0.dylib")

# if __name__ == "__main__":
#     if libming.Ming_init() != 0:
# #         raise Exception("Ming_init failed.");
#     movie = libming.newSWFMovie();
#     bytesout = libming.SWFMovie_save(movie, "test01.swf");
#     print "Bytes written:", bytesout            


from ming import *
import sys

s = SWFShape()
s.setLine(4, 0x7f, 0, 0)
s.setRightFill(s.addFill(0xff, 0, 0))
s.movePenTo(10, 10)
s.drawLineTo(310, 10)
s.drawLineTo(310, 230)
s.drawCurveTo(10, 230, 10, 10)

m = SWFMovie()
m.setDimension(320, 240)
m.setRate(12.0)
m.add(s)
m.nextFrame()

# print """Content-type: application/x-shockwave-flash\n\n"""
m.save("test.swf")

