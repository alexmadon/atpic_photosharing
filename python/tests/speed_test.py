#!/usr/bin/python3
import unittest

import atpic.speed


# 1/10000=.0001
class speed_test(unittest.TestCase):
    """USER legacy urls"""

    def NOtest_speed2int(self):
        inputs=[
            (b'.00006103515625',b'-128'),  # .00006103515625 seconds = 2^-14
            (b'.008',b'-46'),  # 1/125 s ~ 2^-7
            (b'.01666666666666666666',b'-34'), # 1/60s ~ 2^-6
            (b'0.5',b'23'),
            (b'1',b'34'),
            (b'2',b'46'),
            (b'64',b'104'), # 64 seconds = 2^6
            (b'128',b'115'), # 128 seconds = 2^7
            (b'256',b'127'), # 256 seconds = 2^8
            (b'300',b'127'), # 300 seconds = overflow 
            (b'.00001',b'-128'),  # .00001 = underflow
            ]
        for (speed,expect) in inputs:
            print('speed --->',speed)
            res=atpic.speed.speed2int(speed)
            print('=',res)
            print('XXX (',speed,',',res,'),',sep='')
            self.assertEqual(res,expect)

    def test_clean(self):
        inputs=[
            (b'10/500',b'0.02000000'),
            (b'0.1',b'0.1'),
            ]
        for (af,aex) in inputs:
            res=atpic.speed.speed_clean(af)
            print(af,aex,res)
            self.assertEqual(res,aex)


if __name__=="__main__":
    unittest.main()
