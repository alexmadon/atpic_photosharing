#!/usr/bin/python3
# py3k version: Problem: tidy does exist?
"""
http://docs.python.org/lib/module-HTMLParser.html
http://docs.python.org/lib/module-sgmllib.html
http://utidylib.berlios.de/
http://tidy.sourceforge.net/docs/quickref.html



Low level package:

do not use directly except when writing the "clean.py"

"""
import traceback
from html.parser import HTMLParser
# from sgmllib import SGMLParser as HTMLParser
from html import escape
import atpic.tidy3k as tidy
from urllib.parse import urlparse
# from html.entities import entitydefs
import html.entities
import re
# import re
# import logging
import atpic.log

xx=atpic.log.setmod("INFO","cleaner_alex")

def html2xml(html):
    """
    This transforms a HTML soup to clean XML.
    http://tidy.sourceforge.net/docs/quickref.html
    """
    options = {
        b"output-xhtml":b"1", 
        b"output-xml":b"1", 
        b"add-xml-decl":b"0", 
        b"indent":b"0", 
        b"tidy-mark":b"0",
        b"wrap":b"0",
        b"markup":b"1",
        b"show-body-only":b"1", 
        b"quote-nbsp":b"0", # do not want to show &nbsp; but rather b'\xc2\xa0'
        b"quote-ampersand":b"1",
        b"escape-cdata":b"1",
        b"input-encoding":b"utf8", 
        b"output-encoding":b"utf8"
        }
    xml=tidy.parseString(html,options)
    # print("XXXXXX",xml)
    return xml

def clean(input):
    """
    transforms a soup to a secure XML calling
    1) tidy
    2) HTML cleaner 
    3) tidy
    """
    yy=atpic.log.setname(xx,'clean')
    atpic.log.debug(yy,'input=',input)
    parser=MyCleaner()
    # print "INPUT: %s" % input
    # ####input=html2xml(input)
    # print "CLEANED 1: %s" % input
    try:
        input=parser.clean(input)
    except:
        atpic.log.debug(yy,'very bad error!')
        input=b"" #if the sgml parser fails then this is very bad input, reset it
        atpic.log.error(yy,traceback.format_exc())

    atpic.log.debug(yy,"CLEANED 2:",input)
    input=html2xml(input)
    atpic.log.debug(yy,"CLEANED 3:",input)
    return input










class MyCleaner(HTMLParser):
    """This removes unwanted tags.
    It should avoid XSS by removing javascript.
    Output is HTML (should be transformed to XML) """
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = []
        self.open_tags = []
        # A list of the only tags allowed.  Be careful adding to this.  Adding
        # "script," for example, would not be smart.  'img' is out by default 
        # because of the danger of IMG embedded commands, and/or web bugs.
        self.permitted_tags = ['a','img','b','br','hr','div','p','span']
        # you NEED to list all the possible attributes for all the permitted tags
        # use an empty list if necessary
        self.permitted_attributes = \
            {'a':['href','title'],
             'img':['src','alt'],
             'b':[],
             'br':[],
             'hr':[],
             'div':[],
             'p':[],
             'span':[],

            }
        self.permitted_schemes = ['http','https','ftp']


    def handle_starttag(self, tag, attrs):
        # print "Encountered the beginning of a %s tag" % tag
        if tag in self.permitted_tags:
            if tag != 'br': # distinguish BR as tidy will double it if seeing <br></br>
                self.result.append("<%s" % tag)
                for attr,value in attrs:
                    # print "    attribute %s=%s" % (attr,value)
                    if attr in self.permitted_attributes[tag]:
                        if attr in ['href', 'src', 'background']:
                            if self.url_is_acceptable(value):
                                self.result.append(' %s="%s"' % (attr,value))
                        else:    
                            self.result.append(' %s="%s"' % (attr,value))
                self.result.append(">")
            else:
                self.result.append("<br />")
            
        # else:
            # print "NO %s" % tag


    def handle_endtag(self, tag):
        # print "Encountered the end of a %s tag" % tag
        if tag in self.permitted_tags:
            if tag != 'br':
                newresult="</%s>" % tag
                self.result.append(newresult)
                        

    def handle_data(self,data):
        # print "data is: %s" %data
        self.result.append(self.xssescape(data))


    def handle_charref(self, ref):
        if len(ref) < 7 and ref.isdigit():
            self.result += '&#%s;' % ref
        else:
            self.result += self.xssescape('&#%s' % ref)
    def handle_entityref(self, ref):
        # print('handling entity',ref)
        # codepoint=html.entities.name2codepoint[ref]
        # print('codepoint',codepoint)
        # self.result += chr(codepoint) #.encode('utf8')
        # print(self.result)
        
        if ref in html.entities.entitydefs:
            self.result += '&%s;' % ref
        else:
            self.result += self.xssescape('&%s' % ref)
           
    def handle_comment(self, comment):
        if comment:
            self.result += self.xssescape("<!--%s-->" % comment)


    def xssescape(self,text):
        """Gets rid of < and > and &"""
        return escape(text, quote=True)

    def url_is_acceptable(self,url):
        ### Requires all URLs to be "absolute."
        parsed = urlparse(url)
        # print parsed
        return parsed[0] in self.permitted_schemes and '.' in parsed[1]

    def clean(self,input):
        # print "DOING: %s" % input
        input=input.decode('utf8')
        self.feed(input)
        result1="".join(self.result)
        # print"RESULT1= %s" % result1
        result1=result1.encode('utf8')
        return result1















# ==========================================
# TXT
# ==========================================

def html2txt(html):
    """
    This transforms a HTML soup to clean TXT.
    http://tidy.sourceforge.net/docs/quickref.html
    """
    options = {
        b"output-xhtml":b"1", 
        b"output-xml":b"1", 
        b"add-xml-decl":b"0", 
        b"indent":b"0", 
        b"tidy-mark":b"0",
        b"wrap":b"0",
        b"show-body-only":b"1", 
        b"quote-ampersand":b"1",
        b"escape-cdata":b"1",
        b"input-encoding":b"utf8", 
        b"output-encoding":b"utf8",
        b"quote-nbsp":b"1",
        b"quote-marks":b"1"
        }
    xml=tidy.parseString(html, options)
    # print("YYYY",xml)
    return xml


def txtclean(input):
    """
    transforms a soup to a secure XML calling
    1) tidy
    2) HTML cleaner 
    3) tidy
    """
    parser=MyTextCleaner()
    # print("INPUT: %s" % input)
    # ####input=html2xml(input)
    # print "CLEANED 1: %s" % input
    try:
        input=parser.clean(input)
    except:
        input="" #if the sgml parser fails then this is very bad input, reset it
    # print ("CLEANED 2: %s" % input)
    # input=html2xml(input)
    # print "CLEANED 3: %s" % input
    input=html2txt(input)
    # print("CLEANED 3: %s" % input)
    p = re.compile(b'&nbsp;',re.IGNORECASE)
    input=p.sub(b' ',input)
    # print("CLEANED 4:",input)
    return input



class MyTextCleaner(HTMLParser):
    """
    This removes unwanted tags.
    It should avoid XSS by removing javascript.
    Output is HTML (should be transformed to XML) 
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = []
        self.open_tags = []

    def handle_starttag(self, tag, attrs):
        # print "Encountered the start of a %s tag" % tag
        pass

    def handle_endtag(self, tag):
        # print "Encountered the end of a %s tag" % tag
        pass                        

    def handle_data(self,data):
        # print "data is: %s" %data
        self.result.append(self.xssescape(data))


    def handle_charref(self, ref):
        if len(ref) < 7 and ref.isdigit():
            self.result += '&#%s;' % ref
        else:
            self.result += self.xssescape('&#%s' % ref)

    def handle_entityref(self, ref):
        if ref in html.entities.entitydefs:
            self.result += '&%s;' % ref
        else:
            self.result += self.xssescape('&%s' % ref)

    def handle_comment(self, comment):
        pass
    # if comment:
    #        self.result += xssescape("<!--%s-->" % comment)


    def xssescape(self,text):
        """Gets rid of < and > and &"""
        return escape(text, quote=True)

    def url_is_acceptable(self,url):
        ### Requires all URLs to be "absolute."
        parsed = urlparse(url)
        # print parsed
        return parsed[0] in self.permitted_schemes and '.' in parsed[1]

    def clean(self,input):
        # print "DOING: %s" % input
        input=input.decode('utf8')
        self.feed(input)
        result1="".join(self.result)
        # print"RESULT1= %s" % result1
        result1=result1.encode('utf8')
        return result1










if __name__ == "__main__":
    parser=MyCleaner()
    test=b"""<a href=http://atpic.com non=element>ATPIC</a> <b>Alex & Dama</b><!-- comment --><img src=tot.gif> alex<i>ff</i>"""
    # test="""<b>bold<a>it</b></a>"""
    # print html2xml(test)
    # print parser.clean(test)
    print(parser.clean(test))

    parser=MyTextCleaner()
    print(parser.clean(test))
