#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest
import urllib.parse


# import atpic.dispatcher
import atpic.sql_forge3

class sqlforge3_test(unittest.TestCase):
    """USER legacy urls"""
    def testTablename(self):
        olist=['alex','madon']
        tablename=atpic.sql_forge3.create_tablename(olist)
        
        self.assertEqual(tablename,"_alex_madon")

if __name__=="__main__":
    unittest.main()
