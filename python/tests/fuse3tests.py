import unittest
import atpic.fuse3at as fuse3at
import atpic.authenticate

paths=[
# ("/","/"),
# ("/u_http","/")
("/u_http","/atpictree_ln"),
("/u_http/alex","/atpictree_ln/alex"),
("/i_http/1","/atpictree/1"),
# ("/i_cookie/"+atpic.authenticate.session_make(1)+"/1","/atpictree/1"),
("/u_cookie/http_lang:en-us,en;q=0.5/country:--/::/alex","/atpictree_ln/alex"),
]


paths2=[
("/i_http/1",["u","1"]),
("/i_http/1/avignon",["g","1","3","0"]),
("/i_http/1/avignon/IMG_0232s.JPG",["p","1","3","0","23","jpg"]),

]

links=[
("/hdc1/fastdir/atpic/1/128/0/1160/0.jpg")
]
class trans_test(unittest.TestCase):
    """ transforms tests """


    def test_path2tree(self):
        """path to tree conversion"""
        for path in paths:
            treepath=fuse3at.transform_path2tree(path[0])
            print(path[0],"->",treepath," (",path[1],")")
            self.assertEqual(treepath,path[1])

    def test_path2node(self):
        """path to node IDs conversion"""
        for path in paths:
            treepath=fuse3at.transform_path2node(path[0])
            print(path[0],"->",treepath," (",path[1],")")
            self.assertEqual(treepath,path[1])


if __name__ == "__main__":
    unittest.main()
