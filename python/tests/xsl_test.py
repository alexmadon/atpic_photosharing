#!/usr/bin/python3
from lxml import etree
import lxml
# import lxml.usedoctest
import io
import atpic.xsl
import unittest



class worker_test(unittest.TestCase):
    """USER legacy urls"""

    def NOtest_rdf(self):
        print(atpic.xsl.mytrans_xslfile_xmlfile("xmp.xsl","fixture/xmp/sample_xmp.rdf"))

        # for xml xsl testing see
    # /usr/lib/python3/dist-packages/lxml
    #  and xrec
    def test_urls(self):
        xmlt=atpic.xsl.mytrans_xslfile_xmlfile("../atpic/alll.xsl","fixture/xml/pic1.xml")
        print(xmlt)
        # print(xmlt.to_string())
        # xmlt.parse()
        # xml_doc = etree.parse(io.StringIO(xmlt))
        print(dir(xmlt))
        # xml_doc = etree.parse(io.StringIO(xmlt.__str__()))
        # print(xmlt.xmlschema())
        # print(xmlt.relaxng())
        # lxml.lxmldoctest.install()
        el=xmlt.xpath('//*')
        print(el)
        print(dir(el[0]))
        print(el[0].nsmap)
        print(el[0].base)
        XHTML_NAMESPACE="http://www.w3.org/1999/xhtml"
        # a=xmlt.xpath('/{http://www.w3.org/1999/xhtml}html')
        # a=xmlt.xpath('//{http://www.w3.org/1999/xhtml}:a', namespaces={'None':XHTML_NAMESPACE})
        # print(a)
        # see source code of /usr/lib/python3/dist-packages/lxml/html/__init__.py
        XHTML_NAMESPACE = "http://www.w3.org/1999/xhtml"
        
        links_xpath = etree.XPath("descendant-or-self::a|descendant-or-self::x:a", namespaces={'x':XHTML_NAMESPACE})
        print(links_xpath)
        a=[el for el in links_xpath(xmlt)]
        print(a)
        b=links_xpath(xmlt)
        print(b)
        for link in b:
            print(dir(link))
            print(link.attrib)
        print("+++++++++++++++++++++++OR++++++++++++++")
        # res=xmlt.xpath("descendant-or-self::a|descendant-or-self::x:a", namespaces={'x':XHTML_NAMESPACE})
        res=xmlt.xpath("//x:a", namespaces={'x':XHTML_NAMESPACE})
        print(res)
        # does not work:
        # res=xmlt.findall("x:a", namespaces={'x':XHTML_NAMESPACE})
        # print(res)



if __name__=="__main__":
    unittest.main()
