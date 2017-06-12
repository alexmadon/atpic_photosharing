# -*- coding: utf-8 -*-
import unittest

import sys
import os
import atpic.image





class image_test(unittest.TestCase):
    # class cleaner_test():
    """html filter"""

   
    def test_magick_xml(self):
        """exif xml"""
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        file=path+'/fixture/image_dama.jpg'
        # print test
        # we check the option
        xml=atpic.image.magick(file)
        print(xml)
        # self.assertEqual(ret,test[1])
        
    def test_magickpipe_xml(self):
        """exif xml"""
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        file=path+'/fixture/image_dama.jpg'
        # print test
        # we check the option
        xml=atpic.image.magickpipe(file)
        print(xml)
        # self.assertEqual(ret,test[1])
        
    def test_pil_xml(self):
        """exif xml"""
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        file=path+'/fixture/image_dama.jpg'
        # print test
        # we check the option
        xml=atpic.image.pil(file)

        print(xml)
        # self.assertEqual(ret,test[1])
        


if __name__ == "__main__":
    unittest.main()
