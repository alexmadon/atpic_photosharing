#!/usr/bin/python3
# py3k version
"""Unit tests for format module"""
import unittest


import atpic.anticsrf



class anticsrftest(unittest.TestCase):
    """Test format guessing"""
    def test_attack(self):
        environs=(
            ({b'REQUEST_METHOD': b'POST',b'HTTP_HOST': b'atpic.faa',b'HTTP_REFERER': b'http://hacker.net'},True),
            ({b'REQUEST_METHOD': b'GET',b'HTTP_HOST': b'atpic.faa',b'HTTP_REFERER': b'http://hacker.net'},False),
            ({b'REQUEST_METHOD': b'POST',b'HTTP_HOST': b'atpic.faa',b'HTTP_REFERER': b''},False),
            ({b'REQUEST_METHOD': b'POST',b'HTTP_HOST': b'atpic.faa',b'HTTP_REFERER': b'http://atpic.faa'},False),
            ({b'REQUEST_METHOD': b'POST',b'HTTP_HOST': b'atpic.faa',b'HTTP_REFERER': b'http://atpic.faa:80'},False),
            ({b'REQUEST_METHOD': b'POST',b'HTTP_HOST': b'atpic.faa',b'HTTP_REFERER': b'https://atpic.faa'},False),
            ({b'REQUEST_METHOD': b'POST',b'HTTP_HOST': b'atpic.faa',b'HTTP_REFERER': b'https://atpic.faa:443'},False),
            ({b'REQUEST_METHOD': b'POST',b'HTTP_HOST': b'atpic.faa'},False),
            ({b'REQUEST_METHOD': b'PUT',b'HTTP_HOST': b'atpic.faa',b'HTTP_REFERER': b'http://hacker.net'},True),
            ({b'REQUEST_METHOD': b'DELETE',b'HTTP_HOST': b'atpic.faa',b'HTTP_REFERER': b'http://hacker.net'},True),
            )

        for  (environ,resex) in environs:
            res=atpic.anticsrf.isattack(environ)

            self.assertEqual(res,resex)

if __name__=="__main__":

    unittest.main()
