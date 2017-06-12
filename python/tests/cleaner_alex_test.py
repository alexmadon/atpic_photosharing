#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest


from cgi import escape


import atpic.cleaner_alex


check_sql = (
(b'Alex & Dama',b'Alex &amp; Dama'),
(b"Alex & 'Dama'",b"Alex &amp; 'Dama'"),
(b'<b>bold</b>',b'<b>bold</b>'),
(b'alex@example.foo',b'alex@example.foo'),
(b'<script>thescript</script>',b'thescript'),
(b'<img src="toto1.jpg"/>',b'<img />'),
(b'<img src="http://atpic.com/toto1.jpg"/>',b'<img src="http://atpic.com/toto1.jpg" />'),
(b'<img src="toto.jpg" onlick="javas()">',b'<img />'),
(b"""<a href="http://atpic.com">atpic.com</a>""",b"""<a href="http://atpic.com">atpic.com</a>"""),
(b"<a>alex<b></a></b>",b"<a>alex</a>"),
(b"""<a href="onclick(alarm(b'bump')">alex</a>""",b"""<a>alex</a>"""),
(b'<script>',b''),
(b'<script/>',b''),
(b'</script>',b''),
(b'<script woo=yay>',b''),
(b'<script woo="yay">',b''),
(b'<script woo="yay>',b''),
(b'<script',b''),
(b'<script woo="yay<b>',b''),
(b'<script woo="yay<b>hello',b''),
(b'<script<script>>',b''),
(b'<<script>script<script>>',b'&lt;script&lt;script&gt;&gt;'),
(b'<<script><script>>',b'&lt;&lt;script&gt;&gt;'),
(b'<<script>script>>',b'&lt;script&gt;&gt;'),
(b'<<script<script>>',b''),
# (b'# bad protocols',),
(b'<a href="http://foo.com">bar</a>',b'<a href="http://foo.com">bar</a>'),
(b'<a href="http://foo">bar</a>',b'<a>bar</a>'),
(b'<a href="ftp://foo.com">bar</a>',b'<a href="ftp://foo.com">bar</a>'),
(b'<a href="ftp://foo">bar</a>',b'<a>bar</a>'),
(b'<a href="mailto:foo">bar</a>',b'<a>bar</a>'),
(b'<a href="javascript:foo">bar</a>',b'<a>bar</a>'),
(b'<a href="java script:foo">bar</a>',b'<a>bar</a>'),
(b'<a href="java'+b'\t'+b'script:foo">bar</a>',b'<a>bar</a>'),
(b'<a href="java'+b'\n'+b'script:foo">bar</a>',b'<a>bar</a>'),
(b'<a href="java'+b'\r'+b'script:foo">bar</a>',b'<a>bar</a>'),
(b'<a href="java'+chr(1).encode('utf8')+b'script:foo">bar</a>',b'<a>bar</a>'),
(b'<a href="java'+chr(0).encode('utf8')+b'script:foo">bar</a>',b'<a>bar</a>'),
(b'<a href="jscript:foo">bar</a>',b'<a>bar</a>'),
(b'<a href="vbscript:foo">bar</a>',b'<a>bar</a>'),
(b'<a href="view-source:foo">bar</a>',b'<a>bar</a>'),
(b'<a href="  javascript:foo">bar</a>',b'<a>bar</a>'),
(b'<a href="jAvAsCrIpT:foo">bar</a>',b'<a>bar</a>'),
# (b'# bad protocols with entities (semicolons)',),
(b'<a href="&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;foo">bar</a>',b'<a>bar</a>'),
(b'<a href="&#0000106;&#0000097;&#0000118;&#0000097;&#0000115;&#0000099;&#0000114;&#0000105;&#0000112;&#0000116;&#0000058;foo">bar</a>',b'<a>bar</a>'),
(b'<a href="&#x6A;&#x61;&#x76;&#x61;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;&#x3A;foo">bar</a>',b'<a>bar</a>'),

# (b'# bad protocols with entities (no semicolons)',),
(b'<a href="&#106&#97&#118&#97&#115&#99&#114&#105&#112&#116&#58;foo">bar</a>',b'<a>bar</a>'),
(b'<a href="&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058foo">bar</a>',b'<a>bar</a>'),
(b'<a href="&#x6A&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3A;foo">bar</a>',b'<a>bar</a>'),


)



class cleaner_test(unittest.TestCase):
    """html filter"""

    def test_cleaner_xml(self):
        """clean to SQL XML"""
        for test in check_sql:
            # print test
            # we check the option
            ret = atpic.cleaner_alex.clean(test[0])
            print("%s => %s" % (test[0],ret))
            self.assertEqual(ret,test[1])
   


if __name__ == "__main__":
    unittest.main()
