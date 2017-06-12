#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest
import atpic.mybytes


class mybytes_test(unittest.TestCase):
    def test_bytes2float(self):
        print('hi')
        inputs=[
            b'100',
            b'100.0001',
            b'-100.9',
            b'+100',
            b'',
            b'5.6',
            None,
            ]
        for abytes in inputs:
            afloat=atpic.mybytes.bytes2float(abytes)
            print('XXX',(abytes,afloat))

    def test_float2bytes(self):
        print('hi')
        inputs=[
            (100, b'100') ,
            (100.0001, b'100.0001') ,
            (-100.9, b'-100.9') ,
            (100, b'100') ,
            (5.6, b'5.6') ,
            (1e-16, b'1e-16') ,
            ]
        for (afloat,abytesex) in inputs:
            abytes=atpic.mybytes.float2bytes(afloat)
            print('YYYY',(afloat,abytes),',')
            self.assertEqual(abytes,abytesex)
            # need to be idempotent
            afloat2=atpic.mybytes.bytes2float(abytes)
            print('should be the same',afloat,afloat2)
            self.assertEqual(afloat,afloat2)
if __name__=="__main__":
    unittest.main()
