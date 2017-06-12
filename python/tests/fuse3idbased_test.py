#!/usr/bin/python3
import unittest
import os
import os.path
import atpic.hashat
import atpic.fuse3idbased
import atpic.idbased # used to mock


class fuse3_test(unittest.TestCase):
    """USER legacy urls"""

    def test_my_getattr(self):
        inputs=(
            (b'/alex',b'',(33,33,1,1,16895,0,0,0)),
            (b'/alex/1_3333_1024_2099_12_31_23_59_16200c54e17fe6483bc655950f7b72af.jpg',
             b'/hdc1/store/2099/12/31/23/59/1_333333_1024.jpg',
             (33, 33, 5, 1, 33279, 0, 0, 0)),
            )
        for (path,pathmock,res) in inputs:
            print(path,pathmock,res)
            # ===== start mocking =======
            def mock(path):
                return pathmock
            atpic.fuse3idbased.idpath2storepath_wrap=mock
            # ===== end mocking =========
            expect=atpic.fuse3idbased.my_getattr(path)
            print(expect)
            self.assertEqual(res,expect)


if __name__=="__main__":
    unittest.main()
