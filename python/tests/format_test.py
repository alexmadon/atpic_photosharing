#!/usr/bin/python3
# py3k version
"""Unit tests for format module"""
import unittest


import atpic.format



class dispatcherFormattest(unittest.TestCase):
    """Test format guessing"""
    def test_get_format_from_query_string(self):
        qss=(
            (b'f=xml',b'xml'),
            (b'a=alex&f=xml',b'xml'),
            (b'f=xhtml&ggggggg=lllll',b'xhtml'),
            )
        for (test,fex) in qss:
            print("Doing %s" % test)
            environ={b"QUERY_STRING":test}
            f=atpic.format.get_format_from_query_string(environ)
            self.assertEqual(fex,f)


    def test_get_format_from_header(self):
        formatheaders=[
            (b"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",b"xhtml"),
            ]
        for test in formatheaders:
            print("Doing %s" % test[0])
            environ={b"HTTP_ACCEPT":test[0]}
            self.assertEqual(atpic.format.get_format_from_header(environ),test[1])

    def test_get_format_from_cookie(self):
        cooks=(
            (b"chips=ahoy; vienna=finger",b""),
            (b"chips=ahoy; vienna=finger; format=xml",b"xml"),
            )
        for cook in cooks:
            environ={b"HTTP_COOKIE":cook[0]}
            self.assertEqual(atpic.format.get_format_from_cookie(environ),cook[1])

if __name__=="__main__":

    unittest.main()
