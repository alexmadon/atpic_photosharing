#!/usr/bin/python3
"""
Transforms a XML model into SQL CREATE, ALTER, etc...



 ./model_xml2db.py -cTIC -t_entry,_entry_line
 ./model_xml2db.py -cTIC 

"""
import getopt
import sys

import atpic.xsl

def get_xsl_tables(atable):
    xsl=[]
    xsl.append(b"""<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">""")
    xsl.append(b"""<xsl:output method="xml" omit-xml-declaration="yes" encoding="utf8" indent="yes"/>""")

    xsl.append(b"""
<xsl:template match="@*|node()">
  <xsl:copy>
    <xsl:apply-templates select="@*|node()"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="/">
    <xsl:apply-templates select="/model/table"/>
</xsl:template>

<xsl:template match="table">
<xsl:if test="@name='"""+atable+b"""'">
  <xsl:copy>
    <xsl:apply-templates select="@*|node()"/>
  </xsl:copy>
</xsl:if>
</xsl:template>

""" )

    xsl.append(b"""</xsl:stylesheet>""")
    xsls=b"\n".join(xsl)
    return xsls


def get_xsl(operation,relation):
    xsl=[]
    xsl.append(b"""<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">""")
    xsl.append(b"""<xsl:output method="xml" omit-xml-declaration="yes" encoding="utf8" indent="yes"/>""")

    if operation=="create":

        if relation=="COMMENT":            
            xsl.append(b"""
<xsl:template match="/">
<xsl:apply-templates/>
</xsl:template>

<xsl:template match="table">
-- <xsl:value-of select="@name"/>;
<xsl:apply-templates select="attribute"/>
</xsl:template>

<xsl:template match="attribute">
COMMENT ON COLUMN <xsl:value-of select="../@name"/>.<xsl:value-of select="@name"/> IS 'read="<xsl:value-of select="@read"/><xsl:text>" write="</xsl:text><xsl:value-of select="@write"/><xsl:text>" comment="</xsl:text><xsl:value-of select="@comment"/><xsl:text>"</xsl:text>' ;
</xsl:template>
""")
        if relation=="CONSTRAINT":            
            xsl.append(b"""
<xsl:template match="/">
<xsl:apply-templates/>
</xsl:template>

<xsl:template match="table">
-- <xsl:value-of select="@name"/>;
<xsl:apply-templates select="constraint"/>
</xsl:template>

<xsl:template match="constraint">
ALTER TABLE <xsl:value-of select="../@name"/> ADD CONSTRAINT <xsl:value-of select="@name"/><xsl:text> </xsl:text><xsl:value-of select="@condef"/> DEFERRABLE INITIALLY DEFERRED;
</xsl:template>""")

            
        if relation=="DEFAULT":
            xsl.append(b"""
<xsl:template match="table">
<xsl:apply-templates/>
<!-- 
ALTER TABLE $table ALTER COLUMN $column SET DEFAULT $thedefault;
ALTER TABLE $table ALTER COLUMN $column DROP DEFAULT;
 -->
</xsl:template>

<xsl:template match="attribute">
<xsl:choose>
<xsl:when test="substring(@attrel,1,7)='nextval'">
ALTER TABLE <xsl:value-of select="../@name"/> ALTER COLUMN <xsl:value-of select="@name"/> SET DEFAULT nextval(('<xsl:value-of select="../@name"/>__seq'::text)::regclass);
</xsl:when>
<xsl:when test="string-length(@attrel)>0">
ALTER TABLE <xsl:value-of select="../@name"/> ALTER COLUMN <xsl:value-of select="@name"/> SET DEFAULT <xsl:value-of select="@attrel"/>;
</xsl:when>
<xsl:otherwise>
</xsl:otherwise>
</xsl:choose>

</xsl:template>
""")
        if relation=="INDEX":

            xsl.append(b"""
<xsl:template match="/">
<xsl:apply-templates/>
</xsl:template>

<xsl:template match="table">
-- <xsl:value-of select="@name"/>;
<xsl:apply-templates select="index"/>
</xsl:template>

<xsl:template match="index">
<xsl:value-of select="@indexdef"/>;
</xsl:template>

""")
        if relation=="NOTNULL":
            xsl.append(b"""
<xsl:template match="/">
<xsl:apply-templates/>
</xsl:template>

<xsl:template match="table">
<xsl:apply-templates select="attribute"/>
</xsl:template>

<!-- 
ALTER TABLE $table ALTER COLUMN $column SET DEFAULT $thedefault;
ALTER TABLE $table ALTER COLUMN $column $setdrop NOT NULL;
 -->
<xsl:template match="attribute">
<xsl:if test="@notnull='t'">
ALTER TABLE <xsl:value-of select="../@name"/> ALTER COLUMN  <xsl:value-of select="@name"/> SET NOT NULL;
</xsl:if>
</xsl:template>

""")
        if relation=="TABLE":
            xsl.append(b"""
<xsl:template match="/">
<xsl:apply-templates/>
</xsl:template>

<xsl:template match="table">
CREATE TABLE <xsl:value-of select="@name"/> (<xsl:apply-templates select="attribute"/>);
</xsl:template>

<xsl:template match="attribute">
<xsl:value-of select="@name"/>
<xsl:text> </xsl:text>
<xsl:value-of select="@type"/>
<xsl:if test="name() = name(following-sibling::*)">,</xsl:if><!-- like in json -->
</xsl:template>
""")
        if relation=="SEQUENCE":

            xsl.append(b"""
<xsl:template match="/">
<xsl:apply-templates/>
</xsl:template>

<xsl:template match="table">
-- <xsl:value-of select="@name"/>;
<xsl:apply-templates select="sequence"/>
</xsl:template>

<xsl:template match="sequence">
CREATE SEQUENCE <xsl:value-of select="@name"/>;
SELECT setval('<xsl:value-of select="@name"/>',max(<xsl:value-of select="@attname"/>)) FROM <xsl:value-of select="../@name"/>;
</xsl:template>

""")
            






















    if operation=="drop":

        if relation=="CONSTRAINT":            
            xsl.append(b"""
<xsl:template match="/">
<xsl:apply-templates/>
</xsl:template>

<xsl:template match="table">
-- <xsl:value-of select="@name"/>;
<xsl:apply-templates select="constraint"/>
</xsl:template>

<xsl:template match="constraint">
ALTER TABLE <xsl:value-of select="../@name"/> DROP CONSTRAINT <xsl:value-of select="@name"/>;
</xsl:template>""")

            
        if relation=="DEFAULT":
            xsl.append(b"""
<xsl:template match="table">
<xsl:apply-templates select="attribute"/>
<!-- 
ALTER TABLE $table ALTER COLUMN $column SET DEFAULT $thedefault;
ALTER TABLE $table ALTER COLUMN $column DROP DEFAULT;
 -->
</xsl:template>

<xsl:template match="attribute">
<xsl:if test="@attrel!='None'">
ALTER TABLE <xsl:value-of select="../@name"/> ALTER COLUMN   <xsl:value-of select="@name"/> DROP DEFAULT;
</xsl:if>
</xsl:template>
""")
        if relation=="INDEX":

            xsl.append(b"""
<xsl:template match="/">
<xsl:apply-templates/>
</xsl:template>

<xsl:template match="table">
-- <xsl:value-of select="@name"/>;
<xsl:apply-templates select="index"/>
</xsl:template>

<xsl:template match="index">
DROP INDEX <xsl:value-of select="@name"/>;
</xsl:template>

""")
        if relation=="NOTNULL":
            xsl.append(b"""
<xsl:template match="/">
<xsl:apply-templates/>
</xsl:template>

<xsl:template match="table">
<xsl:apply-templates select="attribute"/>
</xsl:template>

<!-- 
ALTER TABLE $table ALTER COLUMN $column SET DEFAULT $thedefault;
ALTER TABLE $table ALTER COLUMN $column $setdrop NOT NULL;
 -->
<xsl:template match="attribute">
<xsl:if test="@notnull='True'">
ALTER TABLE <xsl:value-of select="../@name"/> ALTER COLUMN  <xsl:value-of select="@name"/> DROP NOT NULL;
</xsl:if>
</xsl:template>

""")
        if relation=="TABLE":
            xsl.append(b"""
<xsl:template match="/">
<xsl:apply-templates/>
</xsl:template>

<xsl:template match="table">
DROP TABLE <xsl:value-of select="@name"/> CASCADE;
</xsl:template>
""")
            
        if relation=="SEQUENCE":

            xsl.append(b"""
<xsl:template match="/">
<xsl:apply-templates/>
</xsl:template>

<xsl:template match="table">
-- <xsl:value-of select="@name"/>;
<xsl:apply-templates select="sequence"/>
</xsl:template>

<xsl:template match="sequence">
DROP SEQUENCE <xsl:value-of select="@name"/>;
</xsl:template>

""")








    xsl.append(b"""</xsl:stylesheet>""")
    xsls=b"\n".join(xsl)
    return xsls

def display_help():
    print ("""Usage:

-h: help
-c: create
-d: delete
-C: this is a Constraint
-D: this is a Default
-I: this is a Index
-N: this is a Notnull
-T: this is a Table
-S: this is a Sequence
-M: this is a coMMent
-f: model file (default model1.xml)
-t: list of tables (default all)

Examples:
 ./model_xml2db.py -cTIC -t_entry,_entry_line
 ./model_xml2db.py -cTIC 
 ./model_xml2db.py -cDMt _user_gallery_pic,_user_gallery > tt.sql
# drop everything except Tables
./model_xml2db.py -d -CDINSM
# create everything but Tables
./model_xml2db.py -c -CDINSM

""")

if __name__ == "__main__":
    # default values
    operation='create'
    relations=[]
    tablecsv=None
    optlist, list = getopt.getopt(sys.argv[1:], 'f:cdTICNSDMt:h')
    modelxmlfile="model1.xml"
    showhelp=False
    for option in optlist:
        if option[0] == '-h':
            showhelp=True
        if option[0] == '-t':
            tablecsv=option[1].encode('utf8')
        if option[0] == '-f':
            modelxmlfile=option[1].encode('utf8')
            # print ("tables csv found ",tablecsv)

        if option[0] == '-c':
            # this is a create
            operation='create'
        if option[0] == '-d':
            # this is a drop
            operation='drop'
        if option[0] == '-C':
            # this is a Constraint
            relations.append('CONSTRAINT')
        if option[0] == '-D':
            # this is a Default
            relations.append('DEFAULT')
        if option[0] == '-I':
            # this is Index
            relations.append('INDEX')
        if option[0] == '-N':
            # this is a Notnull
            relations.append('NOTNULL')
        if option[0] == '-T':
            # this is a Table
            relations.append('TABLE')
        if option[0] == '-S':
            # this is a Sequence
            relations.append('SEQUENCE')
        if option[0] == '-M':
            # this is a coMMent
            relations.append('COMMENT')

    if len(relations)==0 or showhelp:
        display_help()
    # quit()
    if tablecsv:
        tables=tablecsv.split(b',')
        for atable in tables:
            # first we need to take only wanted tables: identity fro a table list
            xsl=get_xsl_tables(atable)
            # print(xsl)
            xmlmodel=atpic.xsl.mytrans_xslstring_xmlfile(xsl,modelxmlfile)
            # print(xmlmodel)
            # print(dir(xmlmodel))
            # xmlmodel="%s" % xmlmodel
            for relation in relations:
                xsl=get_xsl(operation,relation)
                xml=atpic.xsl.mytrans_xslstring_xmlstring(xsl,xmlmodel)
                print(xml.decode('utf8'))
        # print('done 1')        
    else:
        
        f=open(modelxmlfile,'rb')
        xmlmodel=f.read()
        # print(type(xmlmodel))
        f.close()
        for relation in relations:
            xsl=get_xsl(operation,relation)
            xml=atpic.xsl.mytrans_xslstring_xmlstring(xsl,xmlmodel)
            print(xml.decode('utf8'))


# example:
# ./model_xml2db.py -cDMt _user_gallery_pic,_user_gallery > tt.sql
