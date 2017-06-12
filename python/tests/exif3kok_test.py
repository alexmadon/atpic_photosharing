#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest

import atpic.exif3kok as exif






# exiftool can read RAW_CANON_300D.CRW
files2=[
("./fixture/raw/RAW_CANON_300D.CRW","tiff"),
("./fixture/raw/RAW_SIGMA_SD10.X3F","x3f"),
]

files=[
("./fixture/raw/RAW_FUJI_S5000.RAF","raf"),
("./fixture/image_dama.jpg","jpeg"),
("./fixture/raw/RAW_CANON_300D.CRW","tiff"),
("./fixture/raw/RAW_CANON_300D.jpg","jpeg"),
("./fixture/raw/RAW_CANON_5D_ARGB.CR2","tiff"),
("./fixture/raw/RAW_FUJI_S5000.RAF","raf"),
("./fixture/raw/RAW_MINOLTA_A1.MRW","mrw"),
("./fixture/raw/RAW_NIKON_D70.NEF","tiff"),
("./fixture/raw/RAW_OLYMPUS_SP500UZ.ORF","tiff"),
("./fixture/raw/RAW_PENTAX_K10D_SRGB.PEF","tiff"),
("./fixture/raw/RAW_SIGMA_SD10.X3F","x3f"),
("./fixture/raw/RAW_SONY_A100.ARW","tiff"),
("./fixture/DSCF1390_alt1526.9m.JPG","jpeg"),
]


class exif_test(unittest.TestCase):
    """html filter"""

   
    def test_exif_identify(self):
        """escape"""
        j=0
        for afile in files2:
            print("====================== file %s ===============" % j)
            j=j+1
            print("Doing ",afile[0])
            f=open(afile[0],"rb")
            filetype=exif.identify(f)
            print(filetype)
            self.assertEqual(filetype,afile[1])
            print("")
            print("")
            f.close()

if __name__ == "__main__":
    unittest.main()
