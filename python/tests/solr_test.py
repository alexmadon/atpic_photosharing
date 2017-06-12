"""Unit tests for URL dispatcher"""
import unittest


import atpic.solr
from lxml import etree
from StringIO import StringIO


def extract_one(xpath,xml):
    """xpath example: /a/b/text() """
    xslt_string= StringIO('''
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<foo><xsl:value-of select="%s" /></foo></xsl:template></xsl:stylesheet>''' % xpath)
    xslt_doc = etree.parse(xslt_string)
    transform = etree.XSLT(xslt_doc)
    xml_string= StringIO(xml)
    xml_doc = etree.parse(xml_string)
    xml_doc_new = transform(xml_doc)
    xml_string_new=str(xml_doc_new)
    return xml_string_new



class solr_test(unittest.TestCase):
    """USER legacy urls"""


    def testSolrKey(self):
        """solr key"""
        xml=atpic.solr.solr_generate('p',1)
        print xml
        xml_extract=extract_one("/add/doc/*[@name='key']/text()",xml)
        xml_extract_expected="""<?xml version="1.0"?>\n<foo>p1</foo>\n"""
        self.assertEqual(xml_extract,xml_extract_expected)


        xml_extract=extract_one("/add/doc/*[@name='type']/text()",xml)
        xml_extract_expected="""<?xml version="1.0"?>\n<foo>pic</foo>\n"""
        self.assertEqual(xml_extract,xml_extract_expected)




if __name__=="__main__":
    unittest.main()
