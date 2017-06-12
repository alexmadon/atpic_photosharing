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
        self.document.atpic_endline=0 # we create a special document attribute
        # that stores the line noumber of the end of the section

    def  dispatch_visit(self,node):
        yy=atpic.log.setname(xx,'dispatch_visit')
        nb=node.line
        if nb:
            self.document.atpic_endline=nb
        atpic.log.debug(yy,'99999LINE',node.line,node)
        atpic.log.debug(yy,'77777LINE',self.document.atpic_endline)


class MyHTMLTranslator(docutils.writers.html4css1.HTMLTranslator):
    """
    This is a translator class for the docutils system.
    It will produce a minimal set of html output.
    (No extry divs, classes oder ids.)
    
    """
    # http://docutils.sourceforge.net/docutils/writers/html4css1/__init__.py


    def depart_title(self,node):
        yy=atpic.log.setname(xx,'visit_title')
        print('TITLE',node)
        docutils.writers.html4css1.HTMLTranslator.depart_title(self,node)

        node.parent.walk(MyVisitor(node.document))
        atpic.log.debug(yy,'EEEELINE',node.document.atpic_endline)
        fromline=node.line - 1
        toline=node.document.atpic_endline
        

        # print('VVVVV',self.settings)
        # print('VVVVV',dir(self.settings))
        
        self.body.append('<fromline>'+str(fromline)+'</fromline>\n<toline>'+str(toline)+'</toline>\n')





class MyHTMLWriter(docutils.writers.html4css1.Writer):
    """
    This docutils writer will use the MyHTMLTranslator class below.
    
    """
    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = MyHTMLTranslator



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

    text="""hi
==
SOMEHI

ho
==
*bold*

subsec
======

hello
"""

    print_lines(text)
    print(convert(text,'wikipage',False))
