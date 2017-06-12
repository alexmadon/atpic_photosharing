#!/usr/bin/python3
# apt-get install python3-markdown

# a wiki in nosql solr??
# one document code=is markdown code
#  links=[]
#  broken_links=[] to get the redlinks, and the what links to there
# older versions in GIT?

# wiki parsing could be done with: pyparsing eve if it is not a formal grammar
#
# http://pyparsing.wikispaces.com/file/view/simpleWiki.py/30268307/simpleWiki.py

# in C:
# http://www.pell.portland.or.us/~orc/Code/discount/
#  apt-cache search markdown| grep lib
# libmarkdown2 - implementation of the Markdown markup language in C (library)
# libmarkdown2-dbg - implementation of Markdown markup language in C (debug)
# libmarkdown2-dev - implementation of the Markdown markup language in C (dev files)
# discount - implementation of the Markdown markup language in C
# man mkd-callbacks
# more /usr/include/x86_64-linux-gnu/mkdio.h
# http://pydoc.net/Python/discount/0.2.0BETA/discount.libmarkdown/


# pandoc -f mediawiki test.mdwn 
# https://github.com/toyvo/libpandoc
# get list of links: http://johnmacfarlane.net/pandoc/scripting.html

# https://github.com/erezsh/plyplus

import markdown


content = """
[TOC]

Chapter
=======

Section
-------

* Item 1
* Item 2

[[Google]]

http://atpic.com

this is a link: [google](http://google.com)

"""
# http://daringfireball.net/projects/markdown/syntax
# http://svn.saurik.com/repos/menes/trunk/wikicyte/library/markdown/extensions/wikilinks.py

print(markdown.markdown(content))
print(markdown.markdown(content,['wikilinks']))
print(markdown.markdown(content,['wikilinks(base_url=/wiki/,end_url=.html,html_class=foo)']))
print('++++++++++++++++++++++++++')
print(markdown.markdown(content,['wikilinks','toc']))
# http://pythonhosted.org/Markdown/extensions/wikilinks.html




# http://stackoverflow.com/questions/5930542/check-image-urls-using-python-markdown
# https://github.com/trentm/python-markdown2
import markdown.inlinepatterns

class MyLinkPattern(markdown.inlinepatterns.LinkPattern):
    def handleMatch(self, m):
        node = markdown.inlinepatterns.LinkPattern.handleMatch(self, m)
        href = node.attrib.get('href')
        print("MMMMMMMMMMMMMMMMMMMMMatch",href)
        return node

mk = markdown.Markdown()
# patch in the customized image pattern matcher with url checking
mk.inlinePatterns['link'] = MyLinkPattern(markdown.inlinepatterns.LINK_RE, mk)
result = mk.convert("som [API](url) links and [[Boobo]]")
print(result)
