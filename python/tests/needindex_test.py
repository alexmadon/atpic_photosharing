#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest


import atpic.needindex
import atpic.libpqalex


class needindex_test(unittest.TestCase):
    """USER legacy urls"""

    def NOtest_parse2array(self):
        inputs=(
            (b'T|1419582387.0531254|1|2737234|a|n/2014/12/26/08/26/1_2737234_0.jpg', (True, (b'1', b'', b'2737234'))) ,
            (b'T|1419582387.0531254', (False, (b'', b'', b''))) ,
            )

        for (message,resex) in inputs:
            res=atpic.needindex.check_asyncdone(message)
            print('XXX ',(message,res),',')
            self.assertEqual(res,resex)


    def test_check_fs(self):
        inputs=(
            (b'mkdir', b'/alexmadon/testp/test2', [{b'id': b'55142', b'_user': b'1'}], (True, (b'1', b'55142', b''))) ,
            (b'rmdir', b'/alexmadon/testp/test2', [{b'id': b'55142', b'_user': b'1'}], (True, (b'1', b'55142', b''))) ,
            (b'rename', b'/alexmadon/testp/test4\x00/alexmadon/testp/test5', [{b'id': b'55141', b'_path': b'testp/test5', b'_user': b'1'}], (True, (b'1', b'55141', b''))) ,
            (b'rename', b'/alexmadon/testp/a1.jpg\x00/alexmadon/testp/a2.jpg', [{b'id': b'2737237', b'_originalname': b'a2.jpg', b'_user': b'1', b'_gallery': b'43577'}], (True, (b'1', b'43577', b'2737237'))) ,
            (b'unlink', b'/alexmadon/testp/a2.jpg', [{b'id': b'2737238', b'_user': b'1', b'_gallery': b'43577'}], (True, (b'1', b'43577', b'2737238'))) ,
            )


        

        for (command,path,result,resex) in inputs:
            
            res=atpic.needindex.needindexfs(command,path,result)
            print('YYY ',(command,path,result,res),',')
            self.assertEqual(res,resex)

if __name__=="__main__":
    unittest.main()
