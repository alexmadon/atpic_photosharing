#!/usr/bin/python3

# apt-get install python3-docutils
# use python reStructuredText format

import docutils.nodes
import docutils.parsers.rst.roles
import docutils.core

import docutils.writers.html4css1


import atpic.log



xx=atpic.log.setmod("INFO","wiki_section")
# edit sections alawikipedia/mediawiki
# http://www.arnebrodowski.de/blog/write-your-own-restructuredtext-writer.html



from docutils.writers import html4css1



class MyVisitor(docutils.nodes.NodeVisitor):
    def __init__(self,document):
        docutils.nodes.NodeVisitor.__init__(self,document)
        # self.document.endline=0

    def  dispatch_visit(self,node):
        yy=atpic.log.setname(xx,'dispatch_visit')
        nb=node.line
        if nb:
            self.document.endline=nb
        atpic.log.debug(yy,'555555LINE',node.line,node)
        atpic.log.debug(yy,'6666666LINE',type(node))
        if nb:
            atpic.log.debug(yy,'77777LINE',self.document.endline)
        elif isinstance(node,docutils.nodes.Text):
            atpic.log.debug(yy,'88888LINE',dir(node))
            lines=node.splitlines()
            self.document.endline=self.document.endline+len(lines)
            atpic.log.debug(yy,'99999LINE',self.document.endline)


class MyHTMLTranslator(docutils.writers.html4css1.HTMLTranslator):
    """
    This is a translator class for the docutils system.
    It will produce a minimal set of html output.
    (No extry divs, classes oder ids.)
    
    """
    # http://docutils.sourceforge.net/docutils/writers/html4css1/__init__.py

    def visit_title(self,node):
        yy=atpic.log.setname(xx,'visit_title')
        # if node.line:
        if isinstance(node.parent, docutils.nodes.section):
            h_level = self.section_level + self.initial_header_level - 1
            self.body.append('<div class="wikiheader levelh%s">\n'% h_level)
        docutils.writers.html4css1.HTMLTranslator.visit_title(self,node)



    def depart_title(self,node):
        yy=atpic.log.setname(xx,'visit_title')
        docutils.writers.html4css1.HTMLTranslator.depart_title(self,node)

        atpic.log.debug(yy,"node.line",node.line,node)
        atpic.log.debug(yy,'dir(node)',dir(node))
        atpic.log.debug(yy,'node.list_attributes',node.list_attributes)
        atpic.log.debug(yy,"node.parent",node.parent)
        atpic.log.debug(yy,"node.rawsource",node.rawsource)

        # if node.line:
        if isinstance(node.parent, docutils.nodes.section):


            node.parent.walk(MyVisitor(node.document))
            atpic.log.debug(yy,'EEEELINE',node.document.endline)
            fromline=node.line - 1
            toline=node.document.endline-1
            # self.body.append('<a>Edit</a>\n') 

            # on h1,h2,h3,h4: style="display:inline"
            if self.settings.atpic_editlinks:
                # presentation layer:
                # edit button is made invisible using CSS
                self.body.append('<a href="/wiki'+self.settings.atpic_wikipage+'/_post?lines='+str(fromline)+'-'+str(toline)+'" class="editlines">Edit</a>\n')

            self.body.append('</div>\n')


class MyHTMLWriter(docutils.writers.html4css1.Writer):
    """
    This docutils writer will use the MyHTMLTranslator class below.
    
    """
    def __init__(self):
        yy=atpic.log.setname(xx,'MyHTMLWriter.__init__')
        html4css1.Writer.__init__(self)
        self.translator_class = MyHTMLTranslator
        atpic.log.debug(yy,'DDDD Writer',dir(self))
        atpic.log.debug(yy,'DDDD Writer',self.visitor_attributes)
        atpic.log.debug(yy,'DDDD Writer',self.settings_spec)



def convert(text,wikipage,editlinks):
    parts = docutils.core.publish_parts(text, 
                                        writer=MyHTMLWriter(),
                                        settings_overrides=
                                        { 'stylesheet_path': None,
                                          'link-stylesheet': False,
                                          'embed_stylesheet': False,
                                          'atpic_editlinks':editlinks,
                                          'atpic_wikipage':wikipage,})

    
    return parts['html_body']






def print_lines(text):
    i=1
    lines=text.splitlines()
    for line in lines:
        print(i,line)
        i=i+1

if __name__ == "__main__":
    text=b"""
.. contents:: TOC

Title1
======
Subtitle
--------
some *bold* text.

1) one
2) two

paragraph

Subsection2
-----------

Anothersection
"""

    text="""

.. contents:: TOC

hi
==
SOMEHI

ho
==
*bold*

subsec
======

hello
line2
line3
line4
line5

line7
line8
line9
line10
line11
"""

    print_lines(text)
    print(convert(text,'wikipage',True))
