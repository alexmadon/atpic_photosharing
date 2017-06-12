#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest
import urllib.parse
import io



import atpic.environment
import atpic.xmlob
import atpic.xplo



class environment_test(unittest.TestCase):
    """USER legacy urls"""
    def test_get_map(self):
        inputs=(
            (b'map=q,q1',b'q',b'q1'),
            (b'map=a,b;q,q1',b'q',b'q1'),
            (b'map=',b'q',b'q'),
            (b'',b'q',b'q'),
            )
        i=0
        for (qs,key,newkeyex) in inputs:
            i=i+1
            print('test ++++',i)
            environ={}
            environ[b'QUERY_STRING']=qs
         
            newkey=atpic.environment.get_map(environ,key)
            print('ZZZ',(qs,key,newkey))
            self.assertEqual(newkey,newkeyex)


    def test_get_qs_key(self):
        qss=(
            (b'alex=madon&f=xml',b'f',b'xhtml',b'xml'),
            (b'f=xml',b'f',b'xhtml',b'xml'),
            (b'',b'f',b'xhtml',b'xhtml'),
            (b'alex=madon',b'f',b'xhtml',b'xhtml'),
            (b'q=alex+madon',b'q',b'',b'alex madon'),
            (b'q=alex%20madon',b'q',b'',b'alex madon'),
            (b'q=%2Buid%3A1',b'q',b'',b'+uid:1'),
            (b'q=1&q2=2&map=q,q2',b'q',b'',b'2'),
            # (b'alex=madon&amp;f=xml',b'f',b'xhtml',b'xml'),
            )
        i=0
        for (qs,key,defval,expectval) in qss:
            i=i+1
            print('test ++++',i)
            environ={}
            environ[b'QUERY_STRING']=qs
            val=atpic.environment.get_qs_key(environ,key,defval)
            print('XXX', (qs,key,defval,val))
            self.assertEqual(val,expectval)

if __name__=="__main__":
    unittest.main()
