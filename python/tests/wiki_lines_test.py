#!/usr/bin/python3
# py3k version
"""wiki lines"""
import unittest


import atpic.wiki_lines

class worker_test(unittest.TestCase):
    """USER legacy urls"""

    def test_set_replace(self):
        inputs=(
            (b'one\ntwo\nthree\nfour\nfive',b'THREE',b'3',b'3',b'one\ntwo\nTHREE\nfour\nfive'),
            (b'one\ntwo\nthree\nfour\nfive',b'ONE',b'1',b'1',b'ONE\ntwo\nthree\nfour\nfive'),
            (b'one\ntwo\nthree\nfour\nfive',b'THREE\nTHREEbis',b'3',b'3',b'one\ntwo\nTHREE\nTHREEbis\nfour\nfive'),
            (b'one\ntwo\nthree\nfour\nfive',b'THREE',b'3',b'4',b'one\ntwo\nTHREE\nfive'),
            )
        for (wikitext,wikilines,froml,tol,res) in inputs:
            result=atpic.wiki_lines.replace(wikitext,wikilines,froml,tol)
            self.assertEqual(res,result)

if __name__=="__main__":
    unittest.main()
