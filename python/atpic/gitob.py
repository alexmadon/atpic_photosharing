#!/usr/bin/python3
import zlib
f=open("06241e7ad5d0e655f76c34fbc0ece7f5869ded","rb")
a=f.read()
f.close()
print(a)
b=zlib.decompress( a,15)
print(b.decode('utf8'))
# http://stackoverflow.com/questions/1089662/python-inflate-and-deflate-implementations
# http://stackoverflow.com/questions/1532405/how-to-view-git-objects-and-index-without-using-git
