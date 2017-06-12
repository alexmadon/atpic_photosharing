"""
All possible XSLs

"""

def getxsl(dispatcher,environ):
    print dispatcher
    xsl=[]
    NOxsl=[]
    if dispatcher["native"]=="xml":
        xsl.append("""<xsl:stylesheet version="1.0" """)
        xsl.append("""xmlns="http://www.w3.org/1999/xhtml" """) # the default name space used in the xsl
        xsl.append("""xmlns:xsl="http://www.w3.org/1999/XSL/Transform" """)# the xsl name space used in the transform
        xsl.append("""xmlns:atpic="http://atpic.com/atpicns" """) #  the atpic name space used in the original XML
        # xsl.append("""xmlns:css="http://www.w3.org/TR/XSL-for-CSS" """)
        xsl.append(""">""")

        if dispatcher["format"]=="xhtml" or dispatcher["format"]=="robot" :
            xsl.append("""<xsl:output method="xml"/>""")
            xsl.append("""<xsl:output omit-xml-declaration="no"/>""") 
            xsl.append("""<xsl:output encoding="UTF-8" />""")
            xsl.append("""<xsl:output indent="yes"/>""")
            # see http://www.xml.com/pub/a/2002/09/04/xslt.html?page=2

            # xsl.append("""<xsl:output doctype-public="-//W3C//DTD XHTML 1.1//EN"/>""")
            # xsl.append("""<xsl:output doctype-system="http://www.w3.org/tr/xhtml11/DTD/xhtml11.dtd"/>""")
            
            
            # xhtml11 target
            xsl.append("""<xsl:output doctype-public="-//atpic.com//DTD XHTML 1.1 plus Target 1.0//EN"/>""")
            xsl.append("""<xsl:output doctype-system="http://atpic.com/dtd/xhtml11-target.dtd"/>""")

        if dispatcher["format"]=="html":
            
            xsl.append("""<xsl:output method="html"/>""")
            xsl.append("""<xsl:output omit-xml-declaration="yes"/>""") 
            xsl.append("""<xsl:output encoding="UTF-8" />""")
            xsl.append("""<xsl:output indent="yes"/>""")



        if dispatcher["format"]=="txt":
            
            xsl.append("""<xsl:output method="txt"/>""")
            xsl.append("""<xsl:output omit-xml-declaration="yes"/>""") 
            xsl.append("""<xsl:output encoding="UTF-8" />""")
            xsl.append("""<xsl:output indent="yes"/>""")

            # see XSL disable-output-escaping to process escaped XML

        if dispatcher["format"]=="xhtml" or dispatcher["format"]=="html" or dispatcher["format"]=="robot" :
            import xsldata_xhtml
            xsl_base=getattr(xsldata_xhtml,"xsl_%s%s_%s" % (dispatcher["type"],dispatcher["colorent"],dispatcher["action"]),xsldata_xhtml.dummy)(dispatcher,environ)

            xsl.append(xsl_base)
    

        if dispatcher["format"]=="txt":

            xsl.append("""


<xsl:template match="/">
   This is a dummy XSL
   <xsl:apply-templates/>
</xsl:template>

<xsl:template match="*">
  <xsl:value-of select="name(.)"/>: <xsl:apply-templates/><xsl:text>&#10;</xsl:text>

</xsl:template>

<xsl:template match="text()">
<xsl:value-of select="."/>

</xsl:template>


<xsl:template match="comment()"> COMMENT: <xsl:copy/> </xsl:template> 

""")

        if dispatcher["format"]=="json":
            # http://ajaxian.com/archives/json-vs-xml-the-debate

            # XML is built for giving semantic meaning two text within documents. JSON is built for data structures.
            # On the other hand providing semantic meaning to the text within documents is what XML excels at, HTML being the prime example. JSON actually does not fit this bill at all. Doing something like:
            # some <b>important</b> word
            # should not attempted to be done by JSON.
            # xsl.append("""<?xml version="1.0" encoding="UTF-8"?>""")
            # xsl.append("""<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">""")
            xsl.append("""<xsl:output indent="no" omit-xml-declaration="yes" method="txt" encoding="UTF-8" />""")
        # media-type="text/x-json"/>
            xsl.append("""<xsl:strip-space elements="*"/>""")



            xsl.append("""


<xsl:template match="/">
   <xsl:text>{</xsl:text>
   <xsl:apply-templates/>
   <xsl:text>}</xsl:text>
</xsl:template>

<xsl:template match="answer">"aswer":"no answer"}</xsl:template>

<xsl:template match="*">

   <xsl:if test="name() != name(preceding-sibling::*) and name() = name(following-sibling::*)">[&#10;</xsl:if>


   <xsl:if test="not(preceding-sibling::*)">{&#10;</xsl:if>
   <xsl:text>"</xsl:text>
   <xsl:value-of select="name(.)"/>   
   <xsl:text>"</xsl:text>
   <xsl:text>:</xsl:text>
   <xsl:if test="count(child::node())=0"><xsl:text>null</xsl:text></xsl:if>
   <xsl:apply-templates/>
   <xsl:if test="following-sibling::*">,</xsl:if>
   <xsl:if test="not(following-sibling::*)">}</xsl:if>
   <xsl:text>&#10;</xsl:text>
   <xsl:if test="name() = name(preceding-sibling::*) and name() != name(following-sibling::*)">]&#10;</xsl:if>

</xsl:template>

<!-- ignore document text -->
<xsl:template match="text()[preceding-sibling::node() or following-sibling::node()]"/>


<xsl:template match="text()">
   <xsl:text>"</xsl:text>
   <!-- <xsl:value-of disable-output-escaping="yes" select="translate(.,'&#x9;&#xA;&#xD;','   ')"/>--><!-- &#x9;= tab &#xA;=line feed &#xD;=Carriage return-->
   <!--<xsl:value-of select="."/>-->
   <!--<xsl:text>AAAAAA</xsl:text>-->
   <xsl:call-template name="break"/>

   <xsl:text>"</xsl:text>

</xsl:template>

<!-- escape double quotes http://www.dpawson.co.uk/xsl/sect2/replace.html -->
<!--<xsl:template match="text()"><xsl:call-template name="break"></xsl:template>-->

<xsl:template name="break">
   <!--<xsl:param name="text" select="."/>-->
   <xsl:param name="text"><xsl:value-of disable-output-escaping="yes" select="translate(.,'&#x9;&#xA;&#xD;','   ')"/></xsl:param>
   <xsl:choose>
   <xsl:when test="contains($text, '&quot;')">
      <xsl:value-of select="substring-before($text, '&quot;')"/>
      <xsl:text>\&quot;</xsl:text>
      <xsl:call-template name="break">
          <xsl:with-param name="text" select="substring-after($text,
'&quot;')"/>
      </xsl:call-template>
   </xsl:when>
   <xsl:otherwise>
	<xsl:value-of select="$text"/>
   </xsl:otherwise>
   </xsl:choose>
</xsl:template>



<!-- ignore comments -->
<xsl:template match="comment()"></xsl:template> 

""")








# ==================================================






            # http://www.bramstein.com/projects/xsltjson/xml-2-json.xsl

            NOxsl.append("""
   <!-- ignore document text -->
  <xsl:template match="text()[preceding-sibling::node() or following-sibling::node()]"/>
""")
            NOxsl.append("""
       
	<xsl:template match="*">
		<xsl:param name="recursionCnt">0</xsl:param>
		<xsl:param name="isLast">1</xsl:param>
		<xsl:param name="inArray">0</xsl:param>
		<xsl:if test="$recursionCnt=0">
			<xsl:text>{&#10;</xsl:text>
		</xsl:if>
		<!-- test what type of data to output  -->
		<xsl:variable name="elementDataType">
			<xsl:value-of select="number(text())"/>
		</xsl:variable>
		<xsl:variable name="elementData">
			<!-- TEXT ( use quotes ) -->
			<xsl:if test="string($elementDataType) ='NaN'">
				<xsl:if test="boolean(text())">
				<xsl:text/>"<xsl:value-of select="text()"/>"<xsl:text/>
				</xsl:if>
			</xsl:if>
			<!-- NUMBER (no quotes ) -->
			<xsl:if test="string($elementDataType) !='NaN'">
				<xsl:text/><xsl:value-of select="text()"/><xsl:text/>
			</xsl:if>
			<!-- NULL -->
			<xsl:if test="not(*)">
				<xsl:if test="not(text())">
					<xsl:text/>null<xsl:text/>
				</xsl:if>
			</xsl:if>


		</xsl:variable>
		<xsl:variable name="hasRepeatElements">
			<xsl:for-each select="*">
				<xsl:if test="name() = name(preceding-sibling::*) or name() = name(following-sibling::*)">
					<xsl:text/>true<xsl:text/>
				</xsl:if>
			</xsl:for-each>
		</xsl:variable>
		<xsl:if test="not(count(@*) &gt; 0)">
		 <xsl:text/>"<xsl:value-of select="local-name()"/>":<xsl:value-of select="$elementData"/><xsl:text/>
		</xsl:if>
		<xsl:if test="count(@*) &gt; 0">
		<xsl:text/>"<xsl:value-of select="local-name()"/>":{&#10;"content":<xsl:value-of select="$elementData"/><xsl:text/>
			<xsl:for-each select="@*">
				<xsl:if test="position()=1">,</xsl:if>
				<!-- test what type of data to output  -->
				<xsl:variable name="dataType">
					<xsl:text/><xsl:value-of select="number(.)"/><xsl:text/>
				</xsl:variable>
				<xsl:variable name="data">
					<!-- TEXT ( use quotes ) -->
					<xsl:if test="string($dataType) ='NaN'">
				<xsl:text/>"<xsl:value-of select="current()"/>"<xsl:text/> </xsl:if>
					<!-- NUMBER (no quotes ) -->
					<xsl:if test="string($dataType) !='NaN'">
						<xsl:text/><xsl:value-of select="current()"/><xsl:text/>
					</xsl:if>
				</xsl:variable>
				<xsl:text/><xsl:value-of select="local-name()"/>:<xsl:value-of select="$data"/><xsl:text/>
				<xsl:if test="position() !=last()">,</xsl:if>
			</xsl:for-each>
		<xsl:text/>}<xsl:text/>
		</xsl:if>
		<xsl:if test="not($hasRepeatElements = '')">
					<xsl:text/>[{&#10;<xsl:text/>
				</xsl:if>
		<xsl:for-each select="*">
			<xsl:if test="position()=1">
				<xsl:if test="$hasRepeatElements = ''">
					<xsl:text>{&#10;</xsl:text>
				</xsl:if>
			</xsl:if>
			<xsl:apply-templates select="current()">
				<xsl:with-param name="recursionCnt" select="$recursionCnt+1"/>
				<xsl:with-param name="isLast" select="position()=last()"/>
				<xsl:with-param name="inArray" select="not($hasRepeatElements = '')"/>
			</xsl:apply-templates>
			<xsl:if test="position()=last()">
				<xsl:if test="$hasRepeatElements = ''">
					<xsl:text>}</xsl:text>
				</xsl:if>
			</xsl:if>
		</xsl:for-each>
		<xsl:if test="not($hasRepeatElements = '')">
					<xsl:text/>}]<xsl:text/>
				</xsl:if>
		<xsl:if test="not( $isLast )">
			<xsl:if test="$inArray = 'true'">
				<xsl:text>}</xsl:text>
			</xsl:if>
			<xsl:text/>,<xsl:text/>
			<xsl:if test="$inArray = 'true'">
				<xsl:text>{&#10;</xsl:text>
			</xsl:if>
		</xsl:if>
		<xsl:if test="$recursionCnt=0">}</xsl:if>
	</xsl:template>
""")







# ==================================================


# http://code.google.com/p/xml2json-xslt/

            NOxsl.append("""<!--constant-->
  <xsl:variable name="d">0123456789</xsl:variable>

  <!-- ignore document text -->
  <xsl:template match="text()[preceding-sibling::node() or following-sibling::node()]"/>

  <!-- string -->
  <xsl:template match="text()">
    <xsl:call-template name="escape-string">
      <xsl:with-param name="s" select="."/>
    </xsl:call-template>
  </xsl:template>""")
            
            NOxsl.append("""
<!-- Main template for escaping strings; used by above template and for object-properties 
       Responsibilities: placed quotes around string, and chain up to next filter, escape-bs-string -->
  <xsl:template name="escape-string">
    <xsl:param name="s"/>
    <xsl:text>"</xsl:text>
    <xsl:call-template name="escape-bs-string">
      <xsl:with-param name="s" select="$s"/>
    </xsl:call-template>
    <xsl:text>"</xsl:text>
  </xsl:template>""")
  
            NOxsl.append("""
<!-- Escape the backslash (\) before everything else. -->
  <xsl:template name="escape-bs-string">
    <xsl:param name="s"/>
    <xsl:choose>
      <xsl:when test="contains($s,'\')">
        <xsl:call-template name="escape-quot-string">
          <xsl:with-param name="s" select="concat(substring-before($s,'\'),'\\')"/>
        </xsl:call-template>
        <xsl:call-template name="escape-bs-string">
          <xsl:with-param name="s" select="substring-after($s,'\')"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="escape-quot-string">
          <xsl:with-param name="s" select="$s"/>
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>""")
  
            NOxsl.append("""  
<!-- Escape the double quote ("). -->
  <xsl:template name="escape-quot-string">
    <xsl:param name="s"/>
    <xsl:choose>
      <xsl:when test="contains($s,'&quot;')">
        <xsl:call-template name="encode-string">
          <xsl:with-param name="s" select="concat(substring-before($s,'&quot;'),'\&quot;')"/>
        </xsl:call-template>
        <xsl:call-template name="escape-quot-string">
          <xsl:with-param name="s" select="substring-after($s,'&quot;')"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="encode-string">
          <xsl:with-param name="s" select="$s"/>
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>""")
  
            NOxsl.append("""  
<!-- Replace tab, line feed and/or carriage return by its matching escape code. Can't escape backslash
       or double quote here, because they don't replace characters (&#x0; becomes \t), but they prefix 
       characters (\ becomes \\). Besides, backslash should be seperate anyway, because it should be 
       processed first. This function can't do that. -->
  <xsl:template name="encode-string">
    <xsl:param name="s"/>
    <xsl:choose>
      <!-- tab -->
      <xsl:when test="contains($s,'&#x9;')">
        <xsl:call-template name="encode-string">
          <xsl:with-param name="s" select="concat(substring-before($s,'&#x9;'),'\t',substring-after($s,'&#x9;'))"/>
        </xsl:call-template>
      </xsl:when>
      <!-- line feed -->
      <xsl:when test="contains($s,'&#xA;')">
        <xsl:call-template name="encode-string">
          <xsl:with-param name="s" select="concat(substring-before($s,'&#xA;'),'\n',substring-after($s,'&#xA;'))"/>
        </xsl:call-template>
      </xsl:when>
      <!-- carriage return -->
      <xsl:when test="contains($s,'&#xD;')">
        <xsl:call-template name="encode-string">
          <xsl:with-param name="s" select="concat(substring-before($s,'&#xD;'),'\r',substring-after($s,'&#xD;'))"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise><xsl:value-of select="$s"/></xsl:otherwise>
    </xsl:choose>
  </xsl:template>""")

            NOxsl.append("""  
<!-- number (no support for javascript mantise) -->
  <xsl:template match="text()[not(string(number())='NaN')]">
    <xsl:value-of select="."/>
  </xsl:template>""")

            NOxsl.append("""  
<!-- boolean, case-insensitive -->
  <xsl:template match="text()[translate(.,'TRUE','true')='true']">true</xsl:template>
  <xsl:template match="text()[translate(.,'FALSE','false')='false']">false</xsl:template>
""")

            NOxsl.append("""  
<!-- item:null -->
  <xsl:template match="*[count(child::node())=0]">
    <xsl:call-template name="escape-string">
      <xsl:with-param name="s" select="local-name()"/>
    </xsl:call-template>
    <xsl:text>:null</xsl:text>
    <xsl:if test="following-sibling::*">,</xsl:if>
  </xsl:template>""")

            NOxsl.append("""  
<!-- object -->
  <xsl:template match="*" name="base">
    <xsl:if test="not(preceding-sibling::*)">{</xsl:if>
    <xsl:call-template name="escape-string">
      <xsl:with-param name="s" select="name()"/>
    </xsl:call-template>
    <xsl:text>:</xsl:text>
    <xsl:apply-templates select="child::node()"/>
    <xsl:if test="following-sibling::*">,</xsl:if>
    <xsl:if test="not(following-sibling::*)">}</xsl:if>
  </xsl:template>""")

            NOxsl.append("""  
<!-- array -->
  <xsl:template match="*[count(../*[name(../*)=name(.)])=count(../*) and count(../*)&gt;1]">
    <xsl:if test="not(preceding-sibling::*)">[</xsl:if>
    <xsl:choose>
      <xsl:when test="not(child::node())">
        <xsl:text>null</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:apply-templates select="child::node()"/>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:if test="following-sibling::*">,</xsl:if>
    <xsl:if test="not(following-sibling::*)">]</xsl:if>
  </xsl:template>""")
  
            xsl.append("""  
<!-- convert root element to an anonymous container -->
  <xsl:template match="/">
    <xsl:apply-templates select="node()"/>
  </xsl:template>""")
    
            # xsl.append("""</xsl:stylesheet>""")




        xsl.append("</xsl:stylesheet>")

    return "".join(xsl)






def xsl_dummy(dispatcher,environ):
    xsl=[]
    
    # xsl.append("NO XSL defined for type %s, format %s" % (dispatcher["type"],dispatcher["format"]))
    xsl.append("""


<xsl:template match="/">
   <PAGE>
   <xsl:comment> This is a dummy XSL </xsl:comment>
   <xsl:apply-templates/>
   </PAGE>
</xsl:template>

<xsl:template match="*">
   ELEMENT: <xsl:value-of select="name(.)"/>:
   <xsl:apply-templates/>
</xsl:template>

<xsl:template match="text()">
TEXT: <xsl:value-of select="."/>
</xsl:template>


<xsl:template match="comment()"> COMMENT: <xsl:copy/> </xsl:template> 

""")
    
    return "".join(xsl)


def xsl_faq_get(dispatcher,environ):
    # return xsl_dummy(dispatcher,environ)
    filename="/home/madon/public_html/perso/entreprise/sql_current/site/atpic/python/atpic/faq.xsl"
    infile = open(filename,"r")
    xsl=infile.read()
    infile.close()
    return xsl

