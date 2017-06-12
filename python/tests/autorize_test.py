#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest


import traceback
import urllib.parse

import atpic.autorize
import atpic.xplo



class autorize_test(unittest.TestCase):
    """USER legacy urls"""
    def test_gallery_autorized(self):
        # (mode,gallerymode,isauthenticated,isfriend,isowner,isauthor,isadmin,isinsecret)
        inputs=(
            (b'anonymous',b'b',True,True,True,True,True,True,b'authorized'),
            )
        i=0
        for (mode,gallerymode,isauthenticated,isfriend,isowner,isauthor,isadmin,isinsecret,expected) in inputs:
            i=i+1
            print('test ++++++++++++++++++++++',i)
            res=atpic.autorize.authorization(mode,gallerymode,isauthenticated,isfriend,isowner,isauthor,isadmin,isinsecret)
            self.assertEqual(res,expected)


    def test_authorization_elasticsearch(self):
        # (mode,uid,aid)
        inputs=(
            (b'b',b'1',b'',b'authorized'),
            )
        i=0
       
        for (mode,uid,aid,expected) in inputs:
            i=i+1
            print('test ++++++++++++++++++++++',i)
            res=atpic.autorize.authorization_elasticsearch(mode,uid,aid)
            self.assertEqual(res,expected)


if __name__=="__main__":


    unittest.main()
