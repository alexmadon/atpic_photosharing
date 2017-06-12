# -*- coding: utf-8 -*-
import unittest

import sys
import os
import atpic.exif





class exif_test(unittest.TestCase):
    # class cleaner_test():
    """html filter"""

   
        
    def test_exif_xml_all(self):
        """exif xml"""
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        file=path+'/fixture/raw/RAW_NIKON_D70.NEF'
        # print test
        # we check the option
        xml=atpic.exif.exif_all(file)
        print "***************** TEST 1b"
        print xml
        # self.assertEqual(ret,test[1])
        
    def test_exif_xml_atpic(self):
        """exif xml"""
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        file=path+'/fixture/raw/RAW_NIKON_D70.NEF'
        # print test
        # we check the option
        xml=atpic.exif.exif_atpic(file)
        print "***************** TEST 2"
        print xml
        # self.assertEqual(ret,test[1])
        
    def test_exif_all_geo(self):
        """exif xml GEO"""
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        file=path+'/fixture/test_exif_geo.jpg'
        # print test
        # we check the option
        xml=atpic.exif.exif_all(file)
        print "***************** TEST 3"
        print xml
        # self.assertEqual(ret,test[1])



if __name__ == "__main__":
    unittest.main()
