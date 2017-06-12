#!/usr/bin/python3
# https://github.com/erikrose/parsimonious
# https://github.com/CUGC/wiki/blob/master/resources/mediawiki/mediawiki.jqueryMsg.peg

from parsimonious.grammar import Grammar
import parsimonious.nodes
import time

import atpic.xsl


class HtmlFormatter(parsimonious.nodes.NodeVisitor):
    """Visitor that turns a parse tree into HTML fragments"""
    """
    * check liststatus set inlist1
    ** set inlist2
    ** set inlist2
    """
    line_bullets=[]
    previousline_bullets=[]


    def display_custom_list_open(self):
        # called before listitem to know if we need to start a <ul> or <ol>
        tag_before=''
        tag_after=''
        # copy into a working copy 
        line_bullets=self.line_bullets
        previousline_bullets=self.previousline_bullets

        line_bullets_len=len(line_bullets)
        previousline_bullets_len=len(previousline_bullets)
        if line_bullets_len > previousline_bullets_len:
            for i in range(previousline_bullets_len,line_bullets_len):
                last=line_bullets.pop()
                line_bullets.append(last)
                if last=='uli':
                    tag_before+='<ul>\n'
                else:
                    tag_before+='<ol>\n'
        # out='OPEN:'+tag_before+'C'+str(self.line_bullets)+'P'+str(self.previousline_bullets)
        out= tag_before
        return out
 

    def display_custom_list_close(self):
        # called after new lines to know if we need to close a </ul> or </ul>
        tag_before=''
        tag_after=''
        # copy into a working copy 
        line_bullets=self.line_bullets
        previousline_bullets=self.previousline_bullets

        line_bullets_len=len(line_bullets)
        previousline_bullets_len=len(previousline_bullets)
        if line_bullets_len < previousline_bullets_len:
            for i in range(line_bullets_len,previousline_bullets_len):
                last=previousline_bullets.pop()
                previousline_bullets.append(last)
                if last=='uli':
                    tag_after+='\n</ul>'
                else:
                    tag_after+='\n</ol>'
        # out='CLOSE:'+tag_after+'C'+str(self.line_bullets)+'P'+str(self.previousline_bullets)
        out = tag_after
        return out
        

    def list_reset(self):
        self.previousline_bullets=self.line_bullets
        self.line_bullets=[]
        return ''

    def visit_line(self, node, visited_children):
        # return self.display_custom_list_after(node, visited_children)
        return self.display_custom_list_close()+self.display_custom_list_open()+''.join(visited_children)+self.list_reset()

    def visit_inline(self, node, visited_children):
        return 'line:'+''.join(visited_children)
    def visit_listline(self, node, visited_children):
        return '<listline>'+''.join(visited_children)+'</listline>'

    def visit_lineorend(self, node, visited_children):
        return ''.join(visited_children)
    def visit_end(self, node, visited_children):
        return ''.join(visited_children)
    def visit_listitem(self, node, visited_children):
        # return 'listitem:'+''.join(visited_children)
        return '<listitem>'+''.join(visited_children)+'</listitem>'
    def visit_empty(self, node, visited_children):
        return 'empty:'
    def visit_linecontent(self, node, visited_children):
        # return 'linecontent:('+node.text+')'
        return node.text
    def visit_newline(self, node, visited_children):
        return '\n' # .join(visited_children)+'NNN\n'

    def visit_doublenewline(self, node, visited_children):
        return self.display_custom_list_close()+self.list_reset()+'<br/>\n'
    def visit_star(self, node, visited_children):
        # return 'star:'
        return ''
    def visit_bullets(self, node, visited_children):
        # return 'bullets:'+''.join(visited_children)
        return ''.join(visited_children)
    def visit_bullet(self, node, visited_children):
        # return 'bullet:'+''.join(visited_children)
        return ''.join(visited_children)
    def visit_olbullet(self, node, visited_children):
        self.line_bullets.append('oli')
        return '<olbullet/>'
    def visit_ulbullet(self, node, visited_children):
        self.line_bullets.append('uli')
        return '<ulbullet/>'

    def visit_whitespace(self, node, visited_children):
        # return 'whitespace:'+''.join(visited_children)
        return " "
    def visit_ignorewhitespace(self, node, visited_children):
        return ""
    def visit_document(self, node, visited_children):
        return '<document>\n'+''.join(visited_children)+'</document>'
    
        
    def visit_format_marker1(self, node, visited_children):
        # return 'format_marker1:'+''.join(visited_children)
        return ''
    def visit_format_marker2(self, node, visited_children):
        # return 'format_marker1:'+''.join(visited_children)
        return ''
    def visit_format_marker3(self, node, visited_children):
        # return 'format_marker1:'+''.join(visited_children)
        return ''
    def visit_formatted(self, node, visited_children):
        # return 'formatted:'+''.join(visited_children)
        return node.text
    def visit_formatting(self, node, visited_children):
        # return 'formatting:'+''.join(visited_children)
        return ''.join(visited_children)
    
    def visit_format1(self, node, visited_children):
        return '<format1>'+''.join(visited_children)+'</format1>'
    def visit_format2(self, node, visited_children):
        return '<format2>'+''.join(visited_children)+'</format2>'
    def visit_format3(self, node, visited_children):
        return '<format3>'+''.join(visited_children)+'</format3>'
    
    def visit_header1_mark(self, node, visited_children):
        # return 'header1_mark:'+''.join(visited_children)
        return ''.join(visited_children)
    def visit_header2_mark(self, node, visited_children):
        # return 'header2_mark:'+''.join(visited_children)
        return ''.join(visited_children)
    def visit_header3_mark(self, node, visited_children):
        # return 'header3_mark:'+''.join(visited_children)
        return ''.join(visited_children)
    def visit_header4_mark(self, node, visited_children):
        # return 'header4_mark:'+''.join(visited_children)
        return ''.join(visited_children)
    def visit_title(self, node, visited_children):
        # return 'title:'+''.join(visited_children)
        return node.text
    def visit_header1(self, node, visited_children):
        return '<h1>'+''.join(visited_children)+'</h1>'
    def visit_header2(self, node, visited_children):
        return '<h2>'+''.join(visited_children)+'</h2>'
    def visit_header3(self, node, visited_children):
        return '<h3>'+''.join(visited_children)+'</h3>'
    def visit_header4(self, node, visited_children):
        return '<h4>'+''.join(visited_children)+'</h4>'
    def visit_header(self, node, visited_children):
        return '<header>'+''.join(visited_children)+'</header>'
    
    
    def visit_link_start(self, node, visited_children):
        # return 'link_start:'+''.join(visited_children)
        return ''.join(visited_children)
    def visit_link_end(self, node, visited_children):
        #return 'link_end:'+''.join(visited_children)
        return ''.join(visited_children)
    def visit_link_ref(self, node, visited_children):
        return 'link_ref:'+''.join(visited_children)
    def visit_link_description(self, node, visited_children):
        return 'link_description:'+''.join(visited_children)
    def visit_link_content(self, node, visited_children):
        return 'link_content:'+''.join(visited_children)
    def visit_link(self, node, visited_children):
        return '<link>'+''.join(visited_children)+'</link>'
    def visit_link1(self, node, visited_children):
        return 'link1:'+''.join(visited_children)
    def visit_link2(self, node, visited_children):
        return '<link2>'+''.join(visited_children)+'</link2>'
    def visit_link_element(self, node, visited_children):
        # return 'link_element:'+''.join(visited_children)
        return '<link_element>'+node.text+'</link_element>'
        
    def visit_link_url(self, node, visited_children):
        return '<link_url>'+''.join(visited_children)+'</link_url>'
    
    def visit_link_url_file_pattern(self, node, visited_children):
        # return '<link_url_file_pattern>'+''.join(visited_children)+'</link_url_file_pattern>'
        return ''
    def visit_link_url_filename(self, node, visited_children):
        return '<link_url_filename>'+''.join(visited_children)+'</link_url_filename>'
    def visit_link_url_file(self, node, visited_children):
        return '<link_url_file>'+''.join(visited_children)+'</link_url_file>'
    
    
    def visit_(self, node, visited_children):
        return ''+''.join(visited_children)
    def visit_verticalbar(self, node, visited_children):
        return '<verticalbar/>'
    def visit_link_url_internal(self, node, visited_children):
        return 'link_url_internal:'+''.join(visited_children)
    
    
    def visit_digit(self, node, visited_children):
        return ''.join(visited_children)
    # def visit_(self, node, visited_children):
    #     return ''.join(visited_children)


def convert(wikitext):

    # read the grammer PEG file
    f=open("wiki1.peg")    
    peg=f.read()
    f.close()
    
    start = time.clock()
    grammar = Grammar(peg)
    elapsed1 = time.clock() - start

    print("+++++++++grammar+++++++++")
    print(peg)
    print("+++++++++input+++++++++")
    print(atext.decode('utf8'))
    print('*********************')
    start = time.clock()
    parsed=grammar.parse(atext.decode('utf8'))
    elapsed2 = time.clock() - start
    print(dir(parsed))
    print(parsed)
    start = time.clock()
    result = HtmlFormatter().visit(parsed)
    elapsed3 = time.clock() - start


    print("timeto create grammar:",elapsed1)
    print("timeto parse text:",elapsed2)
    print("timeto convert to xml:",elapsed3)

    return result.encode('utf8')


def convert2html(xml_string):

    xslt_string=b"""
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="document">
<html><xsl:apply-templates/></html>
</xsl:template>


<xsl:template match="h1">
<h1><xsl:apply-templates/></h1>
</xsl:template>

<xsl:template match="h2">
<h2><xsl:apply-templates/></h2>
</xsl:template>

<xsl:template match="h3">
<h3><xsl:apply-templates/></h3>
</xsl:template>

<xsl:template match="h4">
<h4><xsl:apply-templates/></h4>
</xsl:template>



<xsl:template match="ol">
<ol><xsl:apply-templates/></ol>
</xsl:template>


<xsl:template match="ul">
<ul><xsl:apply-templates/></ul>
</xsl:template>

<xsl:template match="listitem">
<li><xsl:apply-templates/></li>
</xsl:template>


<xsl:template match="format2">
<i><xsl:apply-templates/></i>
</xsl:template>


<xsl:template match="format3">
<b><xsl:apply-templates/></b>
</xsl:template>

<xsl:template match="br">
<br/>
</xsl:template>


<xsl:template match="link/link_url/link_element">
<a href="{.}"><xsl:value-of select="."/></a>
</xsl:template>


<xsl:template match="link/link2">
<a href="{link_url/link_element}"><xsl:value-of select="link_element"/></a>
</xsl:template>

<xsl:template match="link/link_url/link_url_file">
<a href="{link_element}"><img src="{link_element}?stream=true"/></a>
</xsl:template>

</xsl:stylesheet>
"""
    start = time.clock()
    result=atpic.xsl.mytrans_xslstring_xmlstring(xslt_string,xml_string)
    elapsed = time.clock() - start

    print("timeto convert to xml2:",elapsed)
    return result

if __name__ == "__main__":
    
    atext=b"""= some title =
== some subtitle ==

some [[wiki]] page

* uno a=b
* dos ''bolded''
** tres
** quatro
* cinco

some para

* one
* two
* three

some [[!File:image.png]]
see [[mypage]]
finally [[yourpage|nice your page]]
some 'bold' and not
some ''bold two'' and not
some '''bold three''' and not
external go to http://google.com 
1. un
2. deux
3. trois

la fin!
* one
* two
the end
"""
    newtext=convert(atext)
    print('+++++++++++++++++++++++++++++++++++++++++++++++++')
    print(newtext.decode('utf8'))
    htmltext=convert2html(newtext)
    print('+++++++++++++++++++++++++++++++++++++++++++++++++')
    print(htmltext.decode('utf8'))
