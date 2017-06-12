#!/usr/bin/python3
import unittest
import atpic.redis_index_server


class redisindex_test(unittest.TestCase):
    def test_get(self):

        inputs=(
            (b'1', (b'1', b'', b'')) ,
            (b'1:22', (b'1', b'22', b'')) ,
            (b'1:2:333', (b'1', b'2', b'333')) ,
            )
        for (logkey,exres) in inputs:

            res=atpic.redis_index_server.transform2triplet(logkey)
            print('XXX',(logkey,res),',')
            self.assertEqual(res,exres)

if __name__=="__main__":
    unittest.main()
