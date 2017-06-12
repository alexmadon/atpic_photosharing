#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest
import urllib.parse
import io



import atpic.redistreepath





class redistreepath_test(unittest.TestCase):
    """USER legacy urls"""

    def test_idempotent(self):
        tests=(
            (b'/sda1',b'1',b'22',b'p',b'5555555555',b'666666666'),
            )

        for (mount,uid,gid,perm,ctime,mtime) in tests:

            serial=atpic.redistreepath.serialize_path(mount,uid,gid,perm,ctime,mtime)
            print(serial)
            unser=atpic.redistreepath.unserialize_path(serial)
            self.assertEqual(unser,(mount,uid,gid,perm,ctime,mtime))




    def test_expect(self):
        tests=(
            ((b'/sda1',b'1',b'22',b'p',b'5555555555',b'666666666'),b'/sda1|1|22|p|5555555555|666666666'),
            )

        for ((mount,uid,gid,perm,ctime,mtime),expected) in tests:

            serial=atpic.redistreepath.serialize_path(mount,uid,gid,perm,ctime,mtime)
            print(serial,expected)





if __name__=="__main__":

    unittest.main()
