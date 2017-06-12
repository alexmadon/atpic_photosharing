#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest


import atpic.wikinormalizer


class wikinormalizer_test(unittest.TestCase):
    """USER legacy urls"""

    def test_parse2array(self):
        inputs=(
            (b'FTP',b'ftp'),
            (b'File Upload',b'file_upload'),
            (b'go-go',b'go_go'),
            (b'Europe/France',b'europe_france'),
            
            )

        for (key,res) in inputs:
            result=atpic.wikinormalizer.normalize(key)
            # print("YYY",result)
            print("XXX ",(key,res),sep='')
            self.assertEqual(res,result)

if __name__=="__main__":
    unittest.main()
