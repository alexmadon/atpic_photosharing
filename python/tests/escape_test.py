#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest

import atpic.cleaner_escape


check_escape=(
("<br/>","&lt;br/&gt;"),
("cet été là","cet été là"),
("Lierre&pétale","Lierre&amp;pétale"),
)



class cleaner_escape_test(unittest.TestCase):
    """html filter"""

   
    def test_cleaner_escape(self):
        """escape"""
        for test in check_escape:
            # print test
            # we check the option
            ret = atpic.cleaner_escape.escape(test[0])
            print("%s => %s" % (test[0],ret))
            self.assertEqual(ret,test[1])

    def test_cleaner_escape_unescape(self):
        """escape and then unescape: should get the first input"""
        for test in check_escape:
            # print test
            # we check the option
            ret = atpic.cleaner_escape.unescape(atpic.cleaner_escape.escape(test[0]))
            print("%s => %s" % (test[0],ret))
            self.assertEqual(ret,test[0])



if __name__ == "__main__":
    unittest.main()
