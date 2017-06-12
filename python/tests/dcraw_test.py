#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest

import sys
import os
import atpic.dcraw






class dcraw_test(unittest.TestCase):
    # class cleaner_test():
    """html filter"""

   
    def NOtest_identify_wrong(self):
        """dcraw should fail"""
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        file=path+'/fixture/image_dama.jpg'
        # print test
        # we check the option
        mime=atpic.dcraw.identify(file)
        mime_expected="<noraw/>"
        self.assertEqual(mime,mime_expected)
        
    def test_identify_ok(self):
        """dcraw canon"""
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        infile=path+'/fixture/raw/RAW_CANON_300D.CRW'
        # print test
        # we check the option
        mime=atpic.dcraw.identify(infile)
        mime_expected="<israw/><make>Canon</make><model>EOS 300D DIGITAL</model>"
        self.assertEqual(mime,mime_expected)
        
    def test_convert(self):
            
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        outfile=b'/tmp/hh.jpg'
        infile=path+'/fixture/raw/RAW_CANON_300D.CRW'
        msg=atpic.dcraw.ufraw_convert(infile.encode('utf8'),outfile)
        print('msg=',msg)


if __name__ == "__main__":
    unittest.main()
