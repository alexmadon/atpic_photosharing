#!/usr/bin/python3
"""
A library of XSL styles

One BIG style for the frontal XML (i.e the non solr):
this is because we allow composite.
Style is chosen based on the HTTP method+URL; everything needs to be encoded in the XML 

/response/request
/response/authentication
/response/authorization
/response/get/get/USER

you could put '/' but not necessary as always after get/get or similar

composite:
/response/request (global composite request)
/response/authentication
/response/Component/component/request (individual request)
/response/Component/component/authentication
/response/Component/component/get/get/HOME/USER (same page USER but add an optionnal marker HOME)

multiput
"""

# i18n:
# http://docstore.mik.ua/orelly/xml/jxslt/ch08_06.htm
# import logging
import atpic.log
import atpic.parameters
import atpic.i18n

xx=atpic.log.setmod("INFO","xsllib")

def parse(*args):
    return atpic.i18n.parse(*args)

def declare(format):
    yy=atpic.log.setname(xx,'declare')
    xsl=[]
    atpic.log.debug(yy,"fformat",format)
    xsl.append(b'<?xml version="1.0"?>')
    xsl.append(b'<xsl:stylesheet version="1.0" ')
    xsl.append(b'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" ')
    xsl.append(b'xmlns:date="http://exslt.org/dates-and-times" ')
    # not used:

    if format==b"xhtml":
        xsl.append(b'xmlns="http://www.w3.org/1999/xhtml" ')
    # xsl.append(b'exclude-result-prefixes="" ')
    xsl.append(b'>')
    xsl.append(b'<xsl:output ')
    xsl.append(b'method="xml" ')
    xsl.append(b'omit-xml-declaration="yes" ')
    xsl.append(b'encoding="UTF-8" ')
    xsl.append(b'indent="yes"/>')

    return b"".join(xsl)
# arabic and hebrew need a: <html  dir="rtl" lang="he">


def protect_with_captcha(dotcom):
    """
    
    """
    out=b"""
<div class="captchapublic">
<xsl:comment>captchapublic: <xsl:value-of select="captchapublic" /></xsl:comment>
<img src="http://atpic"""+dotcom+b"""/captcha/{captchapublic}" alt="captcha"/>
<input name="captchapublic" value="{captchapublic}" type="hidden"/>
</div>
<div class="captchahidden">
enter the number above (captcha) <input name="captchahidden" value="{captchahidden}"/>
</div>"""
    
    return out

def xml2xhtml(format,environ):
    """
    One big style as we allow composite and we do not know in advance what the XML will have as components.
    """
    dotcom=atpic.parameters.get_tld(environ) # get dotcom
    xsl=[]
    xslBAD=[]
    lang=b'en'
    xsl.append(declare(format))

    xsl.append(b"""
<!-- xml2xhtml -->
<xsl:template match="/">
<xsl:apply-templates/>
</xsl:template>

<xsl:template match="/response/Component/component/error">
<xsl:apply-templates/>
</xsl:template>

<xsl:template match="/response/Component/component/error/code">
<h1>Error <xsl:value-of select="."/></h1>
</xsl:template>

<xsl:template match="/response/Component/component/error/dataerror">
<div class="dataerror">
<xsl:apply-templates mode="dataerror"/>
</div>
</xsl:template>


<xsl:template match="message" mode="dataerror">
<div class="message">
<xsl:apply-templates/>
</div>
</xsl:template>


<xsl:template match="wikierror">
<div class="wikierror">
This wiki page does not exist.
To create it go to: <a href="{/response/request/pathinfo}/_post"><xsl:value-of select="/response/request/pathinfo"/><xsl:text>/_post</xsl:text></a>
</div>
</xsl:template>


<xsl:template match="/response">
<!-- 
lang should be passed by XML
http://www.sagehill.net/docbookxsl/Localizations.html
-->
""")

    # html4=b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">'
    # xhtml11=b'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/tr/xhtml11/DTD/xhtml11.dtd">';
    # http://stackoverflow.com/questions/3387127/set-html5-doctype-with-xslt
    xsl.append(b"""<xsl:text disable-output-escaping='yes'>&lt;!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"></xsl:text>""")

    xsl.append(b"""
<html dir="{capabilities/dir}" lang="{capabilities/lang}"><!-- for hebrew and arabic dir is 'rtl' else 'ltr' -->
<head>
<title>
<xsl:apply-templates mode="title" select="Component/component/get/get"/>
</title>
<xsl:apply-templates mode="javascript" select="Component/component/get/get"/>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.3/jquery.min.js"></script>
<script type="text/javascript" src="http://atpic"""+dotcom+b"""/static/javascript/jquery.justifiedGallery.min.js"/>

<link rel="stylesheet" type="text/css" href="http://atpic"""+dotcom+b"""/static/css/global.css"/>
<link rel="stylesheet" type="text/css" href="http://atpic"""+dotcom+b"""/static/css/pygments-long.css"/>
<link rel="stylesheet" type="text/css" href="http://atpic"""+dotcom+b"""/static/css/justifiedGallery.min.css"/>
<link href="https://fonts.googleapis.com/css?family=Raleway:400,900" rel="stylesheet" type="text/css"/>
<link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css" rel="stylesheet" integrity="sha384-T8Gy5hrqNKT+hzMclPo118YTQO6cYprQmhrYwIiQ/3axmI1hQomh7Ud2hPOy8SP1" crossorigin="anonymous"/>

<xsl:apply-templates mode="css" select="Component/component/get/get"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>
<body>""")

# http://www.dwuser.com/education/content/creating-responsive-tiled-layout-with-pure-css/

    messageoftheday=b"""
<div class="messageofday">
<b>Welcome to Atpic V2 BETA</b>
<br/>
<a href="http://atpic"""+dotcom+b"""/wiki">[Documentation]</a> is being published, but if you need some help, email us at:
<br/>
atpicversion2 AT gmail DOT com
</div>
"""



    xsl.append(b"""


<div class="logo">atpic</div>

<div class="searchzone">
<form class="search">
<input class="searchTerm" placeholder="Enter your search term ..." /><input class="searchButton" type="submit" value=""/>
</form>
</div>

<div class="authenticationtop">
<xsl:call-template name="displayauthentication"/>
</div>
""")

    # xsl.append(messageoftheday)

    xsl.append(b"""
<xsl:apply-templates select="Component"/>

<div class="authenticationbottom">
<xsl:call-template name="displayauthentication"/>
</div>

</body>
</html>
</xsl:template>






<xsl:template name="displayauthentication">
<xsl:comment>displayauthentication</xsl:comment>
<xsl:apply-templates select="authentication"/>

<xsl:if test="not(authentication) and (request/pathinfo != '/login')">
<div class="authentication">
<xsl:choose>
<xsl:when test="request/pathinfo = '/'">
<a href="http://atpic"""+dotcom+b"""/login">login here</a>
</xsl:when>
<xsl:otherwise>
<a href="http://atpic"""+dotcom+b"""/login?redirect={request/url}">login here</a>
</xsl:otherwise>
</xsl:choose>
</div>
</xsl:if>
</xsl:template>


<!-- mode javascript: adds js to some pages -->

<xsl:template match="/response/Component/component/get/get" mode="javascript">
<xsl:apply-templates mode="javascript" select="Wiki"/>
</xsl:template>


<xsl:template match="Wiki" mode="javascript">
<script type="text/javascript" src="http://atpic"""+dotcom+b"""/static/javascript/diff_radio.js"/>
</xsl:template>






<!-- mode css: adds css to some pages -->

<xsl:template match="/response/Component/component/get/get" mode="css">
<xsl:apply-templates mode="css" select="wiki|USER/wiki"/>
</xsl:template>


<xsl:template match="USER/wiki" mode="css">
<xsl:if test="not(ancestor::component/authorization/useris/owner)">
<link rel="stylesheet" type="text/css" href="http://atpic"""+dotcom+b"""/static/css/hide_edit.css"/>
</xsl:if>
</xsl:template>



<xsl:template match="wiki" mode="css">
<xsl:if test="not(ancestor::component/authorization/useris/admin)">
<link rel="stylesheet" type="text/css" href="http://atpic"""+dotcom+b"""/static/css/hide_edit.css"/>
</xsl:if>
</xsl:template>






<!-- composite title -->
<xsl:template match="/response/Component/component/get/get" mode="title">
<xsl:apply-templates mode="title" select="HOME/SEARCH"/>
<xsl:apply-templates mode="title" select="HOME/USER/SEARCH"/>
<xsl:apply-templates mode="title" select="wiki|USER/wiki|Wiki|USER/Wiki"/>
</xsl:template>

<xsl:template match="HOME/SEARCH" mode="title">
<xsl:text>Atpic Home Page</xsl:text>
</xsl:template>

<xsl:template match="HOME/USER/SEARCH" mode="title">
<xsl:text>Atpic Home Page for </xsl:text>
<xsl:value-of select="../name"/>
</xsl:template>

<xsl:template match="wiki" mode="title">
<xsl:text>Atpic Wiki Page </xsl:text>
<xsl:apply-templates  select="wikihtml/div/h1"/>
</xsl:template>

<xsl:template match="Wiki" mode="title">
<xsl:text>Atpic Wiki Diff Page</xsl:text>
</xsl:template>

<!-- non composite titles -->
<xsl:template match="/response/get/get" mode="title">
</xsl:template>






""")

    # this is controlled by atpic.parameters.get_readonly()
    xsl.append(b"""<xsl:template match="readonly">
<div style="color:red;">
<b>System is in read-only mode: We are upgrading Atpic.</b>
<br/>
Documentation is coming soon, but if you need some help, email us at:
<br/>
atpicversion2 AT gmail DOT com
</div>
</xsl:template>""")
    

    xsl.append(b"""

<!-- ignore the following -->

<xsl:template match="capabilities">
</xsl:template>

<xsl:template match="request">
</xsl:template>

<xsl:template match="authorization">
</xsl:template>

<xsl:template match="route">
</xsl:template>

<xsl:template match="query">
</xsl:template>

<xsl:template match="presentation">
</xsl:template>

<xsl:template match="size">
</xsl:template>

<xsl:template match="hits">
</xsl:template>

 
<xsl:template match="/response/authentication">
<xsl:comment>matching /response/authentication</xsl:comment>
<div class="authentication">
<xsl:comment>for desktop</xsl:comment>
<div class="authenticatedas">"""+parse(lang,b'authenticatedas',b"""<a href="http://{short}.atpic"""+dotcom+b"""\">""")+b"""<xsl:value-of select="displayname"/></a></div>
<xsl:comment>for mobile</xsl:comment>
<div class="myhome"><a href="http://{short}.atpic"""+dotcom+b"""\">my home</a></div>
<div class="logout"><a href="http://atpic"""+dotcom+b"""/logout?redirect={/response/request/url}">logout</a></div>
</div>
</xsl:template>




<xsl:template match="component/get/get">
<xsl:apply-templates/>
</xsl:template>


<xsl:template match="component/get/post|component/get/put">
<xsl:apply-templates mode="rw"/>
</xsl:template>

<xsl:template match="component/get/delete">
<xsl:apply-templates mode="delete"/>
</xsl:template>

<xsl:template match="component/post/post|component/post/put|component/put/put">
<xsl:if test="not(../../error)">
<xsl:apply-templates/>
</xsl:if>
<xsl:if test="(../../error)">
<xsl:apply-templates mode="rw"/>
</xsl:if>
</xsl:template>

<xsl:template match="Wiki">
<div class="Wiki">
<xsl:comment>Wiki1</xsl:comment>
<xsl:call-template name="previousapi"/>
<xsl:call-template name="nextapi"/>
<form onsubmit="return false;">
<xsl:apply-templates/>
<input type="submit" onclick="window.location.href=get_diffurl();"/>
</form>
<xsl:call-template name="previousapi"/>
<xsl:call-template name="nextapi"/>
</div>
</xsl:template>

<xsl:template match="Wiki/wiki">
<div class="wiki">
<xsl:comment>wiki2</xsl:comment>

<xsl:element name="input">
<xsl:attribute name="type">radio</xsl:attribute>
<xsl:attribute name="name">group1</xsl:attribute>
<xsl:attribute name="value"><xsl:value-of select="id"/></xsl:attribute>
<xsl:if test="(position() = 2) "><xsl:attribute name="checked"></xsl:attribute></xsl:if>
</xsl:element>

<xsl:element name="input">
<xsl:attribute name="type">radio</xsl:attribute>
<xsl:attribute name="name">group2</xsl:attribute>
<xsl:attribute name="value"><xsl:value-of select="id"/></xsl:attribute>
<xsl:if test="(position() = 1) "><xsl:attribute name="checked"></xsl:attribute></xsl:if>
</xsl:element>


<a href="http://{/response/request/host}{ancestor::component/request/pathinfo}/{id}"><xsl:value-of select="id"/></a>
<xsl:apply-templates select="datepublished"/>
<xsl:apply-templates select="message"/>
</div>
</xsl:template>



<xsl:template match="USER/wiki">
<div class="wiki">
<a href="/wiki{ancestor::component/route/pxplo/wiki}/_revision">history</a>
<xsl:text> </xsl:text>
<xsl:if test="ancestor::component/authorization/useris/owner">
<a href="/wiki{ancestor::component/route/pxplo/wiki}/_post" class="editwiki">edit</a>
</xsl:if>
<xsl:apply-templates select="wikihtml"/>
</div>
</xsl:template>


<xsl:template match="wiki">
<div class="wiki">

   <xsl:call-template name="split">
    <xsl:with-param name="pText" select="ancestor::component/route/pxplo/wiki"/>
    <xsl:with-param name="path" select="ancestor::component/route/pxplo/wiki"/>
   </xsl:call-template>

<br/>
<a href="/wiki{ancestor::component/route/pxplo/wiki}/_revision">history</a>
<xsl:text> </xsl:text>
<xsl:if test="ancestor::component/authorization/useris/admin">
<a href="/wiki{ancestor::component/route/pxplo/wiki}/_post" class="editwiki">edit</a>
</xsl:if>
<xsl:apply-templates select="wikihtml"/>
</div>
</xsl:template>


<xsl:template match="wiki/wikitext">
thetext:<pre><xsl:apply-templates/></pre>
</xsl:template>

<xsl:template match="wiki/wikihtml">
<xsl:apply-templates mode="identity" /> <!-- preserve HTML tags -->
</xsl:template>



<xsl:template match="wikidiff">
wikidiff11<xsl:apply-templates select="wikitextdiff"/>
</xsl:template>


<xsl:template match="wikitext1">
Old:<pre><xsl:apply-templates mode="identity"/></pre>
</xsl:template>


<xsl:template match="wikitext2">
New:<pre><xsl:apply-templates mode="identity"/></pre>
</xsl:template>



<xsl:template match="wikitextdiff">
diff22<pre><xsl:apply-templates /></pre>
</xsl:template>

<xsl:template match="wikitextdiff/insert">
<ins style="background:#e6ffe6;"><xsl:apply-templates  mode="identity"/></ins>
</xsl:template>

<xsl:template match="wikitextdiff/delete">
<del style="background:#ffe6e6;"><xsl:apply-templates  mode="identity"/></del>
</xsl:template>

<xsl:template match="wikitextdiff/equal">
<span><xsl:apply-templates  mode="identity"/></span>
</xsl:template>




<xsl:template match="User">
<div class="User">
<xsl:call-template name="previousapi"/>
<xsl:call-template name="nextapi"/>
<xsl:apply-templates/>
<xsl:call-template name="previousapi"/>
<xsl:call-template name="nextapi"/>
</div>
</xsl:template>

<xsl:template match="User/user">
<div class="user">
<a href="/user/{id}"><xsl:value-of select="id"/></a>
<xsl:text> </xsl:text>
<a href="http://{servershort}.atpic"""+dotcom+b""""><xsl:value-of select="servershort"/>.atpic"""+dotcom+b"""</a>
<xsl:text> </xsl:text>
<xsl:value-of select="name"/>
</div>
</xsl:template>



<xsl:template match="get/user">
<div class="user">
Userpage:
<xsl:value-of select="id"/>
<xsl:text> </xsl:text>
<a href="http://{servershort}.atpic"""+dotcom+b""""><xsl:value-of select="servershort"/>.atpic"""+dotcom+b"""</a> 
<xsl:value-of select="name"/>

<xsl:if test="ancestor::component/authorization/useris/owner">
<a href="/user/{id}/put">edit</a>
</xsl:if>


</div>
</xsl:template>

<xsl:template match="user/name">
<div class="name">
<a href="http://{servershort}.atpic"""+dotcom+b"""\"><xsl:value-of select="servershort"/></a>
</div>
</xsl:template>


<xsl:template match="user/login">
<div class="login">
<xsl:apply-templates/>
</div>
</xsl:template>



<xsl:template match="USER">
<div class="user">
<xsl:apply-templates select="GALLERY|Gallery|gallery"/>
<xsl:apply-templates select="PM|Pm|pm"/>
<xsl:apply-templates select="FRIEND|Friend|friend"/>
<xsl:apply-templates select="WIKI|Wiki|wiki|wikidiff"/>
<xsl:apply-templates select="TREESEARCH|TREENAV|TREE"/>
<xsl:apply-templates select="BLOGSEARCH|BLOGNAV|BLOG"/>
<xsl:apply-templates select="SEARCH"/>
</div>
</xsl:template>



<xsl:template match="USER/Pm">
<div class="Pm">
<a href="/pm/post">Add a new pm</a>
<xsl:apply-templates select="pm"/>
</div>
</xsl:template>

<xsl:template match="USER/Pm/pm">
<div class="pm">
<a href="/pm/{id}"><xsl:value-of select="id"/></a>
<xsl:value-of select="title"/>
<xsl:value-of select="text"/>
</div>
</xsl:template>

<xsl:template match="USER/pm">
<div class="pm">
A private message
<xsl:value-of select="title"/>
<xsl:value-of select="text"/>
</div>
</xsl:template>




<xsl:template match="USER/Gallery">
<div class="Gallery">
<xsl:call-template name="previousapi"/>
<xsl:call-template name="nextapi"/>
<a href="/gallery/post">Add a new gallery</a>
<xsl:apply-templates select="gallery"/>
<xsl:call-template name="previousapi"/>
<xsl:call-template name="nextapi"/>
</div>
</xsl:template>


<xsl:template match="USER/Gallery/gallery">
<div class="gallery">
<xsl:apply-templates select="id"/>
<xsl:apply-templates select="title"/>
<xsl:apply-templates select="text"/>
<xsl:apply-templates select="path"/>
<xsl:apply-templates select="pathstore_r160" mode="img1"/>
</div>
</xsl:template>

<xsl:template match="USER/Gallery/gallery/id">
<div class="id">
<a href="/gallery/{.}"><xsl:value-of select="."/></a>
</div>
</xsl:template>

<xsl:template match="USER/Gallery/gallery/title">
<div class="title">
<xsl:apply-templates/>
</div>
</xsl:template>

<xsl:template match="USER/Gallery/gallery/text">
<div class="text">
<xsl:apply-templates/>
</div>
</xsl:template>









<xsl:template match="USER/Friend">
<div class="Friend">
<a href="/friend/post">Add a new friend</a>
<xsl:apply-templates select="friend"/>
</div>
</xsl:template>


<xsl:template match="USER/Friend/friend">
<div class="friend">
<xsl:apply-templates select="id"/>
</div>
</xsl:template>

<xsl:template match="USER/friend">
<div class="friend">
friend<xsl:value-of select="id"/>
</div>
</xsl:template>






<xsl:template match="wiki" mode="rw">
<div class="wiki">
atpic wiki
<form action="" method="post">
<xsl:choose>
<xsl:when test="wikilines">
<input name="wikitext" value="{wikitext}" type="hidden"/>
wikilines
<textarea name="wikilines" cols="80" rows="20"><xsl:value-of select="wikilines"/></textarea>
</xsl:when>

<xsl:otherwise>
<div class="wikitext">
wikitext
<textarea name="wikitext" cols="80" rows="20"><xsl:value-of select="wikitext"/></textarea>
</div>
</xsl:otherwise>
</xsl:choose>


<br/>
message:
<input name="message" value="{message}"/>
<br/>
<input type="submit"/>
</form>
</div>

</xsl:template>




<xsl:template match="component/get/post/user" mode="rw">
user creation

<form action="/user" method="post">
<div class="login">
<label for="login">login</label>
<input name="login" id="login" value="{login}"/>
</div>
<div class="password">
<label for="password">password</label>
<input name="password" id="password" value="{password}" type="password"/>
</div>
<div class="email">
<label for="email">email</label>
<input name="email" type="email" value="{email}"/>
</div>
""")
    
    xsl.append(protect_with_captcha(dotcom))
    xsl.append(b"""
<input type="submit"/>
</form>

</xsl:template>

<xsl:template match="component/get/put/user" mode="rw">
user update

<form action="/user/{id}/put" method="post">
<div class="login">
<label for="login">login</label>
<input name="login" value="{login}"/>
</div>
<div class="password">
<label for="password">password </label>
<input name="password" value="{password}" type="password"/>
</div>
<div class="email">
<label for="email">email</label>
<input name="email" value="{email}" type="email"/>
</div>
<div class="servershort">
<label for="servershort">servershort</label> 
<input name="servershort" value="{servershort}"/>
</div>
""")
    
    # xsl.append(protect_with_captcha(dotcom))
    xsl.append(b"""
<input type="submit"/>
</form>

</xsl:template>



<xsl:template match="USER" mode="rw">
user rw
<xsl:apply-templates select="gallery" mode="rw"/>
<xsl:apply-templates select="GALLERY" mode="rw"/>
<xsl:apply-templates select="pm" mode="rw"/>
<xsl:apply-templates select="friend" mode="rw"/>
<xsl:apply-templates select="wiki" mode="rw"/>
</xsl:template>


<xsl:template match="USER/GALLERY" mode="rw">
gallery rw11
<xsl:apply-templates select="pic" mode="rw"/>
<xsl:apply-templates select="comment" mode="rw"/>
<xsl:apply-templates select="phrase" mode="rw"/>
<xsl:apply-templates select="tag" mode="rw"/>
<xsl:apply-templates select="friend" mode="rw"/>
<xsl:apply-templates select="PIC" mode="rw"/>
</xsl:template>

<xsl:template match="USER/GALLERY/PIC" mode="rw">
PIC rw
<xsl:apply-templates select="tag" mode="rw"/>
<xsl:apply-templates select="phrase" mode="rw"/>
<xsl:apply-templates select="comment" mode="rw"/>
<xsl:apply-templates select="friend" mode="rw"/>
<xsl:apply-templates select="path" mode="rw"/>
</xsl:template>



<xsl:template match="USER/gallery" mode="rw">
<xsl:comment>usergalrw</xsl:comment>
<div class="gallery">
 <form action="" method="post">
  <div class="title">
   <label class="title" for="title">title</label>
   <input name="title" value="{title}"/>
   <xsl:apply-templates select="/response/Component/component/error/dataerror/title"/>
  </div>
  <div class="text">
   <label class="text" for="text">text</label>
   <input name="text" value="{text}"/>
  </div>
  <div class="path">
   <label class="path" for="path">path</label>
   <input name="path" value="{path}"/>
  </div>
  <div class="mode">
   <label class="mode" for="mode">mode</label>
   <select name="mode">
    <option value="b">
      <xsl:if test="mode = 'b'">
        <xsl:attribute name="selected">selected</xsl:attribute>
      </xsl:if>
      <xsl:text>puBlic</xsl:text>
    </option>

    <option value="v">
      <xsl:if test="mode = 'v'">
        <xsl:attribute name="selected">selected</xsl:attribute>
      </xsl:if>
      <xsl:text>priVate</xsl:text>
    </option>

    <option value="s">
      <xsl:if test="mode = 's'">
        <xsl:attribute name="selected">selected</xsl:attribute>
      </xsl:if>
      <xsl:text>Sell</xsl:text>
    </option>

    <option value="t">
      <xsl:if test="mode = 't'">
        <xsl:attribute name="selected">selected</xsl:attribute>
      </xsl:if>
      <xsl:text>proTect</xsl:text>
    </option>

    <option value="f">
      <xsl:if test="mode = 'f'">
        <xsl:attribute name="selected">selected</xsl:attribute>
      </xsl:if>
      <xsl:text>Friends</xsl:text>
    </option>

   </select>
  </div>
  <div class="secret">
   <label class="secret" for="secret">secret</label>
   <input name="secret" value="{secret}"/>
  </div>
  <input type="submit"/>
 </form>
</div>
</xsl:template>










<xsl:template match="USER/pm" mode="rw">
<div class="pm">

<form action="" method="post">
<div class="title">
title
<input name="title" value="{title}"/>
</div>
<div class="text">
text <input name="text" value="{text}"/>
</div>
 <input type="submit"/>
</form>
</div>

</xsl:template>





<xsl:template match="USER/friend" mode="rw">
<div class="friend">

<form action="" method="post">
<div class="friend">
friend
<input name="friend" value="{friend}"/>
</div>
 <input type="submit"/>
</form>
</div>

</xsl:template>



<xsl:template match="USER/wiki" mode="rw">
<div class="wiki">
user wiki
<form action="" method="post">
<div class="wikitext">
wikitext
<input name="wikitext" value="{wikitext}"/>
</div>
 <input type="submit"/>
</form>
</div>

</xsl:template>




<xsl:template match="USER/GALLERY/friend" mode="rw">
<div class="friend">

<form action="" method="post">
<div class="friend">
friend
<input name="friend" value="{friend}"/>
</div>
 <input type="submit"/>
</form>
</div>

</xsl:template>


<xsl:template match="USER/GALLERY/PIC/friend" mode="rw">
<div class="friend">

<form action="" method="post">
<div class="friend">
friend
<input name="friend" value="{friend}"/>
</div>
 <input type="submit"/>
</form>
</div>

</xsl:template>




<xsl:template match="USER/GALLERY/comment" mode="rw">
<div class="comment">

<form action="" method="post">
<div class="title">
title
<input name="title" value="{title}"/>
</div>
<div class="text">
text <input name="text" value="{text}"/>
</div>
 <input type="submit"/>
</form>
</div>

</xsl:template>




<xsl:template match="USER/GALLERY/phrase" mode="rw">
<div class="phrase">

<form action="" method="post">
<div class="text">
text <input name="text" value="{text}"/>
</div>
 <input type="submit"/>
</form>
</div>

</xsl:template>



<xsl:template match="USER/GALLERY/tag" mode="rw">
<div class="tag">
tag rw
<form action="" method="post">
<div class="text">
text <input name="text" value="{text}"/>
</div>
 <input type="submit"/>
</form>
</div>

</xsl:template>



<xsl:template match="USER" mode="delete">
<div class="USER">
<xsl:apply-templates mode="delete"/>
</div>
</xsl:template>

<xsl:template match="USER/GALLERY" mode="delete">
<div class="GALLERY">
<xsl:apply-templates mode="delete"/>
</div>
</xsl:template>


<xsl:template match="USER/GALLERY/pic" mode="delete">
<div class="pic">
<form method="post">
Confirm the delete?
<input type="submit"/>
</form>
</div>
</xsl:template>



<xsl:template match="USER/GALLERY/pic" mode="rw">
<div class="pic">



<!-- default in HTML is Content-Type: application/x-www-form-urlencoded -->
<!-- we need multipart/form-data -->
<form action="" method="post" enctype="multipart/form-data">
addnewpic23
<div class="title">
title
<input name="title" value="{title}"/>
</div>
<div class="text">
text <input name="text" value="{text}"/>
</div>


<div class="userfile">
file <input type="file" name="userfile"/>
</div>

 <input type="submit"/>
</form>
</div>

</xsl:template>



<xsl:template match="USER/GALLERY/PIC/tag" mode="rw">
<div class="tag">
tag rw
<form action="" method="post">
<div class="text">
text <input name="text" value="{text}"/>
</div>
 <input type="submit"/>
</form>
</div>

</xsl:template>



<xsl:template match="USER/GALLERY/PIC/phrase" mode="rw">
<div class="phrase">

<form action="" method="post">
phrase rw
<div class="text">
text <input name="text" value="{text}"/>
</div>
 <input type="submit"/>
</form>
</div>

</xsl:template>



<xsl:template match="USER/GALLERY/PIC/comment" mode="rw">
<div class="comment">

<form action="" method="post">
phrase rw
<div class="text">
text <input name="text" value="{text}"/>
</div>
 <input type="submit"/>
</form>
</div>

</xsl:template>



<xsl:template match="USER/GALLERY/PIC/path" mode="rw">
<div class="path">

<form action="" method="post">
path rw
<div class="text">
path <input name="path" value="{path}"/>
</div>
 <input type="submit"/>
</form>
</div>

</xsl:template>





<xsl:template match="USER/gallery">
<div class="gallery">
<xsl:apply-templates select="id"/>
<xsl:apply-templates select="title"/>
<xsl:apply-templates select="text" mode="identity"/><!-- conserve HTML tags -->
<xsl:apply-templates select="path"/>
<xsl:apply-templates select="mode"/>
<xsl:apply-templates select="secret"/>
<br/>
<xsl:comment>Take into account secret keys</xsl:comment>
<xsl:element name="a">
<xsl:attribute name="href">
<xsl:text>/gallery/</xsl:text>
<xsl:value-of select="id"/>
<xsl:text>/pic</xsl:text>
<xsl:if test="/response/request/querystring/secret">
<xsl:text>?secret=</xsl:text>
<xsl:value-of select="/response/request/querystring/secret"/>
</xsl:if>
</xsl:attribute>
<xsl:text>pic</xsl:text>
</xsl:element><br/>
<a href="/gallery/{id}/pic/post">add a pic</a><br/>
<a href="/gallery/{id}/tag">tag</a> <br/>
<a href="/gallery/{id}/phrase">phrase</a> <br/>
<a href="/gallery/{id}/friend">friend</a> 
</div>
</xsl:template>

<xsl:template match="USER/gallery/dir">
<div class="dir"><xsl:text>Parent:</xsl:text>
<a href="/gallery/{.}"><xsl:value-of select="."/></a>
</div>
</xsl:template>

<xsl:template match="USER/gallery/id">
<div class="id">
<a href="/gallery/{.}"><xsl:value-of select="."/></a>
</div>
</xsl:template>

<xsl:template match="USER/gallery/title">
<div class="title">
<xsl:apply-templates/>
</div>
</xsl:template>

<xsl:template match="USER/gallery/text">
<div class="text">
<xsl:apply-templates/>
</div>
</xsl:template>

<xsl:template match="USER/gallery/path">
<div class="path">
<xsl:apply-templates/>
</div>
</xsl:template>


<xsl:template match="USER/gallery/mode">
<div class="mode">
mode: <xsl:apply-templates/>
<xsl:if test="node()='v'"> (priVate) <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../id}?secret={../secret}">secret url</a></xsl:if>
<xsl:if test="node()='b'"> (puBlic)</xsl:if>
<xsl:if test="node()='s'"> (Sell)</xsl:if>
<xsl:if test="node()='t'"> (proTect)</xsl:if>
<xsl:if test="node()='f'"> (Friend)</xsl:if>
</div>
</xsl:template>



<xsl:template match="USER/gallery/secret">
<div class="secret">
secret: <xsl:apply-templates/>
</div>
</xsl:template>






<xsl:template match="USER/GALLERY">
<div class="GALLERY">
Gallery <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{id}"><xsl:value-of select="id"/></a>
<xsl:apply-templates select="PIC|Pic|pic"/>
<xsl:apply-templates select="TAG|Tag|tag"/>
<xsl:apply-templates select="PHRASE|Phrase|phrase"/>
<xsl:apply-templates select="COMMENT|Comment|comment"/>


</div>
</xsl:template>



<xsl:template match="USER/GALLERY/PIC">
<div class="PIC">
PICss <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../id}/pic/{id}"><xsl:value-of select="id"/></a>
<xsl:apply-templates select="TAG|Tag|tag"/>
<xsl:apply-templates select="PHRASE|Phrase|phrase"/>
<xsl:apply-templates select="COMMENT|Comment|comment"/>
<xsl:apply-templates select="TREE|Tree|tree"/>
<xsl:apply-templates select="FRIEND|Friend|friend"/>
</div>
</xsl:template>








<xsl:template match="USER/GALLERY/PIC/tag">
<div class="tag">
tagFF <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../../id}/pic/{../id}/tag/{id}"><xsl:value-of select="id"/></a>
text: <xsl:value-of select="text"/>

<a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../../id}/pic/{../id}/tag/post">Update/Insert8 this tag</a>

</div>
</xsl:template>


<xsl:template match="USER/GALLERY/PIC/Tag">
<div class="Tag">
Tag <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../../id}/pic/{../id}/tag/{id}"><xsl:value-of select="id"/></a>
<xsl:apply-templates select="tag"/>
<a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../../id}/pic/{../id}/tag/post">Update/Insert1 a new tag</a>
</div>
</xsl:template>


<xsl:template match="USER/GALLERY/PIC/Tag/tag">
<div class="tag">
tagDD <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../../id}/pic/{../id}/tag/{id}"><xsl:value-of select="id"/></a>
text: <xsl:value-of select="text"/>
</div>
</xsl:template>









<xsl:template match="USER/GALLERY/PIC/comment">
<div class="comment">
comment <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../../id}/pic/{../id}/comment/{id}"><xsl:value-of select="id"/></a>
text: <xsl:value-of select="text"/>
</div>
</xsl:template>


<xsl:template match="USER/GALLERY/PIC/Comment">
<div class="Comment">
Comment <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../../id}/pic/{../id}/comment/{id}"><xsl:value-of select="id"/></a>
<xsl:apply-templates select="comment"/>
<a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../../id}/pic/{../id}/comment/post">Insert a new comment</a>
</div>
</xsl:template>


<xsl:template match="USER/GALLERY/PIC/Comment/comment">
<div class="comment">
comment <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../../id}/pic/{../id}/comment/{id}"><xsl:value-of select="id"/></a>
text: <xsl:value-of select="text"/>
</div>
</xsl:template>












<xsl:template match="USER/GALLERY/PIC/path">
<div class="path">
path <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../../id}/pic/{../id}/path/{id}"><xsl:value-of select="id"/></a>
path: <xsl:value-of select="path"/>
</div>
</xsl:template>









<xsl:template match="USER/GALLERY/PIC/phrase">
<div class="phrase">
phrase <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../../id}/pic/{../id}/phrase/{id}"><xsl:value-of select="id"/></a>
text: <xsl:value-of select="text"/>
</div>
</xsl:template>


<xsl:template match="USER/GALLERY/PIC/Phrase">
<div class="Phrase">
PhraseHH <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../../id}/pic/{../id}/phrase/{id}"><xsl:value-of select="id"/></a>
<xsl:apply-templates select="phrase"/>
<a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../../id}/pic/{../id}/phrase/post">Add a new phrase</a>
</div>
</xsl:template>


<xsl:template match="USER/GALLERY/PIC/Phrase/phrase">
<div class="phrase">
phrase <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../../id}/pic/{../id}/phrase/{id}"><xsl:value-of select="id"/></a>
text: <xsl:value-of select="text"/>
</div>
</xsl:template>










<xsl:template match="USER/GALLERY/Pic">
<div class="Pic">
<xsl:call-template name="previousapi"/>
<xsl:call-template name="nextapi"/>


<!-- BEGIN DRAG and DROP -->

<!--
<div id="dropTarget" style="width: 100%; height: 100px; border: 1px #ccc solid; padding: 10px;">dragand drop some files here</div>
<div id="filesInfo"></div>
<div id="filesStatus"></div>


<script src="/dragdrop.js"/>
-->
<!-- END DRAG and DROP -->


Gallery22 <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../id}"><xsl:value-of select="../id"/></a>

<xsl:apply-templates select="." mode="divapi"/>

<xsl:call-template name="nextapi"/>
</div>
</xsl:template>



<xsl:template match="Pic" mode="divapi">
<div id="divapiPic" class="Pic">
<xsl:apply-templates mode="divapi"/>
</div>
<script>
	jQuery(document).ready(function() { 
		jQuery("#divapiPic").justifiedGallery({
			rowHeight : 120,
			fixedHeight : false, 
			captions : true, 
			margins : 7,
                        lastRow : 'nojustify',
			randomize : false,
			waitThumbnailsLoad : false,
			sizeRangeSuffixes: {
			}
		}); 
	});
</script>

</xsl:template>

<xsl:template match="pic" mode="divapi">
<xsl:comment>displaying pic in mode divapi 8888</xsl:comment>
<div class="pic">
<xsl:element name="a">
<xsl:attribute name="href">
<xsl:text>http://</xsl:text>
<xsl:value-of select="ancestor::USER/servershort"/>
<xsl:text>.atpic"""+dotcom+b"""/gallery/</xsl:text>
<xsl:value-of select="../../id"/>
<xsl:text>/pic/</xsl:text>
<xsl:value-of select="id"/>
<xsl:if test="/response/request/querystring/secret">
  <xsl:text>?secret=</xsl:text>
  <xsl:value-of select="/response/request/querystring/secret"/>
</xsl:if>
</xsl:attribute>
<xsl:choose>
<xsl:when test="pathstore_r160">
<xsl:apply-templates select="pathstore_r160" mode="img1"/>
</xsl:when>
<xsl:otherwise>
No thumnail for pic <xsl:value-of select="id"/>
</xsl:otherwise>
</xsl:choose>
</xsl:element>
<xsl:value-of select="originalname"/>
</div>
</xsl:template>




<xsl:template match="Pic" mode="divsearch">
<xsl:comment>mode divsearch</xsl:comment>
<xsl:call-template name="previousbutton"/>
<xsl:call-template name="nextbutton"/>
<xsl:apply-templates select="pic" mode="divsearch"/>
<xsl:call-template name="previousbutton"/>
<xsl:call-template name="nextbutton"/>
</xsl:template>

<xsl:template match="pic" mode="divsearch">
<xsl:comment>pic mode divsearch</xsl:comment>
<xsl:call-template name="searchpiclink"/>
</xsl:template>








<xsl:template match="USER/GALLERY/Pic/pic">
<div class="pic">
Pic <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../../id}/pic/{id}"><xsl:value-of select="id"/></a>

<br/>
<xsl:apply-templates select="pathstore_r160" mode="img2"/>

</div>
</xsl:template>


<xsl:template match="USER/GALLERY/pic">
<div class="pic">
picdis000
<a href="/gallery/{gallery}/pic/{id}">Pic<xsl:value-of select="id"/></a>
<div class="title">
<xsl:value-of select="title"/>
</div>
<div class="text">
<xsl:value-of select="text"/>
</div>
<div class="originalname">
<xsl:value-of select="originalname"/>
</div>

<xsl:variable name="code" select="ancestor::component/request/querystring/code"/>


<xsl:if test="$code = 'r70'">
<xsl:apply-templates select="pathstore_r70" mode="img1"/>
</xsl:if>
<xsl:if test="$code = 'r160'">
<xsl:apply-templates select="pathstore_r160" mode="img1"/>
</xsl:if>
<xsl:if test="$code = 'r350'">
<xsl:apply-templates select="pathstore_r350" mode="img1"/>
</xsl:if>
<xsl:if test="$code = 'r600'">
<xsl:apply-templates select="pathstore_r600" mode="img1"/>
</xsl:if>
<xsl:if test="$code = 'r1024'">
<xsl:apply-templates select="pathstore_r1024" mode="img1"/>
</xsl:if>
<!-- default -->
<xsl:if test="not($code)">
<xsl:apply-templates select="pathstore_r350" mode="img1"/>
</xsl:if>
<br/>

Resolutions available:<br/>
<xsl:apply-templates select="pathstore" mode="link1"/>
<xsl:apply-templates select="pathstore_r70" mode="link1"/>
<xsl:apply-templates select="pathstore_r160" mode="link1"/>
<xsl:apply-templates select="pathstore_r350" mode="link1"/>
<xsl:apply-templates select="pathstore_r600" mode="link1"/>
<xsl:apply-templates select="pathstore_r1024" mode="link1"/>



<a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../id}/pic/{id}/tag">tag</a> 
<a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../id}/pic/{id}/phrase">phrase</a> 

</div>
</xsl:template>

<!-- ============== text link to raw images ================== -->

<xsl:template match="pathstore" mode="link1">
<a href="http://{ancestor::USER/servershort}.atpicdata"""+dotcom+b"""/{.}">Full</a><br/>
</xsl:template>

<xsl:template match="pathstore_r70" mode="link1">
<a href="http://{ancestor::USER/servershort}.atpicdata"""+dotcom+b"""/{.}">70px</a><br/>
</xsl:template>

<xsl:template match="pathstore_r160" mode="link1">
<a href="http://{ancestor::USER/servershort}.atpicdata"""+dotcom+b"""/{.}">160px</a><br/>
</xsl:template>

<xsl:template match="pathstore_r350" mode="link1">
<a href="http://{ancestor::USER/servershort}.atpicdata"""+dotcom+b"""/{.}">350px</a><br/>
</xsl:template>

<xsl:template match="pathstore_r600" mode="link1">
<a href="http://{ancestor::USER/servershort}.atpicdata"""+dotcom+b"""/{.}">600px</a><br/>
</xsl:template>

<xsl:template match="pathstore_r1024" mode="link1">
<a href="http://{ancestor::USER/servershort}.atpicdata"""+dotcom+b"""/{.}">1024px</a><br/>
</xsl:template>




<!-- ================== IMG tag ============== -->




<xsl:template match="pathstore_r70|pathstore_r160|pathstore_r350" mode="imgsearch1">
<img src="http://{../servershort}.atpicdata"""+dotcom+b"""/{.}" alt="Pp {../id}"/>
</xsl:template>




<xsl:template match="pathstore_r70|pathstore_r160|pathstore_r350|pathstore_r600|pathstore_r1024" mode="imgsearch1_linkapi">
<xsl:comment>imgsearch1_linkapi</xsl:comment>
<a href="http://{../servershort}.atpic"""+dotcom+b"""/gallery/{../gid}/pic/{../pid}"><xsl:apply-templates select="." mode="img1"/></a>
</xsl:template>







<!-- used for API -->


<xsl:template match="pathstore|pathstore_r70|pathstore_r160|pathstore_r350|pathstore_r600|pathstore_r1024" mode="img1">
<xsl:comment>image source for pathstore PPRR</xsl:comment>
<xsl:element name="img">
<xsl:attribute name="src">
<xsl:text>http://</xsl:text>

<xsl:choose>
<xsl:when test="ancestor::USER/servershort">
<xsl:comment>there is a ancestor::USER/servershort</xsl:comment>
<xsl:value-of select="ancestor::USER/servershort"/>
</xsl:when>
<xsl:otherwise>
<xsl:comment>no ancestor::USER/servershort, trying ../servershort</xsl:comment>
<xsl:value-of select="../servershort"/>
</xsl:otherwise>
</xsl:choose>

<xsl:text>.atpicdata"""+dotcom+b"""/</xsl:text>
<xsl:value-of select="."/>
</xsl:attribute>
<xsl:apply-templates select="." mode="widthheight"/>
<xsl:attribute name="alt">
<xsl:text>Pic</xsl:text>
<xsl:choose>
<xsl:when test="../pid">
<xsl:comment>there is a ..pid</xsl:comment>
<xsl:value-of select="../pid"/>
</xsl:when>
<xsl:otherwise>
<xsl:comment>no ..pid, trying ../id</xsl:comment>
<xsl:value-of select="../id"/>
</xsl:otherwise>
</xsl:choose>
</xsl:attribute>
</xsl:element>
</xsl:template>

<xsl:template match="pathstore|pathstore_r70|pathstore_r160|pathstore_r350|pathstore_r600|pathstore_r1024" mode="widthheight">
<!-- put the width and height used by justified gallery -->
<xsl:if test="local-name()='pathstore_r70'">
<xsl:if test="../width_r70">
<xsl:attribute name="width"><xsl:value-of select="../width_r70"/></xsl:attribute>
</xsl:if>
<xsl:if test="../height_r70">
<xsl:attribute name="height"><xsl:value-of select="../height_r70"/></xsl:attribute>
</xsl:if>
</xsl:if>


<xsl:if test="local-name()='pathstore_r160'">
<xsl:if test="../width_r160">
<xsl:attribute name="width"><xsl:value-of select="../width_r160"/></xsl:attribute>
</xsl:if>
<xsl:if test="../height_r160">
<xsl:attribute name="height"><xsl:value-of select="../height_r160"/></xsl:attribute>
</xsl:if>
</xsl:if>


<xsl:if test="local-name()='pathstore_r350'">
<xsl:if test="../width_r350">
<xsl:attribute name="width"><xsl:value-of select="../width_r350"/></xsl:attribute>
</xsl:if>
<xsl:if test="../height_r350">
<xsl:attribute name="height"><xsl:value-of select="../height_r350"/></xsl:attribute>
</xsl:if>
</xsl:if>

<xsl:if test="local-name()='pathstore_r600'">
<xsl:if test="../width_r600">
<xsl:attribute name="width"><xsl:value-of select="../width_r600"/></xsl:attribute>
</xsl:if>
<xsl:if test="../height_r600">
<xsl:attribute name="height"><xsl:value-of select="../height_r600"/></xsl:attribute>
</xsl:if>
</xsl:if>

<xsl:if test="local-name()='pathstore_r1024'">
<xsl:if test="../width_r1024">
<xsl:attribute name="width"><xsl:value-of select="../width_r1024"/></xsl:attribute>
</xsl:if>
<xsl:if test="../height_r1024">
<xsl:attribute name="height"><xsl:value-of select="../height_r1024"/></xsl:attribute>
</xsl:if>
</xsl:if>
</xsl:template>


<!-- ================================ -->


<xsl:template match="pathstore|pathstore_r70|pathstore_r160|pathstore_r350|pathstore_r600|pathstore_r1024" mode="img2">
<a href="http://{ancestor::component/request/pathinfo}/{../id}"><img src="http://http://{ancestor::USER/servershort}.atpicdata"""+dotcom+b"""/{.}" alt="pps {../pid}"/></a><br/>
</xsl:template>




<!-- ================================ -->

<xsl:template match="USER/GALLERY/Tag">
<div class="Tag">
Tag
<xsl:apply-templates select="tag"/>
<a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../id}/tag/post">Update/Insert2 a new tag</a>
</div>
</xsl:template>


<xsl:template match="USER/GALLERY/Tag/tag">
<div class="tag">
tagYH
 <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../../id}/tag/{id}"><xsl:value-of select="id"/></a>
<xsl:apply-templates/>
</div>
</xsl:template>



<xsl:template match="USER/GALLERY/tag">
<div class="tag">
tag
by: <xsl:value-of select="id"/>
text: <xsl:value-of select="text"/>
datelast: <xsl:value-of select="datelast"/>
 <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../id}/tag/{id}/put">Update5 this tag</a>

</div>
</xsl:template>






<xsl:template match="USER/GALLERY/Friend">
<div class="Friend">
<a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../id}/friend/post">Add2 a new friend</a>
<xsl:apply-templates select="friend"/>
</div>
</xsl:template>


<xsl:template match="USER/GALLERY/Friend/friend">
<div class="friend">
<xsl:apply-templates select="id"/>
</div>
</xsl:template>

<xsl:template match="USER/GALLERY/friend">
<div class="friend">
friend<xsl:value-of select="id"/>
</div>
</xsl:template>






<xsl:template match="USER/GALLERY/Comment">
<div class="Comment">
Comment
<xsl:apply-templates select="comment"/>
<a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../id}/comment/post">Update/Insert3 a new comment</a>
</div>
</xsl:template>


<xsl:template match="USER/GALLERY/Comment/comment">
<div class="comment">
comment
 <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../../id}/pic/{../id}/comment/{id}"><xsl:value-of select="id"/></a>
<xsl:apply-templates/>
</div>
</xsl:template>



<xsl:template match="USER/GALLERY/comment">
<div class="comment">
comment
by: <xsl:value-of select="id"/>
text: <xsl:value-of select="text"/>
datelast: <xsl:value-of select="datelast"/>

</div>
</xsl:template>










<xsl:template match="USER/GALLERY/Phrase">
<div class="Phrase">
Phrase
<xsl:apply-templates select="phrase"/>
<a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../id}/phrase/post">Update/Insert4 a new phrase</a>
</div>
</xsl:template>


<xsl:template match="USER/GALLERY/Phrase/phrase">
<div class="phrase">
phrase
 <a href="http://{ancestor::USER/servershort}.atpic"""+dotcom+b"""/gallery/{../id}/phrase/{id}"><xsl:value-of select="id"/></a>
<xsl:apply-templates/>
</div>
</xsl:template>



<xsl:template match="USER/GALLERY/phrase">
<div class="phrase">
phrase
by: <xsl:value-of select="id"/>
text: <xsl:value-of select="text"/>
datelast: <xsl:value-of select="datelast"/>

</div>
</xsl:template>




<!--  search is only for GET method  -->



<xsl:template match="get/USER/SEARCH">
<form>userform<input name="q" value="{ancestor::component/request/querystring/q}"/></form>
<xsl:apply-templates/>
</xsl:template>


<xsl:template match="get/USER/SEARCH/Pic">
<div class="Pic">
<xsl:apply-templates select="." mode="divsearch"/>
</div>
</xsl:template>




<xsl:template match="get/USER/SEARCH/pic">
<div class="pic">onepicresult:

<!-- previous -->
<xsl:call-template name="navrank_previous"/>

<!-- next -->
<xsl:call-template name="navrank_next"/>


</div>
</xsl:template>



<xsl:template name="previousbutton">
<xsl:param name="querystring" select="/response/request/querystring"/> 
<xsl:param name="hits" select="ancestor::component/hits"/>
<xsl:param name="base" select="/response/request/pathinfo"/>
<xsl:param name="size" select="ancestor::component/size"/>
<xsl:param name="start" select="$querystring/start"/>

<xsl:if test="$start and ($size and ($start &gt;= $size) or not($size) and ($start &gt;= 10))">
<!-- we need a PREVIOUS button -->
<xsl:element name="a">
<xsl:attribute name="href">
<xsl:value-of select="$base" /><xsl:text>?</xsl:text>

<xsl:for-each select="$querystring/*">
<xsl:choose>
<!-- ================================ -->
<xsl:when test="name()='start'">
<xsl:choose>
<xsl:when test="$size">
<xsl:if test="(.-$size) &gt; 0">
<xsl:if test="not(position() = 1)">&amp;</xsl:if>
<xsl:text>start=</xsl:text><xsl:value-of select=".-$size" />
</xsl:if>
</xsl:when>
<xsl:otherwise>
<xsl:if test="(.-10) &gt; 0">
<xsl:if test="not(position() = 1)">&amp;</xsl:if>
<xsl:text>start=</xsl:text><xsl:value-of select=".-10" />
</xsl:if>
</xsl:otherwise>
</xsl:choose>
</xsl:when>
<!-- ================================ -->
<xsl:otherwise>
<!--<xsl:if test="../*[position()=1 and name()='start']">startisFIRST</xsl:if>-->
<xsl:if test="
not(position() = 1) 
and (
  not(../*[position()=1 and name()='start'])
  or (
      ../*[position()=1 and name()='start'] 
      and (($size and ($start &gt; $size)) or (not($size) and ($start &gt; 10)))
     )
    )
">&amp;</xsl:if>
<xsl:value-of select="name()" /><xsl:text>=</xsl:text><xsl:value-of select="." />
</xsl:otherwise>
</xsl:choose>
</xsl:for-each>


</xsl:attribute>
<xsl:text>Previous</xsl:text>
</xsl:element>

</xsl:if>

</xsl:template>








<xsl:template name="nextapi">
<xsl:call-template name="next_previous_api">
<xsl:with-param name="previous_next" select="'next'" />
</xsl:call-template>
</xsl:template>


<xsl:template name="previousapi">
<xsl:call-template name="next_previous_api">
<xsl:with-param name="previous_next" select="'previous'" />
</xsl:call-template>
</xsl:template>


<xsl:template name="next_previous_api">
<xsl:param name="previous_next"/>

<xsl:comment>NEXTAPI</xsl:comment>
<!-- variables -->
<xsl:variable name="lastid" select="child::*[position()=last()]/id" />
<xsl:variable name="firstid" select="child::*[position()=1]/id" />
<xsl:variable name="countid"  select="count(child::*/id)"/>

<xsl:if test="($previous_next = 'next' and ancestor::component/hasnext) or ($previous_next = 'previous' and  ancestor::component/hasprevious)">
<div class="nextapi">
<xsl:element name="a">
<xsl:attribute name="href">
<xsl:value-of select="ancestor::component/request/pathinfo"/>
<xsl:text>?</xsl:text>
<xsl:for-each select="ancestor::component/request/querystring/*">
 <xsl:choose>
 <xsl:when test="name()='end' or name()='start'"/> <!-- do nothing -->
 <xsl:otherwise>
 <xsl:value-of select="name()" /><xsl:text>=</xsl:text><xsl:value-of select="." /><xsl:text>&amp;</xsl:text>
 </xsl:otherwise>
 </xsl:choose>
</xsl:for-each>


<xsl:choose>
<xsl:when test="$previous_next = 'next'">
 <xsl:text>start=</xsl:text>
 <xsl:value-of select="$lastid" />
</xsl:when>
<xsl:otherwise>
 <xsl:text>end=</xsl:text>
 <xsl:value-of select="$firstid" />
</xsl:otherwise>
</xsl:choose>

</xsl:attribute>

<xsl:choose>
<xsl:when test="$previous_next = 'next'">
  <xsl:text>Next</xsl:text>
</xsl:when>
<xsl:otherwise>
  <xsl:text>Previous</xsl:text>
</xsl:otherwise>
</xsl:choose>
</xsl:element>
</div>
</xsl:if>


</xsl:template>











<xsl:template name="nextbutton">
<xsl:param name="querystring" select="/response/request/querystring"/> 
<xsl:param name="hits" select="ancestor::component/hits"/>
<xsl:param name="base" select="/response/request/pathinfo"/>
<xsl:param name="size" select="ancestor::component/size"/>
<xsl:param name="start" select="$querystring/start"/>
<xsl:if test="($size and ($hits &gt; $start+$size) or (not($start) and $hits &gt; $size)) or (not($size) and ($hits &gt; $start+10) or (not($start) and $hits &gt; 10))">
<!-- we need a NEXT button -->

<xsl:element name="a">
<xsl:attribute name="href">
<xsl:value-of select="$base" /><xsl:text>?</xsl:text>

<xsl:for-each select="$querystring/*">
<xsl:value-of select="name()" /><xsl:text>=</xsl:text>
<xsl:choose>
<xsl:when test="name()='start'">
<xsl:choose>
<xsl:when test="$size">
<xsl:value-of select=".+$size" />
</xsl:when>
<xsl:otherwise>
<xsl:value-of select=".+10" />
</xsl:otherwise>
</xsl:choose>
</xsl:when>
<xsl:otherwise>
<xsl:value-of select="." />
</xsl:otherwise>
</xsl:choose>
<xsl:if test="not(position() = last())">&amp;</xsl:if>
</xsl:for-each>


<xsl:if test="not($start)">
<xsl:if test="$querystring[node()]">
<xsl:text>&amp;</xsl:text>
</xsl:if>
<xsl:text>start=</xsl:text>
<xsl:choose>
<xsl:when test="$size">
<xsl:value-of select="$size" />
</xsl:when>
<xsl:otherwise>
<xsl:text>10</xsl:text>
</xsl:otherwise>
</xsl:choose>
</xsl:if>


</xsl:attribute>
<xsl:text>Next</xsl:text>
</xsl:element>
</xsl:if>

</xsl:template>







<xsl:template match="get/USER/SEARCH/Pic/pic">
<div class="pic">
<xsl:call-template name="searchpiclink"/>
</div>
</xsl:template>







<!-- search results -->

<xsl:template match="get/SEARCH">
<form>normalsearch<input name="q" value="{../../../request/querystring/q}"/></form>
<xsl:apply-templates/>
</xsl:template>




<xsl:template match="get/SEARCH/Pic">


<div class="Pic">search result:
<xsl:apply-templates select="." mode="divsearch"/>
</div>
</xsl:template>


<xsl:template match="get/SEARCH/Pic/pic">
<div class="pic">
<xsl:call-template name="searchpiclink"/>
</div>
</xsl:template>



<xsl:template match="get/SEARCH/pic">
<div class="pic">
<!-- one pic -->
<xsl:call-template name="navrank_previous"/>
<xsl:call-template name="navrank_next"/>
</div>
</xsl:template>



<xsl:template name="navrank_previous">
<xsl:call-template name="navrank">
<xsl:with-param name="delta" select="1" />
<xsl:with-param name="text" select="'next'" />
</xsl:call-template>
</xsl:template>

<xsl:template name="navrank_next">
<xsl:call-template name="navrank">
<xsl:with-param name="delta" select="-1" />
<xsl:with-param name="text" select="'previous'" />
</xsl:call-template>
</xsl:template>



<xsl:template name="navrank">
<xsl:param name="querystring" select="ancestor::component/request/querystring"/> 
<xsl:param name="base" select="/response/request/pathinfo"/>
<xsl:param name="pic" select="."/>
<xsl:param name="hits" select="ancestor::component/hits"/>
<xsl:param name="delta"/>
<xsl:param name="text"/>
navrank

<xsl:choose>
<xsl:when test="(($querystring/rank+$delta) &lt;= $hits) and (($querystring/rank+$delta) &gt; 0)">
NEEDLINK
<xsl:element name="a">
<xsl:attribute name="href">
<xsl:value-of select="$base"/>
<xsl:text>?</xsl:text>
<xsl:for-each select="$querystring/*">
<xsl:if test="not(position() = 1) ">
<xsl:text>&amp;</xsl:text>
</xsl:if>

<xsl:choose>
<xsl:when test="name()='rank'">
<xsl:text>rank=</xsl:text>
<xsl:value-of select=".+$delta"/>
</xsl:when>

<xsl:otherwise>
<xsl:value-of select="name()"/>
<xsl:text>=</xsl:text>
<xsl:value-of select="."/>
</xsl:otherwise>
</xsl:choose>

</xsl:for-each>
</xsl:attribute>
<xsl:value-of select="$text"/>
</xsl:element>
</xsl:when>



<xsl:otherwise>
NEEDNOLINK
</xsl:otherwise>
</xsl:choose>


</xsl:template>



<!--  user home search  -->


<xsl:template match="get/HOME/SEARCH">
<xsl:apply-templates/>
<div class="navchildren">
<a href="/user">user</a>
</div>
</xsl:template>

<xsl:template match="get/HOME/SEARCH/Pic">
<div class="Pic">
<div class="random">Some Random Pictures:</div>
<xsl:apply-templates select="." mode="random"/>
</div>
</xsl:template>




<xsl:template match="Pic" mode="random"> 
<!-- 6 random images  -->
<xsl:comment>6 random images</xsl:comment>
<div id="randomgallery">
<xsl:apply-templates mode="random"/>
</div>
<script>
	jQuery(document).ready(function() { 
		jQuery("#randomgallery").justifiedGallery({
			rowHeight : 200,
			fixedHeight : false, 
			captions : true, 
			margins : 7,
                        lastRow : 'hide',
                        randomize : true,
			waitThumbnailsLoad : false,
			sizeRangeSuffixes: {
			}
		}); 
	});
</script>
</xsl:template>

<xsl:template match="pic" mode="random">
<xsl:apply-templates select="pathstore_r350" mode="imgsearch1_linkapi"/>
</xsl:template>




















<xsl:template match="Pic" mode="random2"> 
<!-- not used anymore, no table please -->
<!-- 6 random images in a table -->
<table>
<tr>
<td>
<xsl:apply-templates select="pic[position()=1]/pathstore_r350" mode="imgsearch1_linkapi"/>
</td>
<td>
<table>
<tr>
<td>
<xsl:apply-templates select="pic[position()=2]/pathstore_r160" mode="imgsearch1_linkapi"/>
</td>
</tr>
<tr>
<td>
<xsl:apply-templates select="pic[position()=3]/pathstore_r160" mode="imgsearch1_linkapi"/>
</td>
</tr>
</table>
</td>
<td>
<table>
<tr>
<td>
<xsl:apply-templates select="pic[position()=4]/pathstore_r70" mode="imgsearch1_linkapi"/>
</td>
</tr>
<tr>
<td>
<xsl:apply-templates select="pic[position()=5]/pathstore_r70" mode="imgsearch1_linkapi"/>
</td>
</tr>
<tr>
<td>
<xsl:apply-templates select="pic[position()=6]/pathstore_r70" mode="imgsearch1_linkapi"/>
</td>
</tr>
<tr>
<td>
<xsl:apply-templates select="pic[position()=7]/pathstore_r70" mode="imgsearch1_linkapi"/>
</td>
</tr>
</table>
</td>
</tr>
</table>
</xsl:template>

<!-- userhome -->


<!-- user home some random pics -->

<xsl:template match="get/HOME/USER">
<xsl:apply-templates/>
<div class="navchildren">
<a href="/gallery">gallery</a>
<a href="/tree">tree</a>
<a href="/blog">blog</a>
</div>
</xsl:template>

<xsl:template match="get/HOME/USER/SEARCH/Pic">
<div class="Pic">
<div class="random">Some Random Pictures:</div>
<xsl:apply-templates select="." mode="random"/>
</div>
</xsl:template>

<!-- user treesearch pics -->

<xsl:template match="get/USER/TREESEARCH/Pic">
<div class="Pic">Tree Pictures:
<xsl:apply-templates select="." mode="divsearch"/>
</div>
</xsl:template>

<xsl:template match="get/USER/TREESEARCH/Pic/pic">
<div class="pic">
<xsl:call-template name="searchpiclink"/>
</div>
</xsl:template>


<xsl:template name="searchpiclink">
<!-- used in search results page --> 
<xsl:param name="querystring" select="/response/request/querystring"/>
<xsl:param name="base" select="/response/request/pathinfo"/>
<xsl:param name="pic" select="." />

<xsl:comment>searchpiclink</xsl:comment>
<!-- a new anchor (link) -->
<xsl:element name="a">
<xsl:attribute name="href">
<xsl:value-of select="$base"/>
<xsl:text>?</xsl:text>
<xsl:for-each select="$querystring/*">
<xsl:if test="not(position() = 1) ">
<xsl:text>&amp;</xsl:text>
</xsl:if>
<xsl:value-of select="name()"/>
<xsl:text>=</xsl:text>
<xsl:value-of select="."/>
</xsl:for-each>
<xsl:if test="$querystring/*[node()]">
<xsl:text>&amp;</xsl:text>
</xsl:if>
<xsl:text>rank=</xsl:text><xsl:value-of select="$pic/rank"/>
</xsl:attribute>
<xsl:attribute name="alt">
<xsl:text>Pic </xsl:text><xsl:value-of select="$pic/pid"/>
</xsl:attribute>
<img src="http://{$pic/servershort}.atpicdata"""+dotcom+b"""/{$pic/pathstore_r160}" alt="Picture {$pic/pid}"/>
</xsl:element>
</xsl:template>









<!-- user home treesearch pics -->

<xsl:template match="get/TREE/USER/TREESEARCH/Pic">
<div class="Pic">Tree Pictures:
<xsl:apply-templates select="." mode="divsearch"/>
</div>
</xsl:template>

<xsl:template match="get/TREE/USER/TREESEARCH/Pic/pic">
<div class="pic">
<xsl:call-template name="searchpiclink"/>
</div>
</xsl:template>














<!-- user vtreesearch pics -->

<xsl:template match="get/USER/VTREESEARCH/Pic">
<div class="Pic">Vtree Pictures:
<xsl:apply-templates select="." mode="divsearch"/>
</div>
</xsl:template>

<xsl:template match="get/USER/VTREESEARCH/Pic/pic">
<div class="pic">
Apic pid=<xsl:value-of select="pid"/>
</div>
</xsl:template>




<!-- user home vtreesearch pics -->

<xsl:template match="get/VTREE/USER/VTREESEARCH/Pic">
<div class="Pic">Vtree Pictures:
<xsl:apply-templates select="." mode="divsearch"/>
</div>
</xsl:template>

<xsl:template match="get/VTREE/USER/VTREESEARCH/Pic/pic">
<div class="pic">
Apic pid=<xsl:value-of select="pid"/>
</div>
</xsl:template>


















<!-- user geosearch pics -->

<xsl:template match="get/USER/GEOSEARCH/Pic">
<div class="Pic">Geo Pictures:
<xsl:apply-templates select="." mode="divsearch"/>
</div>
</xsl:template>

<xsl:template match="get/USER/GEOSEARCH/Pic/pic">
<div class="pic">
Apic pid=<xsl:value-of select="pid"/>
</div>
</xsl:template>




<!-- user home geosearch pics -->

<xsl:template match="get/GEO/USER/GEOSEARCH/Pic">
<div class="Pic">Geo Pictures:
<xsl:apply-templates select="." mode="divsearch"/>
</div>
</xsl:template>

<xsl:template match="get/GEO/USER/GEOSEARCH/Pic/pic">
<div class="pic">
Apic pid=<xsl:value-of select="pid"/>
</div>
</xsl:template>





















<!-- user datesearch pics -->

<xsl:template match="BLOGSEARCH/Pic">
<div class="Pic">Date Pictures:
<xsl:apply-templates select="." mode="divsearch"/>
</div>
</xsl:template>

<xsl:template match="BLOGSEARCH/Pic/pic">
<div class="pic">
Apic pid=<xsl:value-of select="pid"/>
<xsl:apply-templates select="pathstore_r160" mode="img1"/>

</div>
</xsl:template>










<!-- indentity modes -->


<xsl:template match="@*|node()" mode="identity2">
  <xsl:copy>
    <xsl:apply-templates select="@*|node()" mode="identity2"/>
  </xsl:copy>
</xsl:template>




<!-- same a identity but do not include xmlns -->
<xsl:template match="@*|node()" mode="identity">
  <xsl:copy>
    <xsl:apply-templates select="@*|node()" mode="identity"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="*" mode="identity">
  <xsl:element name="{local-name()}">
    <xsl:apply-templates select="@*|node()" mode="identity"/>
  </xsl:element>
</xsl:template>

















<!--  default facets, can override below if necessary -->

<!-- facets -->

<!-- TREENAV -->

<xsl:template match="USER/TREENAV/up[not(node())]">
EMPTYUP!!!!!!
</xsl:template>

<xsl:template match="USER/TREENAV/up[node()]">
<div class="up">
<a href="/treenav{.}">Up</a>
</div>
</xsl:template>


<xsl:template match="USER/TREENAV/Facet">
<div class="Facet">
<xsl:text>Facets:</xsl:text><xsl:apply-templates/>
</div>
</xsl:template>



<xsl:template match="USER/TREENAV/Facet/facet">
<div class="facet">
<xsl:text>facet:</xsl:text>
name: <xsl:value-of select="name"/><a href="/treenav/{name}"><xsl:value-of select="name"/></a>
hits: <xsl:value-of select="hits"/>
<xsl:apply-templates select="pic"/>
</div>
</xsl:template>

<xsl:template match="USER/TREENAV/Facet/facet/pic">
<div class="pic">
pid: <xsl:value-of select="pid"/>
gid: <xsl:value-of select="gid"/>
uid: <xsl:value-of select="uid"/>
<xsl:apply-templates select="pathstore_r70" mode="img1"/>

</div>
</xsl:template>




<!-- VTREENAV -->

<xsl:template match="USER/VTREENAV/Facet">
<div class="Facet">
<xsl:text>Facets:</xsl:text><xsl:apply-templates/>
</div>
</xsl:template>



<xsl:template match="USER/VTREENAV/Facet/facet">
<div class="facet">
<xsl:text>facet:</xsl:text>
name: <xsl:value-of select="name"/><a href="/vtreenav/{name}"><xsl:value-of select="name"/></a>
hits: <xsl:value-of select="hits"/>
<xsl:apply-templates select="pic"/>
</div>
</xsl:template>

<xsl:template match="USER/VTREENAV/Facet/facet/pic">
<div class="pic">
pid: <xsl:value-of select="pid"/>
gid: <xsl:value-of select="gid"/>
uid: <xsl:value-of select="uid"/>
</div>
</xsl:template>





<!-- GEONAV -->

<xsl:template match="USER/GEONAV/Facet">
<div class="Facet">
<xsl:text>Facets:</xsl:text><xsl:apply-templates/>
</div>
</xsl:template>



<xsl:template match="USER/GEONAV/Facet/facet">
<div class="facet">
<xsl:text>facet:</xsl:text>
name: <a href="/geonav{name}"><xsl:value-of select="name"/></a>
hits: <xsl:value-of select="hits"/>
<xsl:apply-templates select="pic"/>
</div>
</xsl:template>

<xsl:template match="USER/GEONAV/Facet/facet/pic">
<div class="pic">
pid: <xsl:value-of select="pid"/>
gid: <xsl:value-of select="gid"/>
uid: <xsl:value-of select="uid"/>
</div>
</xsl:template>









<!-- BLOGNAV -->

<xsl:template match="USER/BLOGNAV/Facet">
<div class="Facet">
<xsl:text>Facets:</xsl:text><xsl:apply-templates/>
</div>
</xsl:template>



<xsl:template match="USER/BLOGNAV/Facet/facet">
<div class="facet">
<xsl:text>facet:</xsl:text>
name: <a href="/blognav/{name}"><xsl:value-of select="name"/></a>
hits: <xsl:value-of select="hits"/>
<xsl:apply-templates select="pic"/>
</div>
</xsl:template>

<xsl:template match="USER/BLOGNAV/Facet/facet/pic">
<div class="pic">
pid: <xsl:value-of select="pid"/>
gid: <xsl:value-of select="gid"/>
uid: <xsl:value-of select="uid"/>
<xsl:apply-templates select="pathstore_r70" mode="img1"/>

</div>
</xsl:template>































<!-- repeat, to take precedence -->

<!-- composite facets -->

<!-- TREENAV -->


<xsl:template match="TREE/USER/TREENAV/up[not(node())]">
EMPTYUP!!!!!!
</xsl:template>

<xsl:template match="TREE/USER/TREENAV/up[node()]">
<div class="up">
<a href="/tree{.}">Up</a>
</div>
</xsl:template>



<xsl:template match="TREE/USER/TREENAV/Facet">
<div class="Facet">
<xsl:text>Facets:</xsl:text><xsl:apply-templates/>
</div>
</xsl:template>



<xsl:template match="TREE/USER/TREENAV/Facet/facet">
<div class="facet">
<xsl:text>facet:</xsl:text>
name: <xsl:value-of select="name"/><a href="/tree/{name}"><xsl:value-of select="name"/></a>
hits: <xsl:value-of select="hits"/>
<xsl:apply-templates select="pic"/>
</div>
</xsl:template>

<xsl:template match="TREE/USER/TREENAV/Facet/facet/pic">
<div class="pic">
pid: <xsl:value-of select="pid"/>
gid: <xsl:value-of select="gid"/>
uid: <xsl:value-of select="uid"/>
<xsl:apply-templates select="pathstore_r70" mode="img1"/>
</div>
</xsl:template>




<!-- VTREENAV -->

<xsl:template match="VTREE/USER/VTREENAV/Facet">
<div class="Facet">
<xsl:text>Facets:</xsl:text><xsl:apply-templates/>
</div>
</xsl:template>



<xsl:template match="VTREE/USER/VTREENAV/Facet/facet">
<div class="facet">
<xsl:text>facet:</xsl:text>
name: <xsl:value-of select="name"/><a href="/vtree/{name}"><xsl:value-of select="name"/></a>
hits: <xsl:value-of select="hits"/>
<xsl:apply-templates select="pic"/>
</div>
</xsl:template>

<xsl:template match="VTREE/USER/VTREENAV/Facet/facet/pic">
<div class="pic">
pid: <xsl:value-of select="pid"/>
gid: <xsl:value-of select="gid"/>
uid: <xsl:value-of select="uid"/>
<xsl:apply-templates select="pathstore_r70" mode="img1"/>
</div>
</xsl:template>





<!-- GEONAV -->

<xsl:template match="GEO/USER/GEONAV/Facet">
<div class="Facet">
<xsl:text>Facets:</xsl:text><xsl:apply-templates/>
</div>
</xsl:template>



<xsl:template match="GEO/USER/GEONAV/Facet/facet">
<div class="facet">
<xsl:text>facet:</xsl:text>
name: <a href="/geo{name}"><xsl:value-of select="name"/></a>
hits: <xsl:value-of select="hits"/>
<xsl:apply-templates select="pic"/>
</div>
</xsl:template>

<xsl:template match="GEO/USER/GEONAV/Facet/facet/pic">
<div class="pic">
pid: <xsl:value-of select="pid"/>
gid: <xsl:value-of select="gid"/>
uid: <xsl:value-of select="uid"/>
</div>
</xsl:template>









<!-- BLOGNAV -->

<xsl:template match="BLOG/USER/BLOGNAV/Facet">
<div class="Facet">
<xsl:text>Facets:</xsl:text><xsl:apply-templates/>
</div>
</xsl:template>



<xsl:template match="BLOG/USER/BLOGNAV/Facet/facet">
<div class="facet">
<xsl:text>facet:</xsl:text>
name: <a href="/blog/{name}"><xsl:value-of select="name"/></a>
hits: <xsl:value-of select="hits"/>
<xsl:apply-templates select="pic"/>
</div>
</xsl:template>

<xsl:template match="BLOG/USER/BLOGNAV/Facet/facet/pic">
<div class="pic">
pid: <xsl:value-of select="pid"/>
gid: <xsl:value-of select="gid"/>
uid: <xsl:value-of select="uid"/>
<xsl:apply-templates select="pathstore_r70" mode="img1"/>
</div>
</xsl:template>
























<!-- LOGIN -->

<!-- login2xhtml -->


<xsl:template match="login" mode="rw">
<div class="login">
<form action="{../../../request/url}" method="post"><!-- /login -->

<div class="username">
<label class="username" for="username">username</label>
<input name="username" id="username" value="{username}"/>
</div>

<div class="password">
<label class="password" for="password">password</label>
<input name="password" id="password" value="{password}" type="password"/>
</div>

<input type="submit"/> 

[<a href="/forgot">I forgot my password</a> |
<a href="/user/post">Open an account, Free</a>]

</form>
</div>
</xsl:template>



<xsl:template match="forgot">
<div class="forgot">
<xsl:apply-templates />
</div>
</xsl:template>

<xsl:template match="forgot/sentok">
An email has been sent to the email address we have in our records for you.
Please follow the instructions in that mail to reset your password.
</xsl:template>

<xsl:template match="forgot/sentfailed">
Failure to send email. Please contact Support.
</xsl:template>


<xsl:template match="forgot" mode="rw">
<div class="forgot">
I do not remember my password, but I remember
<form action="{../../../request/url}" method="post">
<select name="fieldname">
<option value="id">my UID</option>
<option value="_email">my email address</option>
<option value="_servershort">my DNS uname</option>
</select>
<br/>
and its value is:
<input name="fieldvalue"/>""")
    xsl.append(protect_with_captcha(dotcom))
    xsl.append(b"""<input type="submit"/>
</form>
</div>
</xsl:template>



<xsl:template match="component/get/post/reset" mode="rw">
<div class="reset">
You are now temporarly authenticated. <br/>
You can manage your account and in particular change your password.
<a href="/user/{/response/authentication/uid}/put">password management</a>
</div>
</xsl:template>



<!-- template to split by slash -->
 <xsl:template name="split1">
  <xsl:param name="pText" select="."/>
  <xsl:if test="string-length($pText)>0">
pText=<xsl:value-of select="$pText"/>
   BEFORE<xsl:value-of select="substring-before(concat($pText,'/'),'/')"/>XXX<br/>
   <xsl:call-template name="split">
    <xsl:with-param name="pText" select="substring-after($pText, '/')"/>
   </xsl:call-template>
  </xsl:if>
</xsl:template>



<!-- template to split by slash -->
 <xsl:template name="split">
  <xsl:param name="pText"/>
  <xsl:param name="path"/>
  <xsl:param name="separator"/>
  <xsl:if test="string-length($pText)>0">

<!--
pText=<xsl:value-of select="$pText"/>
diff1=<xsl:value-of select="substring-before($path,$pText)"/>
diff2=<xsl:value-of select="substring-before(concat($pText,'/'),'/')"/>
diff3=<xsl:value-of select="concat(substring-before($path,$pText),substring-before(concat($pText,'/'),'/'))"/><br/> -->

<xsl:value-of select="$separator"/>
<a href="/wiki{concat(substring-before($path,$pText),substring-before(concat($pText,'/'),'/'))}">
<xsl:if test="string-length(substring-before(concat($pText,'/'),'/'))=0">wiki home</xsl:if>
<xsl:value-of select="substring-before(concat($pText,'/'),'/')"/>
</a>

   <xsl:call-template name="split">
    <xsl:with-param name="pText" select="substring-after($pText, '/')"/>
    <xsl:with-param name="path" select="$path"/>
    <xsl:with-param name="separator" select="'/'"/>
   </xsl:call-template>
  </xsl:if>
</xsl:template>





</xsl:stylesheet>

""")
    return b''.join(xsl)


if __name__ == "__main__":
    xsl=xml2xhtml("xhtml",{})
    print(xsl.decode('utf8'))
    f=open('alll.xsl','wb')
    f.write(xsl)
    f.close()
    pass
