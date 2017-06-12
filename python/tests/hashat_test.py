#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest
import urllib.parse
import atpic.hashat


class hash_test(unittest.TestCase):
    """USER legacy urls"""

    def test_dohash(self):
        inputs=(
            b'1',b'12345',
            )
    """
    def test_dohash(self):
        inputs=(
            (b'33333',b'1024',b'2012',b'12',b'31',b'23',b'59',b'f4916de4a198f8f702c06647ff8b81e8'),
            )
        for (pid,resolution,year,month,day,hour,minute,expect) in inputs:
            res=atpic.hashat.dohash(pid,resolution,year,month,day,hour,minute)
            print(res)
            self.assertEqual(res,expect)

    def test_checkhash(self):
        inputs=(
            (b'33333',b'1024',b'2012',b'12',b'31',b'23',b'59',b'f4916de4a198f8f702c06647ff8b81e8',True),
            (b'33333',b'1024',b'2012',b'12',b'31',b'23',b'59',b'F4916de4a198f8f702c06647ff8b81e8',False),
            (b'43333',b'1024',b'2012',b'12',b'31',b'23',b'59',b'f4916de4a198f8f702c06647ff8b81e8',False),
            )
        for (pid,resolution,year,month,day,hour,minute,ahash,expect) in inputs:
            res=atpic.hashat.checkhash(ahash,pid,resolution,year,month,day,hour,minute)
            print(res)
            self.assertEqual(res,expect)

    def test_idempotent(self):
        inputs=(
            (b'33333',b'1024',b'2012',b'12',b'31',b'23',b'59'),
            )
        for (pid,resolution,year,month,day,hour,minute) in inputs:
            ahashgood=atpic.hashat.dohash(pid,resolution,year,month,day,hour,minute)
            print(ahashgood)
            res=atpic.hashat.checkhash(ahashgood,pid,resolution,year,month,day,hour,minute)
            self.assertEqual(res,True)

            # now check some False modifying input
            res=atpic.hashat.checkhash(ahashgood+b'BAD',pid,resolution,year,month,day,hour,minute)
            self.assertEqual(res,False)
            res=atpic.hashat.checkhash(ahashgood,pid+b'1',resolution,year,month,day,hour,minute)
            self.assertEqual(res,False)
            res=atpic.hashat.checkhash(ahashgood,pid,resolution+b'1',year,month,day,hour,minute)
            self.assertEqual(res,False)
            res=atpic.hashat.checkhash(ahashgood,pid,resolution,year+b'1',month,day,hour,minute)
            self.assertEqual(res,False)
            """


if __name__=="__main__":
    unittest.main()
