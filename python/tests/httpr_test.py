import atpic.httpr
import unittest

verbui=[
("GET /dir1/dir2/dir3",("GET","/dir1/dir2/dir3")),

("STAT /dir1/dir2/dir3",("STAT","/dir1/dir2/dir3")),




]

class httpr_test(unittest.TestCase):

    def testverb(self):
        for testa in verbui:
            print testa
            
            (verb,uri)=atpic.httpr.splituri(testa[0])
            print verb
            print uri
            self.assertEqual(verb,testa[1][0])
            self.assertEqual(uri,testa[1][1])


    def test_get_content_length(self):
        # some headers
        headers2test=[
            (["GET /dir1 HTTP/1.1"],0),
            (["GET /dir1 HTTP/1.1",
              "Content-Length: 1999"],1999),
            (["GET /dir1 HTTP/1.1",
              "Content-Length: 1999",
              "Content-Type: txt/html"],1999),
            (["GET /dir1 HTTP/1.1",
              "\nContent-Length: 1999\n",
              "Content-Type: txt/html"],1999),
            
            ]
        for headers in headers2test:
            sizeok=headers[1]
            size=atpic.httpr.get_content_length(headers[0])
            print "size: %s, %s" % (sizeok,size)
            self.assertEqual(sizeok,size)



if __name__=="__main__":
    unittest.main()
