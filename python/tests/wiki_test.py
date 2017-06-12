#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest
import urllib.parse


import atpic.wiki


class dispatcherWikitest(unittest.TestCase):
    """USER legacy urls"""
    def test_dispatcher(self):
        inputs=[
            ({b'QUERY_STRING': b'', b'PATH_INFO': b'/wiki/Index'},(b'get', b'index', b'html', b'')),
            ({b'QUERY_STRING': b'', b'PATH_INFO': b'/wiki'},(b'get', b'index', b'html', b'')),
            ({b'QUERY_STRING': b'', b'PATH_INFO': b'/wiki/'},(b'get', b'index', b'html', b'')),
            ({b'QUERY_STRING': b'', b'PATH_INFO': b'/wiki/API'},(b'get', b'api', b'html', b'')),
            ({b'QUERY_STRING': b'f=txt', b'PATH_INFO': b'/wiki/API'},(b'get', b'api', b'txt', b'')),
            ({b'QUERY_STRING': b'', b'PATH_INFO': b'/wiki/Myimage.jpg'},(b'get', b'myimage.jpg', b'html', b'')),
            ({b'QUERY_STRING': b'f=mediawiki', b'PATH_INFO': b'/wiki/Index'},(b'get', b'index', b'mediawiki', b'')),
            ({b'QUERY_STRING': b'a=log', b'PATH_INFO': b'/wiki/Index'},(b'log', b'index', b'html', b'')),
            ({b'QUERY_STRING': b'a=diff', b'PATH_INFO': b'/wiki/Index'},(b'diff', b'index', b'html', b'')),
            ({b'QUERY_STRING': b'a=diff&r=AAAA..BBBB', b'PATH_INFO': b'/wiki/Index'},(b'diff', b'index', b'html', b'AAAA..BBBB')),
            ({b'QUERY_STRING': b'a=log&r=AAAA..BBBB', b'PATH_INFO': b'/wiki/Index'},(b'log', b'index', b'html', b'AAAA..BBBB')),
            ({b'QUERY_STRING': b'r=AAAA', b'PATH_INFO': b'/wiki/Index'},(b'get', b'index', b'html', b'AAAA')),
            ]
        for (environ,resex) in inputs:
            (res)=atpic.wiki.dispatcher(environ)
            # self.assertEqual(response,url[4])
            print('XXX (',environ,',',res,'),',sep='')
            self.assertEqual(resex,res)
if __name__=="__main__":


    unittest.main()
