#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest



import atpic.exiftool3k_client as exif
import atpic.exiftool3k_zmq_client as exif2


files=[
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
# files=files+files+files+files+files+files+files

# files=[]
# for i in range(0,100):
#     files.append(("./fixture/image_dama.jpg","jpeg"))

class exif_test(unittest.TestCase):
    """exif using exiftool XML output"""

   
    def NOtest_exif_identify(self):
        """escape"""
        i=0
        for afile in files:
            i=i+1
            print("Doing ",i,afile[0])
            xml=exif.getexif("/home/madon/public_html/perso/entreprise/sql_current/site/atpic/python/tests/"+afile[0])
            # print(xml)

    def test_exif_identify(self):
        """escape"""
        i=0
        for afile in files:
            i=i+1
            print("Doing ",i,afile[0])
            fname="/home/madon/public_html/perso/entreprise/sql_current/site/atpic/python/tests/"+afile[0]
            fname=fname.encode('utf8')
            xml=exif2.send(fname)
            # print(xml)

if __name__ == "__main__":
    unittest.main()
