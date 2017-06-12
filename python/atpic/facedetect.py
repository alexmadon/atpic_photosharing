#!/usr/bin/python
 
# face_detect.py
 
# Face Detection using OpenCV. Based on sample code from:
# http://python.pastebin.com/m76db1d6b
 
# Usage: python face_detect.py <image_file>
# http://creatingwithcode.com/howto/face-detection-in-static-images-with-python/
# apt-get install python-opencv
# apt-get install libcv-dev

# contains: /usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml





import sys, os
from opencv.cv import *
from opencv.highgui import *
 
def detectObjects(image):
  """Converts an image to grayscale and prints the locations of any
  faces found"""
  grayscale = cvCreateImage(cvSize(image.width, image.height), 8, 1)
  cvCvtColor(image, grayscale, CV_BGR2GRAY)
 
  storage = cvCreateMemStorage(0)
  cvClearMemStorage(storage)
  cvEqualizeHist(grayscale, grayscale)
  cascade = cvLoadHaarClassifierCascade(
    '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml',
    cvSize(1,1))
  faces = cvHaarDetectObjects(grayscale, cascade, storage, 1.2, 2,CV_HAAR_DO_CANNY_PRUNING, cvSize(50,50))
 
  # if faces:
  #   for f in faces:
  #     print("[(%d,%d) -> (%d,%d)]" % (f.x, f.y, f.x+f.width, f.y+f.height))
  return faces

def print_html(image,faces):
  out=[]
  out.append("""<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<!-- http://www.dynamicdrive.com/forums/showthread.php?t=28508 -->
<head>
<title>Photo</title>
<style type="text/css">
.square {
border: 1px solid #FF0000;
position: absolute;
}
</style></head>
<body>
<img style="z-index: 1;" src="%s"/>
""" % image)
  zindex=1
  color=-1
  colors=[
    "FF0000",
    "00FF00",
    "0000FF",
    "FFFF00",
    "00FFFF",
    "FF00FF",

    
    ]
  for f in faces:
    zindex=zindex+1
    color=color+1
    # print("[(%d,%d) -> (%d,%d)]" % (f.x, f.y, f.x+f.width, f.y+f.height))
    out.append("""<div style="left:%d;top:%dpx;width:%dpx;height:%dpx;position: absolute;border-width: 2px; border-style:solid; border-color:%s;z-index: %d;"></div>""" % (f.x, f.y, f.width, f.height,colors[color],zindex))
  out.append("""</body></html>""")
  print "".join(out)

def main():
  image_path=sys.argv[1]
  image = cvLoadImage(image_path);
  faces=detectObjects(image)
  print_html(image_path,faces)


if __name__ == "__main__":
  main()
 

