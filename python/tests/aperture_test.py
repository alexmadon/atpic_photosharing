#!/usr/bin/python3
import unittest

import atpic.aperture

class aperture_test(unittest.TestCase):
    """USER legacy urls"""

    def NOtest_fnumber2int(self):
        inputs=[
            (b'1.0',b'-128'),
            (b'2.0',b'-86'),
            (b'4.0',b'-43'),
            (b'64',b'127'),
            (b'0.99',b'-128'),
            (b'64.0002',b'127'),
            ]
        for (f,expect) in inputs:
            print('--->',f)
            res=atpic.aperture.fnumber2int(f)
            print('=',res)
            self.assertEqual(res,expect)

    def test_clean(self):
        inputs=[
            (b'f5.6',b'5.6'),
            (b'f:2.0',b'2.0'),
            (b'40/10',b'4.0'),
            (b'8.0',b'8.0'),
            ]
        for (af,aex) in inputs:
            res=atpic.aperture.aperture_clean(af)
            print(af,aex,res)
            self.assertEqual(res,aex)


if __name__=="__main__":
    unittest.main()
