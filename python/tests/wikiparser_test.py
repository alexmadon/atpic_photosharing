#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest
import urllib.parse
import io



import atpic.wikiparser


class wikiparser_test(unittest.TestCase):
    """USER legacy urls"""

    def test_parse2array(self):
        inputs=[
            ('p:124',{'image': '124'}),
            ('p:1:124',{'image': '124', 'user': '1'}),
            ('p:124@r1024',{'image': '124', 'resolution': 'r1024'}),
            ('p:124@1024',{'image': '124', 'resolution': '1024'}),
            ('p:124@r350',{'image': '124', 'resolution': 'r350'}),
            ('p:123|',{'image': '123', 'bar': '|'}),
            ('p:123@r1024|',{'resolution': 'r1024', 'image': '123', 'bar': '|'}),
            ('p:123|text link',{'link': 'text link', 'image': '123', 'bar': '|', 'id': 'text link'}),
            ('g:99',{'gallery': '99'}),
            ('g:99|some text gallery',{'link': 'some text gallery', 'gallery': '99'}),
            ('~alex',{'userdns': 'alex'}),
            ('somewikipage',{'wikipage': 'somewikipage'}),
            ('some wiki page',{'wikipage': 'some wiki page'}),
            ('somewikipage|some page',{'link': 'some page', 'wikipage': 'somewikipage'}),
            ('/some/internal',{'internal': 'some/internal'}),
            ('/some/internal|some internal',{'internal': 'some/internal', 'link': 'some internal'}),
            ('u:1',{'user': '1'}),
            ('g:99|p:124',{'image': '124', 'gallery': '99'}),
            ('g:99|p:124@350',{'image': '124', 'resolution': '350', 'gallery': '99'}),
            ]

        for (key,res) in inputs:
            result=atpic.wikiparser.parse2array(key)
            print("YYY",result)
            print("XXX ('",key,"',",result,'),',sep='')
            self.assertEqual(res,result)

if __name__=="__main__":
    unittest.main()
