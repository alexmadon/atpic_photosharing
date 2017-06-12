# python-imaging   # http://www.pythonware.com/products/pil/
# http://www.pythonware.com/library/pil/handbook/introduction.htm


# python-webunit



# python-pythonmagick
# ftp://ftp.imagemagick.net/pub/ImageMagick/python/README.txt

import PythonMagick
import Image
import subprocess
from . import apihelper

def magick(file):
    i = PythonMagick.Image(file)
    print(i)
    print(dir(i))
    apihelper.info(i,spacing=20,collapse=1)
    print("size=%s" % dir(i.size()))
    print("size.width=%s" % i.size().width())
    print("format=%s" % i.format())
    print("rows=%s" % i.rows())
    print("columns=%s" % i.columns())
    print(i.write.__doc__)
    # i.format = 'PNG'
    # i.gaussianBlur( 5.0, 0.0)
    # i.transformSkewX(25.0)
    i.scale("128x128")
    i.quality(99)
    i.write('testQ.jpg')

def magickpipe(file):
    output = subprocess.Popen(["convert","-scale","128x128","-quality","98",file,"test7.jpg"], stdout=subprocess.PIPE).communicate()[0]

def pil(file):
    im = Image.open(file)
    print(im.format, im.size, im.mode)
    # im.show()
    size=(128, 128)
    out = im.resize(size)
    out.save("test.jpg")
    print(im.format, im.size, im.mode)
    im2=im
    im2.thumbnail(size)
    im2.save("test2.jpg")

    im3=im    
    im2.thumbnail(size,Image.ANTIALIAS)
    im2.save("test3.jpg")


    im4=im
    out = im4.resize(size)
    im4.save("test4.jpg",quality=100, optimize=0)
