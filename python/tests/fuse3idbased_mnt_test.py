#!/usr/bin/python3
import unittest
import os
import os.path
import atpic.hashat

class worker_test(unittest.TestCase):
    """USER legacy urls"""

    def test_readfs(self):
        inputs=(
            (b'/hdc1/store/2099/12/31/23/59/1_333333_1024.jpg',
             b'/atpicidbased/alex/1_3333_1024_2099_12_31_23_59_'+atpic.hashat.dohash(b'',b'alex',b'3333',b'1024',b'2099',b'12',b'31',b'23',b'59')+b'.jpg'),
            )
        for (storepath,idpath) in inputs:
            print(storepath,idpath)
            storedir=os.path.dirname(storepath)
            print(storedir)
            try:
                os.makedirs(storedir)
            except OSError as e:
                if e.errno == 17:
                     print('dir exists')
            f=open(storepath,'wb')
            f.write(b'hello')
            f.close()
            fout=open(idpath,'rb')
            a=fout.read()
            fout.close()
            print(a)
            # self.assertEqual(res,expect)


if __name__=="__main__":
    unittest.main()
