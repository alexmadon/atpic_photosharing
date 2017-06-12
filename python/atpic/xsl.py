#!/usr/bin/python3
from lxml import etree
from io import BytesIO

"""
Simple wrapper to transform a XML document according to a XSL.

cf also: Usage: xsltproc [options] stylesheet file [file ...]

"""
def mytrans_xslstring_xmlfile(xsl_string,xmlfile):
    xslt_string=BytesIO(xsl_string)
    xslt_doc = etree.parse(xslt_string)
    transform = etree.XSLT(xslt_doc)

    xml_doc = etree.parse(xmlfile)
    xml_doc_new = transform(xml_doc)
    xml_string_new=str(xml_doc_new)
    # print(xml_string_new)
    return xml_string_new.encode('utf8')

def mytrans_xslfile_xmlstring(xslfile,xml_string):
    xslt_doc = etree.parse(xslfile)
    transform = etree.XSLT(xslt_doc)
    xml_string=BytesIO(xml_string)
    xml_doc = etree.parse(xml_string)


    xml_doc_new = transform(xml_doc)
    xml_string_new=str(xml_doc_new)
    return xml_string_new.encode('utf8')

def mytrans_xslfile_xmlfile(xslfile,xmlfile):

    # =========================================
    # test for FAQ
    # =========================================
    xslt_doc = etree.parse(xslfile)
    transform = etree.XSLT(xslt_doc)
    
    xml_doc = etree.parse(xmlfile)
    xml_doc_new = transform(xml_doc)
    xml_string_new=str(xml_doc_new)
    # print(xml_string_new)
    return xml_string_new.encode('utf8')

def mytrans_xslstring_xmlstring(xslt_string,xml_string):
    """Converts a XML string into another one using the XSLT string"""
    # unparsed-text file:///home/madon/books/wrox.press.xslt.2.0.programmers.reference.third.edition/9053final/lib0128.html
    # http://www.w3.org/TR/xslt#patterns
    # first convert strings to StringIO
    xslt_string=BytesIO(xslt_string)
    xslt_doc = etree.parse(xslt_string)
    transform = etree.XSLT(xslt_doc)


    xml_string=BytesIO(xml_string)
    xml_doc = etree.parse(xml_string)


    xml_doc_new = transform(xml_doc)
    # print(type(xml_doc_new))
    # print(dir(xml_doc_new))
    # print(xml_doc_new.__unicode__())
    xml_string_new=str(xml_doc_new).encode('utf8')
    # at this stage the type is probably Unicode 
    # (will need to encode it into a string)
    return xml_string_new


def example0():
    res=mytrans_xslfile_xmlfile('faq.xsl','faq.xml')
    print(res)

def example1():
    xslt_string= b'''
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<foo><xsl:value-of select="/a/b/text()" /></foo>
</xsl:template>
</xsl:stylesheet>'''
    


    xml_string= b'<a><b>Text</b></a>'
    
    a=mytrans_xslstring_xmlstring(xslt_string,xml_string)
    print(a)



def example2():

    # =========================================
    # test for FAQ
    # =========================================
    xslt_doc = etree.parse("faq.xsl")
    transform = etree.XSLT(xslt_doc)
    
    xml_doc = etree.parse("faq.xml")
    xml_doc_new = transform(xml_doc)
    xml_string_new=str(xml_doc_new)
    print(xml_string_new)
    

def example3():
    # =========================================
    # test for variables
    # =========================================
    # <?xml version="1.0" encoding="UTF-8"?>
    # <xsl:output method="html" encoding="UTF-8"/>
    # to avoid:
    # ValueError: Unicode strings with encoding declaration are not supported.
    # removed <?xml version="1.0" encoding="UTF-8"

    xslt_string= '''<?xml version="1.0"?>
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" encoding="UTF-8"/>
  
  <xsl:variable name="lang.id1">Welcome to XSLT!</xsl:variable>


  <xsl:template match="/">
    <html>
      <head>
        <title><xsl:value-of select="$lang.id1"/></title>
      </head>cet été là
     </html>
  </xsl:template>
</xsl:stylesheet>'''.encode('utf8')

    xml_string= b'<a><b>Text</b></a>'

    print(mytrans_xslstring_xmlstring(xslt_string,xml_string))



def example4():
    """
    Generate HTML forms from XML using curly braces {} 
    """

    xml_string= b"""<doc>
<input>
  <type>text</type>
  <name>FIRSTNAME</name>
  <value>James</value>
</input>
<input>
  <type>text</type>
  <name>LASTNAME</name>
  <value>Wolf</value>
</input>
</doc>"""





    xslt_string=b"""<?xml version="1.0"?>
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" encoding="UTF-8"/>
<xsl:template match="input">
  <input type="{type}" name="{name}" value="{value}"/>
</xsl:template>
</xsl:stylesheet>"""




    a=mytrans_xslstring_xmlstring(xslt_string,xml_string)
    print(a)

def example5():
    """
    Generate HTML forms from XML with errors
    """
    # http://zvon.org/xxl/XSLTreference/OutputExamples/example_1_20_frame.html
    print("example5")
    xml_string= b"""<doc>
<errors>
<password>Should contain digits.</password>
<password>Should contain upper case letters.</password>
</errors>
<data>
<username>alex</username>
<password>mysecret</password>
</data>
</doc>"""





    xslt_string=b"""<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8"/>




<xsl:template match="data/username">
  <input type="text" name="username" value="{.}"/>
  <xsl:apply-templates select="errors/username"/>
</xsl:template>

<xsl:template match="data/password">
  <input type="text" name="password" value="{.}"/>
  <xsl:apply-templates select="//errors/password" mode="error"/>
</xsl:template>


<xsl:template match="*" mode="error">
error:<xsl:apply-templates mode="error"/>
</xsl:template>

<xsl:template match="text()">
</xsl:template>


<xsl:template match="text()" mode="error">
  <xsl:copy>
    <xsl:apply-templates/>
  </xsl:copy>
</xsl:template>

</xsl:stylesheet>"""




    print(mytrans_xslstring_xmlstring(xslt_string,xml_string))





def example6():
    """
    Generate HTML forms from XML with errors. Same as above but more generic
    """
    # http://zvon.org/xxl/XSLTreference/OutputExamples/example_1_20_frame.html


    print("example6")
    xml_string= b"""<doc>
<username>
<data>alex</data>
<errors>
<error>Username already exists.</error>
</errors>
</username>


<password>
<data>mysecret</data>
<errors>
<error>Password should contain digits.</error>
<error>Password should contain upper case letters.</error>
</errors>
</password>

<country>
<data>France</data>
</country>
</doc>"""





    # You should never have curly brackets inside an XPath expression. 
    # http://www.dpawson.co.uk/xsl/sect2/N1575.html
    # Attribute Value Templates
    xslt_string=b"""<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8"/>

<xsl:template match="/">
The errors summary:
<xsl:apply-templates mode="summary" select="//error"/>
<xsl:apply-templates/></xsl:template>


<xsl:template match="error" mode="summary">
error:<xsl:apply-templates/>
</xsl:template>
<xsl:template match="error" mode="form">
errorfrom:<xsl:apply-templates/>
</xsl:template>


<xsl:template match="doc/*">
  <input type="text" name="{name(.)}" value="{data}"/>
<xsl:apply-templates select="errors/error" mode="form"/>
</xsl:template>



</xsl:stylesheet>"""




    print(mytrans_xslstring_xmlstring(xslt_string,xml_string))



def example7():
    """
    Generate HTML forms from XML with errors. Same as above but more generic
    """
    # http://zvon.org/xxl/XSLTreference/OutputExamples/example_1_20_frame.html


    print("example7")
    xml_string= b"""<doc>
<data>
<username>alex</username>
<password error="123">mysecret</password>
<country>France</country>
</data>
</doc>"""
    xslt_string=b"""<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8"/>


<xsl:template match="@*|node()">
  <xsl:copy>
    <xsl:apply-templates select="@*|node()"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="doc">
<A>
<xsl:apply-templates/>
</A>
</xsl:template>


</xsl:stylesheet>"""

    print(mytrans_xslstring_xmlstring(xslt_string,xml_string))

def example8():
    """
    Generate HTML forms from XML with errors. Same as above but more generic
    """
    # escape (see also disable output escaping)
    # http://codexmonkey.blogspot.com/2007/02/stupid-xslt-trick-1-escape-madness.html

    print("example8")
    xml_string= b"""<doc>
<data>
<username>alex</username>
<password error="123">mysecret</password>
<country>France</country>
</data>
</doc>"""
    xslt_string=b"""<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    version="1.0">
<xsl:output method="html" encoding="UTF-8"/>
<xsl:template match="/">
<someAlmostMarkup>
<xsl:apply-templates mode="escape" />
</someAlmostMarkup>
</xsl:template>

<xsl:template match="*" mode="escape">
<xsl:text>&lt;</xsl:text>
<xsl:value-of select="name()" />
<xsl:apply-templates mode="escape" select="@*" />
<xsl:text>&gt;</xsl:text>
<xsl:apply-templates mode="escape" />
<xsl:text>&lt;/</xsl:text>
<xsl:value-of select="name()" />
<xsl:text>&gt;</xsl:text>
</xsl:template>

<xsl:template match="@*" mode="escape">
<xsl:text> </xsl:text>
<xsl:value-of select="name()" />
<xsl:text>="</xsl:text>
<xsl:value-of select="." />
<xsl:text>"</xsl:text>
</xsl:template>

</xsl:stylesheet>"""

    print(mytrans_xslstring_xmlstring(xslt_string,xml_string))













def example9():
    """
    Same as example 4 and 5 but without the curly braces {}
    We use the more verbose xsl:element instead. 
    Generate HTML forms from XML with errors. Same as above but more generic
    """
    # escape (see also disable output escaping)
    # http://codexmonkey.blogspot.com/2007/02/stupid-xslt-trick-1-escape-madness.html

    print("example9")
    xml_string= b"""<doc>
<data>
<username>alex</username>
<password>mysecret<error>an error</error></password>
<country>France</country>
</data>
</doc>"""
    xslt_string=b"""<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    version="1.0">
<xsl:output method="xhtml" encoding="UTF-8"/>

<xsl:template match="doc/data/username|password|country">
<xsl:element name="input">
<xsl:attribute name="name">
<xsl:value-of select="name(.)"/>
</xsl:attribute>
<xsl:attribute name="value">
<xsl:value-of select="."/>
</xsl:attribute>
</xsl:element>
</xsl:template>



</xsl:stylesheet>"""

    print(mytrans_xslstring_xmlstring(xslt_string,xml_string))



def example10():
    """
    Same as example 9 but combined with example 8 escaping.
    Generate HTML forms from XML with errors. Same as above but more generic
    """
    # escape (see also disable output escaping)
    # http://codexmonkey.blogspot.com/2007/02/stupid-xslt-trick-1-escape-madness.html

    print("example10")
    xml_string= b"""<doc>
<data>
<username>alex</username>
<password>mysecret<error>an error</error></password>
<country>France</country>
</data>
</doc>"""
    xslt_string=b"""<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    version="1.0">
<xsl:output method="xhtml" encoding="UTF-8"/>

<xsl:template match="doc/data/username|password|country">
<xsl:element name="input">
<xsl:attribute name="name">
<xsl:value-of select="name(.)"/>
</xsl:attribute>
<xsl:attribute name="value">
<xsl:apply-templates mode="escape" />
</xsl:attribute>
</xsl:element>
</xsl:template>


<xsl:template match="*" mode="escape">
<xsl:text>&lt;</xsl:text>
<xsl:value-of select="name()" />
<xsl:apply-templates mode="escape" select="@*" />
<xsl:text>&gt;</xsl:text>
<xsl:apply-templates mode="escape" />
<xsl:text>&lt;/</xsl:text>
<xsl:value-of select="name()" />
<xsl:text>&gt;</xsl:text>
</xsl:template>

<xsl:template match="@*" mode="escape">
<xsl:text> </xsl:text>
<xsl:value-of select="name()" />
<xsl:text>="</xsl:text>
<xsl:value-of select="." />
<xsl:text>"</xsl:text>
</xsl:template>

</xsl:stylesheet>"""

    print(mytrans_xslstring_xmlstring(xslt_string,xml_string))









def example11():
    """
    The data layer is very close to the HTML name=value POST logics
    """
    # escape (see also disable output escaping)
    # http://codexmonkey.blogspot.com/2007/02/stupid-xslt-trick-1-escape-madness.html

    print("example11")
    xml_string= b"""<doc>
<errors>
<password>Should contain digits.</password>
<password>Should contain upper case letters.</password>
</errors>
<data>
<username>alex</username>
<password>mysecret</password>
<like>France</like>
<like>UK</like>
</data>
</doc>"""
    xslt_string=b"""<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8"/>

<xsl:template match="/doc/data">
<tr>
<xsl:apply-templates select="username" mode="input"/>
<xsl:apply-templates select="password" mode="input"/>
<xsl:apply-templates select="/doc/errors/password" mode="error"/>
<select name="like">
<xsl:apply-templates select="like" mode="option"/>
</select>
</tr>
</xsl:template>

<xsl:template match="/doc/errors/*"/>

<xsl:template match="*" mode="option">
  <option value="{.}"/>
</xsl:template>

<xsl:template match="*" mode="input">
  <input name="{name(.)}" value="{.}"/>
</xsl:template>



<xsl:template match="*" mode="error">
<li>Error: <xsl:apply-templates/></li>
</xsl:template>

</xsl:stylesheet>"""

    print(mytrans_xslstring_xmlstring(xslt_string,xml_string))






def example12():
    """
    Same as example 9 but combined with example 8 escaping.
    Generate HTML forms from XML with errors. Same as above but more generic
    """
    # escape (see also disable output escaping)
    # http://codexmonkey.blogspot.com/2007/02/stupid-xslt-trick-1-escape-madness.html

    print("example12")
    xml_string= b"""<doc>
<user>
<fields>
<name>Alex</name>
</fields>
<children>
<pic>
avignon
</pic>
<pic>
paris
</pic>
</children>
</user>
</doc>"""
    xslt_string=b"""<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
<xsl:output method="xhtml" encoding="UTF-8"/>


<xsl:template match="/doc/user/fields">
<div><xsl:apply-templates/></div>
</xsl:template>

<xsl:template match="/doc/user/fields/name">
<h1><xsl:apply-templates/></h1>
</xsl:template>

<xsl:template match="/doc/user/children/pic">
<h2><xsl:apply-templates/></h2>
</xsl:template>

</xsl:stylesheet>"""

    print(mytrans_xslstring_xmlstring(xslt_string,xml_string))











def example13():
    """
    The data layer is very close to the HTML name=value POST logics
    """
    # escape (see also disable output escaping)
    # http://codexmonkey.blogspot.com/2007/02/stupid-xslt-trick-1-escape-madness.html

    print("example13")
    xml_string= b"""<doc>
<errors>
<password>Should contain digits.</password>
<password>Should contain upper case letters.</password>
</errors>
<data>
<username>alex</username>
<password>mysecret</password>
<like>France</like>
<like>UK</like>
</data>
</doc>"""
    xslt_string=b"""<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8"/>


<xsl:template match="/doc/errors">
NOTHING
</xsl:template>

<xsl:template match="/doc/data">
<div><xsl:apply-templates/></div>
</xsl:template>
<xsl:template match="/doc/data/username">
<input><xsl:apply-templates/></input>
</xsl:template>


</xsl:stylesheet>"""

    print(mytrans_xslstring_xmlstring(xslt_string,xml_string))


def example14():
    res=mytrans_xslfile_xmlfile('xslt_dates.xsl','ttt.xml')
    print(res)




if __name__ == "__main__":
    # example1()

    # quit()
    # example2()
    # example3()
    # example4()
    # example5()
    # example6()
    # example7()
    # example8()
    # example9()
    # example10()
    # example11()
    # example12()
    # example13()
    # example14()
    xslfile=b'xml2json_at.xsl'
    xmlfile=b'gallery_list_example.xml'
    print(mytrans_xslfile_xmlfile(xslfile,xmlfile).decode('utf8'))
