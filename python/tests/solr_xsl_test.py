
import atpic.xsl
infilename="./fixture/solr_result.xml"
infile = open( infilename, "r" )
xml_string=infile.read()
infile.close()

xslt_string="""
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="xml" omit-xml-declaration="yes" encoding="utf8" indent="yes"/>


<xsl:template match='/'>
        <xsl:apply-templates select="response/result/doc"/>
</xsl:template>



<xsl:template match="doc">
<doc>
<xsl:apply-templates/>
</doc>
</xsl:template>



<xsl:template match="doc/*">
 <xsl:element name= "{@name}">
        <xsl:value-of select="."/>
</xsl:element>
</xsl:template>


  <xsl:template match="*"/>

</xsl:stylesheet>
"""

print atpic.xsl.transform(xml_string,xslt_string)
