#!/usr/bin/python3
import unittest
import atpic.xplo


class xmplo_test(unittest.TestCase):

    def test_toxml(self):
        lists=(
            ([(b'gallery', b'99'), (b'gallery', b'100')], b'<gallery>99</gallery><gallery>100</gallery>') ,
            ([(b'A', b'a&b'), (b'B', b'c&d')], b'<A>a&amp;b</A><B>c&amp;d</B>') ,
            ([(b'A', b'a'), (b'B', None)], b'<A>a</A><B/>') ,
            ([(b'A', b'a'), (b'B', b'')], b'<A>a</A><B/>') ,
            )

        for (alist,ares) in lists:
            xplo=atpic.xplo.Xplo(alist)
            xml=xplo.toxml()
            print('XXX',(xplo.list(),xml),',')
            self.assertEqual(xml,ares)

    def test_get(self):
        lists=(
            ([(b'gallery',b'99'),(b'gallery',b'100')],b'99'),
            ([(b'nogallery',b'99'),(b'nogallery',b'100')],b''),
            )

        for (alist,exp) in lists:
            xplo=atpic.xplo.Xplo(alist)
            res=xplo.get(b'gallery')
            
            self.assertEqual(res,exp)



    def test_getkey(self):
        lists=(
            ([(b'gallery',b'99'),(b'gallery',b'100')],b'99'),
            ([(b'nogallery',b'99'),(b'nogallery',b'100')],None),
            )

        for (alist,exp) in lists:
            xplo=atpic.xplo.Xplo(alist)
            res=xplo.getkey(b'gallery')
            
            self.assertEqual(res,exp)

    def test_signature(self):
        lists=(
            ([(b'gallery',b'99'),(b'gallery',b'10')],b'gallery_gallery_'),
            ([(b'gallery',b'99'),(b'gallery',None)],b'gallery_gallery/'),
            )

        for (alist,asig) in lists:
            axplo=atpic.xplo.Xplo(alist)
            self.assertEqual(axplo.signature(),asig)


    def test_int(self):
        lists=(
            [(b'gallery',b'99'),(b'gallery',b'100')],
            )

        for alist in lists:
            xplo=atpic.xplo.Xplo(alist)
            nxplo=xplo.int()
            print(nxplo)
            # self.assertEqual(res,result)

if __name__=="__main__":
    unittest.main()
