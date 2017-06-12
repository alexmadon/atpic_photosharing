#!/usr/bin/python3
# mimetypes.guess_all_extensions('image/jpeg')
import unittest

import atpic.idbased
import atpic.redis_pie

class idbased_test(unittest.TestCase):
    """USER legacy urls"""

    def test_idpath2storepath(self):
        paths=(
            (b'/alex/3333_1024_2012_12_31_23_59_7e785a311a5d9ad0bfc0d66c3b5ba74e.jpg',
             b'1',b'/sdc1',b'myseed',
             b'/sdc1/store/2012/12/31/23/59/1_3333_1024.jpg'),
            )
        for (path,uid,partition,userseed,storepath_ex) in paths:
            print('testing',(path,partition,uid,userseed,storepath_ex))
            (isvalid,storepath)=atpic.idbased.idpath2storepath(path,uid,partition)
            print(isvalid,storepath)
            self.assertEqual(storepath,storepath_ex)




    def NOtest_idpath2storepath_bad(self):
        paths=(
            (b'/alex/3333_1024_2012_12_31_23_59_aassasasasasaasasasasaas.jpg',
             b'1',b'/sdc1',b'myseed',
             b'/sdc1/store/2012/12/31/23/59/1_3333_1024.jpg'),
            )
        for (path,partition,uid,userseed,storepath_ex) in paths:
            print('testing exception',(path,partition,uid,userseed,storepath_ex))
            self.assertRaises(Exception,atpic.idbased.idpath2storepath,path,partition,uid,userseed)
            
    def NOtest_get_partition_sql(self):
        paths=((b'/alex/3333_1024_2012_12_31_23_59_aassasasasasaasasasasaas.jpg',(b'1', b'/hdc1', b'')),
               )
        
        for (path,resexpect) in paths:
            res=atpic.idbased.get_partition_sql(path)
            print('PPPP',res)
            self.assertEqual(res,resexpect)
            pass
        



if __name__=="__main__":

    unittest.main()
