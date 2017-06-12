#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest

import atpic.magic3k as magic3k

files=[
(b"./fixture/image_dama.jpg",b"image/jpeg"),
(b"./fixture/raw/RAW_FUJI_S5000.RAF",b"image/x-fujifilm-raf"), # custom magic
]


class magic_mime_test(unittest.TestCase):
    """html filter"""

   
    def test_magic(self):
        """escape"""
        for afile in files:
            themime=magic3k.from_file(afile[0], mime=True)
            print("Mime=",afile[0],themime)
            self.assertEqual(themime,afile[1])

            # another type opf call;
            themime=magic3k.mymime_from_file(afile[0])
            self.assertEqual(themime,afile[1])



if __name__ == "__main__":
    unittest.main()
