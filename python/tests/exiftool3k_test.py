#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest



import atpic.exiftool3k
import atpic.exiftool_parse

files=[
( b'./fixture/image_dama.jpg' , (b'image/jpeg', b'1600', b'1200', b'', b'Canon', b'Canon PowerShot A60', b'2.8', b'0.0015625', b'5.40625', b'24', b'0', b'0', b'2004:03:29 15:51:19', b'', b'') ),
( b'./fixture/raw/RAW_CANON_300D.CRW' , (b'image/x-canon-crw', b'3072', b'2048', b'', b'', b'', b'2.8', b'', b'', b'', b'', b'', b'', b'', b'') ),
( b'./fixture/raw/RAW_CANON_300D.jpg' , (b'image/jpeg', b'3088', b'2056', b'', b'Canon', b'Canon EOS 300D DIGITAL', b'2.8', b'0.02857142857', b'', b'', b'', b'', b'2007:03:03 11:26:42', b'', b'') ),
( b'./fixture/raw/RAW_CANON_5D_ARGB.CR2' , (b'image/x-canon-cr2', b'4368', b'2912', b'', b'Canon', b'Canon EOS 5D', b'10.0', b'0.005', b'180', b'16', b'0', b'1', b'2006:01:15 19:04:48', b'', b'') ),
( b'./fixture/raw/RAW_FUJI_S5000.RAF' , (b'image/x-fujifilm-raf', b'1280', b'960', b'', b'FUJIFILM', b'FinePix S5000', b'2.8', b'0.003571428571', b'5.7', b'16', b'0', b'0', b'2008:06:22 03:48:05', b'', b'') ),
( b'./fixture/raw/RAW_MINOLTA_A1.MRW' , (b'image/x-minolta-mrw', b'2560', b'1920', b'', b'Minolta Co., Ltd.', b'DiMAGE A1', b'3.5', b'0.125', b'7.21484375', b'16', b'1', b'0', b'2004:03:28 00:45:47', b'', b'') ),
( b'./fixture/raw/RAW_NIKON_D70.NEF' , (b'image/x-nikon-nef', b'3040', b'2014', b'', b'NIKON CORPORATION', b'NIKON D70', b'7.1', b'0.005', b'50', b'16', b'0', b'0', b'2004:06:26 14:16:26', b'', b'') ),
( b'./fixture/raw/RAW_OLYMPUS_SP500UZ.ORF' , (b'image/x-olympus-orf', b'2832', b'2117', b'', b'OLYMPUS IMAGING CORP.', b'SP500UZ', b'2.8', b'0.2', b'6.3', b'16', b'1', b'0', b'2007:10:14 15:02:51', b'', b'') ),
( b'./fixture/raw/RAW_PENTAX_K10D_SRGB.PEF' , (b'image/x-pentax-pef', b'3936', b'2624', b'', b'PENTAX Corporation', b'PENTAX K10D', b'8.0', b'0.004', b'108', b'16', b'0', b'0', b'2006:12:27 10:59:50', b'', b'') ),
( b'./fixture/raw/RAW_SIGMA_SD10.X3F' , (b'image/x-sigma-x3f', b'2268', b'1512', b'', b'SIGMA', b'SIGMA SD10', b'8.0', b'', b'', b'', b'', b'', b'', b'', b'') ),
( b'./fixture/raw/RAW_SONY_A100.ARW' , (b'image/x-sony-arw', b'3872', b'2592', b'', b'SONY', b'DSLR-A100', b'11.0', b'0.01', b'60', b'16', b'1', b'0', b'2007:04:08 17:41:18', b'', b'') ),
( b'./fixture/DSCF1390_alt1526.9m.JPG' , (b'image/jpeg', b'2848', b'2136', b'', b'FUJIFILM', b'FinePix F30', b'5.6', b'0.001470588235', b'8', b'16', b'0', b'0', b'2008:01:01 13:16:54', b'47.06362405', b'8.68933233333333') ),
( b'./fixture/videos/better_MVI_5848.AVI' , (b'video/x-msvideo', b'640', b'480', b'19.933134', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'') ),
( b'./fixture/videos/loic.MPG' , (b'video/mpeg', b'720', b'576', b'5.9732596112311', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'') ),
( b'./fixture/video_apple/sample.3gp' , (b'video/3gpp', b'176', b'144', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'') ),
( b'./fixture/video_apple/sample_3GPP2.3g2' , (b'video/3gpp2', b'176', b'144', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'') ),
( b'./fixture/video_apple/sample_iPod.m4v' , (b'video/x-m4v', b'320', b'240', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'') ),
( b'./fixture/video_apple/sample_iTunes.mov' , (b'video/quicktime', b'640', b'480', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'') ),
( b'./fixture/video_apple/samplelog1.txt' , (b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'') ),
( b'./fixture/video_apple/sample_mpeg2.m2v' , (b'video/mpeg', b'192', b'240', b'5.381392', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'') ),
( b'./fixture/video_apple/sample_mpeg4.mp4' , (b'video/mp4', b'190', b'240', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'') ),
( b'./fixture/video_apple/sample_sorenson.mov' , (b'video/quicktime', b'190', b'240', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'') ),
]
# files=files+files+files+files+files+files+files

# files=[]
# for i in range(0,100):
#     files.append(("./fixture/image_dama.jpg","jpeg"))

class exif_test(unittest.TestCase):
    """exif using exiftool XML output"""

   
    def test_exif_identify(self):
        """escape"""
        i=0
        for (afile,expected) in files:
            i=i+1
            print("Doing ",i,afile)
            thexml=atpic.exiftool3k.process_file(afile)
            print(thexml.decode('utf8'))
            important3=atpic.exiftool_parse.parse(thexml)
            print('XXX (',afile,',',important3,'),')
            print('YYY',important3[0])
            self.assertEqual(expected,important3)

    def NOtest_exif_pipe(self):
        """escape"""
        i=0
        for afile in files:
            i=i+1
            print("Doing ",i,afile[0])
            xml=exif.process_file_withpipe(afile[0])
            # print(xml)

if __name__ == "__main__":
    unittest.main()
