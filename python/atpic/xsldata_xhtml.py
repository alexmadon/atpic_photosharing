"""

XSL common to XHTML, HTML and robots



"""

def dummy(dispatcher,environ):
    
    xsl="""
<xsl:template match="/">
<html>
<head><title>some title</title></head>
<body>
<img src="http://atpic.com/art/atpic_square1.png"/>
<xsl:comment> This is a dummy XSL </xsl:comment>
<xsl:apply-templates/>
</body>
</html>
</xsl:template>

<xsl:template match="*">
   ELEMENT: <xsl:value-of select="name(.)"/>:
   <xsl:apply-templates/>
</xsl:template>

<xsl:template match="text()">
TEXT: <xsl:value-of select="."/><br/>
</xsl:template>


<xsl:template match="comment()"> COMMENT: <xsl:copy/> </xsl:template> 

"""

    return xsl





def xsl_pic_entry_get(dispatcher,environ):
    xsl=[]
    NOxsl=[]

    xsl.append("""

<xsl:template match="/">
<html>
<head>
<title>Test</title>
</head>
<body>
Hiiii

ID2: <xsl:value-of select="/page/pic/id"/>


<img>
<xsl:attribute name="src">
<xsl:value-of select="/page/pic/picurl"/>
</xsl:attribute>
<xsl:attribute name="alt">Picture <xsl:value-of select="/page/pic/id"/></xsl:attribute>
</img>

</body>
</html>
</xsl:template>




""")
    NOxsl.append("""

<xsl:template match="atpic:thepic" xml:lang="$setlang">
<html xml:lang="$setlang">
<head>
<title>Test</title>
</head>
<body>

Picture testalpha
<xsl:apply-templates select="atpic:picture"/>

</body>
</html>
</xsl:template>
""")


    NOxsl.append("""
<xsl:template match="atpic:picture">
<td class="picture" border="1">


<img>
<xsl:attribute name="src">
<xsl:value-of select="atpic:picdetails/atpic:thumb_url"/>
</xsl:attribute>
<xsl:attribute name="alt">Picture <xsl:value-of select="atpic:picdetails/atpic:id"/></xsl:attribute>
</img>
<xsl:value-of select="atpic:picdetails/atpic:id"/>


</td>
</xsl:template>
""")

    return "".join(xsl)


def xsl_gallery_entry_get(dispatcher,environ):


    xsl=[]
    xsl.append("""

<xsl:template match="atpic:thegallery" xml:lang="$setlang">
<html xml:lang="$setlang">


<head>
<title>
<xsl:text>Atpic XSL: </xsl:text>
<xsl:apply-templates select="atpic:gallery/atpic:gallerytitle"/>
</title>""")


    # build: <link rel="stylesheet" type="text/css" href="http://atpic.foo/css/default_color.css"  />
    xsl.append("""

<xsl:element name="link">
<xsl:attribute name="rel">
<xsl:text>stylesheet</xsl:text>
</xsl:attribute>
<xsl:attribute name="type">
<xsl:text>text/css</xsl:text>
</xsl:attribute>
<xsl:attribute name="href">
<xsl:text>test.css</xsl:text>
</xsl:attribute>
</xsl:element>

""")






    # build:<link rel="alternate" type="application/rss+xml" title="Atpic RSS gallery19" href="http://atpic.foo/rss.php?gid=19&amp;secret=0" />
    
    xsl.append("""

<xsl:element name="link">
<xsl:attribute name="rel">
<xsl:text>alternate</xsl:text>
</xsl:attribute>
<xsl:attribute name="type">
<xsl:text>application/rss+xml</xsl:text>
</xsl:attribute>
<xsl:attribute name="title">
<xsl:text>Atpic RSS gallery</xsl:text>
</xsl:attribute>
<xsl:attribute name="href">
<xsl:apply-templates select="atpic:rssfeed"/>
</xsl:attribute>
</xsl:element>

""")










    xsl.append("""
</head>

<xsl:comment>End of head</xsl:comment>



<body>
<div class="gallery">
<xsl:apply-templates select="atpic:artist"/>
<xsl:apply-templates select="atpic:gallery"/>
<xsl:apply-templates select="atpic:pictures"/>
<xsl:apply-templates select="atpic:preload"/>
<xsl:apply-templates select="atpic:pm"/>
<xsl:apply-templates select="atpic:comments"/>
<xsl:apply-templates select="atpic:votes"/>
<xsl:apply-templates select="atpic:tags"/>
<xsl:apply-templates select="atpic:counter"/>

</div>
</body>
</html>


</xsl:template>




""")












    # artist
    xsl.append("""
<xsl:template match="atpic:artist">
<div class="artist">
<xsl:apply-templates select="atpic:artistname"/>
</div>
</xsl:template>
""")


    # pictures
    xsl.append("""


<xsl:template match="atpic:pictures">
<div class="pictures">
<table border="2">

<xsl:apply-templates/>


</table>
</div>
</xsl:template>
""")

    
    # picture
    
    #  xsl.append("""
    #  <xsl:template match="atpic:picture">
    #  <div class="picture">
    #  <xsl:value-of select="thumb_url"/>
    #  <br/>
    #  <xsl:apply-templates/>
    #  </div>
    #  </xsl:template>
    #  """)
    
    
    xsl.append("""

<xsl:template match="atpic:picture[(position()-1) mod ../atpic:mycol = 0]" >
    <tr>
      <xsl:call-template name="pict"/>

      <xsl:for-each select="following-sibling::atpic:picture[position() &lt; ../atpic:mycol ]">
        <xsl:call-template name="pict"/>

      </xsl:for-each>
    </tr>
</xsl:template>


""")

    # picture called from table
    xsl.append("""
<xsl:template name="pict">
<td class="picture" border="1">


<img>
<xsl:attribute name="src">
<xsl:value-of select="atpic:picdetails/atpic:thumb_url"/>
</xsl:attribute>
<xsl:attribute name="alt">Picture <xsl:value-of select="atpic:picdetails/atpic:id"/></xsl:attribute>
</img>
<xsl:value-of select="atpic:picdetails/atpic:id"/>


</td>
</xsl:template>
""")


    xsl.append("""
<xsl:template match="atpic:raw">
</xsl:template>
""")

    xsl.append("""
<xsl:template match="atpic:picdetails">
</xsl:template>
""")

    xsl.append("""
<xsl:template match="atpic:resolution_links">
</xsl:template>
""")


    # ==================================
    #  non picture elements
    # ==================================
    
    # pm
    xsl.append("""
<xsl:template match="atpic:pm">
<div class="pm">
<xsl:apply-templates/>
</div>
</xsl:template>
""")
        
    # comments
    xsl.append("""
<xsl:template match="atpic:comments">
<div class="comments">
<xsl:apply-templates/>
</div>
</xsl:template>
""")

    # votes
    xsl.append("""
<xsl:template match="atpic:votes">
<div class="votes">
<xsl:apply-templates/>
</div>
</xsl:template>
""")


    # tags
    xsl.append("""
<xsl:template match="atpic:tags">
<div class="tags">
<xsl:apply-templates/>
</div>
</xsl:template>
""")

    # tag
    xsl.append("""
<xsl:template match="atpic:tag">
<div class="tag">

<xsl:element name="a">
<xsl:attribute name="href">
<xsl:value-of select="atpic:url"/>
</xsl:attribute>
<xsl:attribute name="style">
<xsl:text>font-size:</xsl:text>
<xsl:value-of select="atpic:weight"/>
<xsl:text>em;</xsl:text>
</xsl:attribute>
<xsl:value-of select="atpic:thetag"/>
</xsl:element>

<xsl:apply-templates/>
</div>
</xsl:template>
""")

    # no ouput for:
    xsl.append("""
<xsl:template match="atpic:tag/atpic:weight">
</xsl:template>
""")
    # no ouput for:
    xsl.append("""
<xsl:template match="atpic:tag/atpic:thetag">
</xsl:template>
""")

    # url
    xsl.append("""
<xsl:template match="atpic:url">
<xsl:text> </xsl:text>
<xsl:element name="a">
<xsl:attribute name="href">
<xsl:value-of select="."/>
</xsl:attribute>
<xsl:value-of select="../atpic:info"/>
</xsl:element>
</xsl:template>
""")

    # info display: no display
    xsl.append("""
<xsl:template match="atpic:info">
</xsl:template>

""")


    # text display
    xsl.append("""
<!-- change default to not display text -->
<xsl:template match="text()">
<xsl:value-of select="."/>
</xsl:template>

""")

    # javascript
    xsl.append("""
<xsl:template match="atpic:script">

<xsl:element name="script">
<xsl:attribute name="type">
<xsl:value-of select="@type"/>
</xsl:attribute>

<xsl:apply-templates/>
</xsl:element>
</xsl:template>
""")

    return "".join(xsl)


