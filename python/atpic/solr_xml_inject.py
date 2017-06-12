#!/usr/bin/python3
"""
modify the solr calendar XML to inject an easier way to get years, month days requested
"""

from io import StringIO
from lxml import etree

# <str name="q">useryearmonth:1200310</str>
# solr_cal_ex1_usermonthday.xml

def insert_useryearmonth(user,year,month):
    # this is a dynamic XSL
    # copy most of it but insert at the top the search query parameters

    # xsl identity:
    xslt_string="""<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8"/>




<xsl:template match="@*|node()">
  <xsl:copy>
    <xsl:apply-templates select="@*|node()"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="response">
<response>
<query>
<year>"""+str(year)+"""</year>
<month>"""+str(month)+"""</month>
<first>"""+str(year)+"""-"""+str(month)+"""-01T00:00:00Z</first>
<user>"""+str(user)+"""</user>
</query>
<xsl:apply-templates/>
</response>
</xsl:template>

</xsl:stylesheet>
"""
    xslt_string=StringIO(xslt_string)
    xslt_doc = etree.parse(xslt_string)
    transform = etree.XSLT(xslt_doc)

    xmlfile="solr_cal_ex1_usermonthday.xml"
    xml_doc = etree.parse(xmlfile)
    xml_doc_new = transform(xml_doc)
    print(xml_doc_new)

if __name__ == "__main__":

    insert_useryearmonth(1,2003,10)
