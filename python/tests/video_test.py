# -*- coding: utf-8 -*-
import unittest

import sys
import os
import atpic.videothumb





class video_test(unittest.TestCase):
    # class cleaner_test():
    """html filter"""

   
    def test_video_thumb(self):
        """exif xml"""
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        infile=path+'/fixture/videos/better_MVI_5848.AVI'
        outfile=path+'/tmp/videosthumb.png'
        # print test
        # we check the option
        xml=atpic.videothumb.videothumbnailer(infile,outfile)
        print xml
        # self.assertEqual(ret,test[1])
        
    def test_video_thumb_size(self):
        """exif xml"""
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        infile=path+'/fixture/videos/better_MVI_5848.AVI'
        outfile=path+'/tmp/videosthumbsize.png'
        size="800"
        # print test
        # we check the option
        xml=atpic.videothumb.videothumbnailer(infile,outfile,size)
        print xml
        # self.assertEqual(ret,test[1])
        


if __name__ == "__main__":
    unittest.main()
