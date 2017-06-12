#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest
import urllib.parse
import io



import atpic.wiki_rst


class wiki_rst_test(unittest.TestCase):
    """USER legacy urls"""

    def test_parse2array(self):
        # the input is the output of wikiparser
        inputs=[
            ({'image': '124'},),
            ({'resolution': 'r1024', 'image': '124'},),
            ({'resolution': '1024', 'image': '124'},),
            ({'resolution': 'r350', 'image': '124'},),
            ({'image': '123', 'bar': '|'},),
            ({'resolution': 'r1024', 'image': '123', 'bar': '|'},),
            ({'image': '123', 'id': 'text link', 'bar': '|', 'link': 'text link'},),
            ({'gallery': '99'},),
            ({'gallery': '99', 'link': 'some text gallery'},),
            ({'userdns': 'alex'},),
            ({'wikipage': 'somewikipage'},),
            ({'wikipage': 'some wiki page'},),
            ({'wikipage': 'somewikipage', 'link': 'some page'},),
            ({'internal': 'some/internal'},),
            ({'internal': 'some/internal', 'link': 'some internal'},),
            ({'user': '1'},),
            ({'image': '124', 'gallery': '99'},),
    
            ]

        for (key,) in inputs:

            pass # TODO in forgesql?




    def test_2nodes(self):

        inputs=[
            ({'p:1':{'link': 'http://alex.atpic.faa/gallery/1/pic/1', 'url': 'http://alex.atpicdata.faa/a99VLuvVMtCaVAs0EIWIDTiEaJM8iUXTC.jpg', 'image': '1'}, 'hello': {'wikipage': 'hello'}, 'p:1234': {'error': 'could not find picture with key p:1234', 'image': '1234'}},)
            ]

        for references in inputs:
            new_ref=atpic.wiki_rst.transform_refnodes(references)
            print((references,new_ref))

if __name__=="__main__":
    unittest.main()
