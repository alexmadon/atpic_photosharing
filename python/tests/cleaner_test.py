#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest


import atpic.cleaner

check_html = (
('présenté à'.encode('utf8'),'présenté à'.encode('utf8')),
(b'&agrave;','à'.encode('utf8')),
(b'Alex & Dama',b'Alex &amp; Dama'),
(b"Alex & 'Dama'",b"Alex &amp; 'Dama'"),
(b'<b>bold</b>',b'<b>bold</b>'),
(b'alex@example.foo',b'alex@example.foo'),
# (b'<script>thescript</script>',b'thescript'),
(b'<script>thescript</script>',b'thescript'),
(b'<img src="http://atpic.com/toto1.jpg"/>',b'<img src="http://atpic.com/toto1.jpg" />'),
(b'<img src="http://atpic.com/toto.jpg" onlick="javas()">',b'<img src="http://atpic.com/toto.jpg" />'),
(b'<a href="http://atpic.com">atpic.com</a>',b'<a href="http://atpic.com">atpic.com</a>'),
(b'&nbsp;',b'\xc2\xa0'), # b'&nbsp;'),
(b'&copy;','©'.encode('utf8')),
("Lierre&pétale".encode('utf8'),"Lierre&amp;pétale".encode('utf8')),
(b'<div aaa="bbb">alex</div>',b'<div>alex</div>'),
(b'<span aaa="bbb">alex</span>',b'<span>alex</span>'),
(b'<p aaa="bbb">alex</p>',b'<p>alex</p>'),
(b'<br aaa="bbb">alex</br>',b'<br />\nalex'),
)

check_txt = (
(b'Alex & Dama',b'Alex &amp; Dama'),
(b"Alex <b>Dama</b>",b"Alex Dama"),
(b'',b''),
(b'>alex',b'&gt;alex'),
(b"apos'troph",b"apos&#39;troph"),
('<b>présenté</b> à'.encode('utf8'),'présenté à'.encode('utf8')),
(b'&agrave;','à'.encode('utf8')),
# (b'&nbsp;','\xc2\xa0'),
(b'&nbsp;',b' '),
(b'alex&nbsp;madon',b'alex madon'),
(b'"',b'&quot;'),
(b'&copy;','©'.encode('utf8')),
(b'<',b''),
(b'10<11',b'10&lt;11'),
(b'alex<',b'alex'),
(b'alex<-go',b'alex&lt;-go'),
(b'>',b'&gt;'), # this is a known XML entity
(b'&pound;','£'.encode('utf8')),
(b'<!-- comment -->',b''),
(b'no <!-- comment --> comment',b'no comment'),
)


check_escape=(
("cet été là".encode('utf8'),"cet été là".encode('utf8')),
(b'<b>bold</b>',b'&lt;b&gt;bold&lt;/b&gt;'),
(b"a<hr/>b",b"a\n&lt;hr /&gt;\nb"),
(b"a\n<hr/>\nb",b"a\n&lt;hr /&gt;\nb"),
(b"a<br/>b",b"a&lt;br /&gt;\nb"),
(b"a<div>b</div>",b"a\n&lt;div&gt;b&lt;/div&gt;"),
(b"a<p>b</p>",b"a\n&lt;p&gt;b&lt;/p&gt;"),
("Lierre&pétale".encode('utf8'),"Lierre&amp;amp;pétale".encode('utf8')),
(b'he is "silly"',b"he is &quot;silly&quot;"),
(b'<a href="http://atpic.com">ATPIC</a>',b'&lt;a href=&quot;http://atpic.com&quot;&gt;ATPIC&lt;/a&gt;'),
# (b'alex\nmadon',b'alex\nmadon'),
)


check_wiki=(
    (b'alex\nmadon',b'alex\nmadon'),
    (b'a < b',b'a &lt; b'), # security? code for <

)

class cleaner_test(unittest.TestCase):
# class cleaner_test():
    """html filter"""

   
    def test_cleaner_txt(self):
        """clean to TXT"""
        for test in check_txt:
            print(test)
            # we check the option
            ret = atpic.cleaner.txt(test[0])
            print("%s => %s" % (test[0],ret))
            self.assertEqual(ret,test[1])
   
    def test_cleaner_html(self):
        """clean to HTML"""
        for test in check_html:
            # print test
            # we check the option
            ret = atpic.cleaner.html(test[0])
            print("%s => %s" % (test[0],ret))
            self.assertEqual(ret,test[1])


# class cleaner_escape_test(unittest.TestCase):
#     """html filter"""

    def test_cleaner_escape(self):
        """clean to escaped"""
        for test in check_escape:
            # print test
            # we check the option
            ret = atpic.cleaner.escape(test[0])
            print("AAAA%s => %s" % (test[0],ret))
            self.assertEqual(ret,test[1])
   

    def test_cleaner_escape_eq_unescape_escape(self):
        """clean to escaped=escape_unescape_escape"""
        for test in check_escape:
            # print test
            # we check the option
            ret = atpic.cleaner.escape(test[0])
            ret2=atpic.cleaner.escape(atpic.cleaner.unescape(ret))
            print("%s => %s" % (test[0],ret))
            self.assertEqual(ret,ret2)
   

    def test_cleaner_escape_unescape_eq_unescape_escape_unescape(self):
        """clean to escaped_unescape=escape_unescape_escape_unescape"""
        for test in check_escape:
            # print test
            # we check the option
            ret = atpic.cleaner.unescape(atpic.cleaner.escape(test[0]))
            ret2=atpic.cleaner.unescape(atpic.cleaner.escape(atpic.cleaner.unescape(ret)))
            print("%s => %s" % (test[0],ret))
            self.assertEqual(ret,ret2)
   




    def test_cleanwiki(self):
        print("============wiki========")
        for (st,st_ex) in check_wiki:
            # print test
            # we check the option
            st1=atpic.cleaner.cleanwiki(st)
            print(st,'->',st1)
            print('compare',(st1,st_ex))
            self.assertEqual(st1,st_ex)
   


if __name__ == "__main__":
    unittest.main()
