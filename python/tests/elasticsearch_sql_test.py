#!/usr/bin/python3
import atpic.elasticsearch_sql
import unittest

inputs=(
    ({b'mimesubtype_exiftool': b'', b'ptag': b'', b'uid': b'1', b'countgt': b'', b'ppath': b'', b'datetimeoriginalsql': b'2010-10-24 16:48:12.254367', b'exifexposuretime': b'', b'datestore1024': b'', b'pid': b'2019119', b'pfriend': b'', b'servershort': b'alex', b'countpt': b'', b'gpath': b'/screen_shots/', b'originalname': b'atpic_screen_shot.png', b'countpf': b'', b'datestore70': b'', b'gtag': b'', b'countga': b'', b'gfriend': b'', b'gphrase': b'', b'exifmodel': b'', b'secret': b'', b'gid': b'38764', b'gtitle': b'screen shots', b'countgf': b'', b'plon': b'', b'exifaperture': b'', b'glon': b'', b'mimesubtype_magic': b'', b'glat': b'', b'plat': b'', b'countpa': b'', b'gmode': b'b', b'countpv': b'', b'ufriend': b'2 3', b'mimetype_magic': b'', b'countua': b'2', b'exiffocallength': b'', b'extension': b'png', b'pphrase': b'', b'datestore350': b'', b'countph': b'', b'counter': b'0', b'exifmake': b'', b'mimetype_exiftool': b'', b'datestore0': b'', b'datestore160': b'', b'ptitle': b'', b'datestore600': b'', b'pvote': b''},b''),
    ({b'mimesubtype_exiftool': b'', b'ptag': b'', b'uid': b'1', b'countgt': b'1', b'ppath': b'', b'datetimeoriginalsql': b'2011-02-05 14:17:36', b'exifexposuretime': b'1/112', b'datestore1024': b'', b'pid': b'2087289', b'pfriend': b'', b'servershort': b'alex', b'countpt': b'', b'gpath': b'/5317/', b'originalname': b'photo1r.JPG', b'countpf': b'', b'datestore70': b'', b'gtag': b'test', b'countga': b'', b'gfriend': b'', b'gphrase': b'', b'exifmodel': b'iPhone 3GS', b'secret': b'', b'gid': b'5317', b'gtitle': b'', b'countgf': b'', b'plon': b'', b'exifaperture': b'f/2.8', b'glon': b'', b'mimesubtype_magic': b'', b'glat': b'', b'plat': b'', b'countpa': b'', b'gmode': b'v', b'countpv': b'', b'ufriend': b'2 3', b'mimetype_magic': b'', b'countua': b'2', b'exiffocallength': b'77/20', b'extension': b'jpg', b'pphrase': b'', b'datestore350': b'', b'countph': b'', b'counter': b'0', b'exifmake': b'Apple', b'mimetype_exiftool': b'', b'datestore0': b'', b'datestore160': b'', b'ptitle': b'', b'datestore600': b'', b'pvote': b''},b''),
)

class elasticsearch_test(unittest.TestCase):
    def test_dic2json(self):

        for (adic,ajson_expect) in inputs:
            ajson=atpic.elasticsearch_sql.dic2json(adic)
            print(ajson)

if __name__=="__main__":
    unittest.main()
