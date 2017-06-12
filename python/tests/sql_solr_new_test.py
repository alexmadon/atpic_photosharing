#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest
import urllib.parse
import io

import atpic.solr_sqlbased

class date_test(unittest.TestCase):
    def test_year(self):

        inputs=(
            (b'2009-01-01 00:10:25',b'2009'),
            (b'2005-06-10 22:35:13',b'2005'),
            )
        for (date,ex) in inputs:
            res=atpic.solr_sqlbased.get_year(date)
            print(res)
            self.assertEqual(res,ex)
   
    def test_yearmonth(self):

        inputs=(
            (b'2009-01-01 00:10:25',b'200901'),
            (b'2005-06-10 22:35:13',b'200506'),
            )
        for (date,ex) in inputs:
            res=atpic.solr_sqlbased.get_yearmonth(date)
            print(res)
            self.assertEqual(res,ex)
   

    def test_yearmonthday(self):

        inputs=(
            (b'2009-01-01 00:10:25',b'20090101'),
            (b'2005-06-10 22:35:13',b'20050610'),
            )
        for (date,ex) in inputs:
            res=atpic.solr_sqlbased.get_yearmonthday(date)
            print(res)
            self.assertEqual(res,ex)
   

    def test_datexml(self): # ("%Y-%m-%dT%H:%M:%S.%fZ")

        inputs=(
            (b'2009-01-01 00:10:25',b'2009-01-01T00:10:25.000000Z'),
            (b'2005-06-10 22:35:13',b'2005-06-10T22:35:13.000000Z'),
            (b'2006-11-12 06:05:05.935479',b'2006-11-12T06:05:05.935479Z'),
            )
        for (date,ex) in inputs:
            res=atpic.solr_sqlbased.get_datexml(date)
            print(res)
            self.assertEqual(res,ex)
   




if __name__ == "__main__":
    unittest.main()
