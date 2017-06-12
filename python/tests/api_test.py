# -*- coding: utf-8 -*-
import unittest
from atpic.api import process

class process_test(unittest.TestCase):

    """tests get"""

   
    def test_process(self):
        print process("get","pic",id="1")

if __name__ == "__main__":
    unittest.main()
