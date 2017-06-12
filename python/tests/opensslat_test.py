#!/usr/bin/python3

import unittest

import atpic.opensslat

class openssl_test(unittest.TestCase):
    def test_encrypt_idempotent(self):

        data=b'some text to encrypt2 more more more moe more more'
        key=b'some super long keeyyy'

        out=atpic.opensslat.encrypt(data,key)
        print(out)
        out2=atpic.opensslat.encrypt(out,key,enc=0)
        self.assertEqual(out2,data)

    def test_encrypt_brokenkey(self):
        data=b'some text to encrypt2 more more more moe more more'
        key=b'some super long keeyyy'

        out=atpic.opensslat.encrypt(data,key)
        print(out)
        self.assertRaises(Exception,atpic.opensslat.encrypt,out,key+b'bbb',enc=0)

    def test_encrypt_brokendata(self):
        data=b'some text to encrypt2 more more more moe more more'
        key=b'some super long keeyyy'

        out=atpic.opensslat.encrypt(data,key)
        print(out)
        self.assertRaises(Exception,atpic.opensslat.encrypt,out+b'bad',key,enc=0)


if __name__=="__main__":
    unittest.main()
