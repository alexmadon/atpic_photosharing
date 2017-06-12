#!/usr/bin/python3
# -*- coding: utf-8 -*-
import atpic.xmlat


import unittest

class xml_test(unittest.TestCase):
    """USER legacy urls"""


    def testExtractWikis(self):
        """Extract Wikis ID"""
        xml='<faq><t id="45">Blah1</t><b><t id="49">Blah2</t></b></faq>'
        extracted=atpic.xmlat.extract_id(xml)
        extracted_ok={'45':"Blah1",'49':"Blah2"}
        # print extracted
        # print extracted_ok
        self.assertEqual(extracted['45'],extracted_ok['45'])
        self.assertEqual(extracted['49'],extracted_ok['49'])

    def testExtractWikisDeep(self):
        """Extract Wikis ID"""
        xml='<faq>META<t id="49">Blah2<a href="/home">Home</a>Blah3</t></faq>'
        extracted=atpic.xmlat.extract_id(xml)
        extracted_ok={'49':'Blah2<a href="/home">Home</a>Blah3'}
        # print extracted
        # print extracted_ok
        self.assertEqual(extracted['49'],extracted_ok['49'])


    def testReplaceIdWikiOn(self):
        xml='<faq>META<t id="49">Nice<a href="/home">Home</a>expensive</t>river<t id="88">Thames</t>ppp</faq>'
        dictids={}
        dictids['49']='Belle<a href="/home">Maison</a>chere'
        dictids['88']='Tamise'
        xmltranslated=atpic.xmlat.replace_id(xml,dictids,wiki='on')
        xmltranslated_should="""<?xml version="1.0" ?><faq>META<t id="49" wiki="on">Belle<a href="/home">Maison</a>chere</t>river<t id="88" wiki="on">Tamise</t>ppp</faq>"""

        # print(xmltranslated)
        # print(xmltranslated_should)
        self.assertEqual(xmltranslated,xmltranslated_should)

    def testReplaceIdWikiOffUnicode(self):
        xml='<faq>été <t id="49">là</t></faq>'
        dictids={}
        dictids['49']='Là'
        
        xmltranslated=atpic.xmlat.replace_id(xml,dictids,wiki='off')
        xmltranslated_should="""<?xml version="1.0" ?><faq>été <t id="49">Là</t></faq>"""
        # print(xmltranslated)
        # print(xmltranslated_should)
        self.assertEqual(xmltranslated,xmltranslated_should)


    def testReplaceIdWikiOff(self):
        xml='<faq>META<t id="49">Nice<a href="/home">Home</a>expensive</t>river<t id="88">Thames</t>ppp</faq>'
        dictids={}
        dictids['49']='Belle<a href="/home">Maison</a>chere'
        dictids['88']='Tamise'
        xmltranslated=atpic.xmlat.replace_id(xml,dictids,wiki='off')
        xmltranslated_should="""<?xml version="1.0" ?><faq>META<t id="49">Belle<a href="/home">Maison</a>chere</t>river<t id="88">Tamise</t>ppp</faq>"""
        # print(xmltranslated)
        # print(xmltranslated_should)
        self.assertEqual(xmltranslated,xmltranslated_should)

    def testReplaceIdWikiOffMissingKey(self):
        xml='<faq>META<t id="49">Nice<a href="/home">Home</a>expensive</t>river<t id="88">Thames</t>ppp</faq>'
        dictids={}
        dictids['49']='Belle<a href="/home">Maison</a>chere'
        # Missing key test
        # dictids['88']='Tamise'
        xmltranslated=atpic.xmlat.replace_id(xml,dictids,wiki='off')
        xmltranslated_should="""<?xml version="1.0" ?><faq>META<t id="49">Belle<a href="/home">Maison</a>chere</t>river<t id="88" missing="1">Thames</t>ppp</faq>"""
        self.assertEqual(xmltranslated,xmltranslated_should)


    def testText(self):
        """should remove the tags"""
        soup="une <b>belle</b> soupe"
        cleaned_expected="une belle soupe"
        cleaned=atpic.xmlat.extract_text(soup)
        self.assertEqual(cleaned_expected,cleaned)

    def testTextDeeper(self):
        """should remove the tags"""
        soup="""une <b><a href="toto">belle</a> soupe</b>"""
        cleaned_expected="une belle soupe"
        cleaned=atpic.xmlat.extract_text(soup)
        self.assertEqual(cleaned_expected,cleaned)


    def testTextDeeperUtf8(self):
        """should remove the tags"""
        soup="""Cet <b><a href="toto">été là</a> !</b>"""
        cleaned_expected="Cet été là !"
        cleaned=atpic.xmlat.extract_text(soup)
        self.assertEqual(cleaned_expected,cleaned)


    def testEscape(self):
        """should escape the tags"""
        xml="""<faq><a href="http://atpic.com">Some</a> good <i>xml</i>: <escape mode="ok">this is <b>important</b></escape></faq>"""
        taglist=["escape"]
        escaped_ok="""<?xml version="1.0" ?><faq><a href="http://atpic.com">Some</a> good <i>xml</i>: <escape mode="ok">this is &lt;b&gt;important&lt;/b&gt;</escape></faq>"""
        escaped=atpic.xmlat.escape_xml(xml,taglist)
        # print(escaped_ok)
        # print(escaped)
        self.assertEqual(escaped_ok,escaped)




    def testEscapeUnicode(self):
        """should escape the tags"""
        xml="""<faq>été<escape>là</escape></faq>"""
        taglist=["escape"]
        escaped_ok="""<?xml version="1.0" ?><faq>été<escape>là</escape></faq>"""
        escaped=atpic.xmlat.escape_xml(xml,taglist)
        # print(escaped_ok)
        # print(escaped)
        self.assertEqual(escaped_ok,escaped)


if __name__ == "__main__":
    unittest.main()
