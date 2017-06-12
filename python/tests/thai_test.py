#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest
import atpic.thai_libthai
"""
http://www.thai-language.com/id/801644


แล้วพบกันใหม่ means "See you later."

and is compound by three words:

แล้ว
พบกัน
ใหม่
"""

class thai_test(unittest.TestCase):
    def test_whitespace(self):
        inputs=(
            ("แล้วพบกันใหม่","แล้ว พบ กัน ใหม่"),
            )
        for (ains,ex) in inputs:
            ain=ains.encode('utf8')
            aout=atpic.thai_libthai.whitespace(ain)
            aouts=aout.decode('utf8')
            print(ains,'=>',aouts)
            self.assertEqual(aouts,ex)

if __name__=="__main__":
    unittest.main()
