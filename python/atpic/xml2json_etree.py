#!/usr/bin/python3
# look at:
# https://github.com/hay/xml2json/blob/master/xml2json.py

import xml.sax
from io import BytesIO
import json # to validate
import io

from lxml import etree
from xml.dom import minidom


import atpic.log
xx=atpic.log.setmod("INFO","xml2json_etree")


def is_collection(atag):
    collection=False
    if len(atag)==1:
        collection=False
    else:
        if atag[0:1].upper()==atag[0:1] and atag[1:2].upper()!=atag[1:2]:
            collection=True
        elif atag[0:1].upper()!=atag[0:1] and atag[1:2].upper()==atag[1:2]:
            collection=True
    # if atag=='querystring':
    #     collection=True
    return collection

def is_colleclist(atag):
    # a collection, but with object names
    collection=False
    if atag=='querystring':
        collection=True
    return collection

def myprint(*args):
    # print(*args)
    pass

def is_html(tag):
    ishtml=False
    if tag in ["html","text",]:
        ishtml=True
    return ishtml

def alower(aname):
    # returns the lowercase name
    return aname.lower()

def put_true_or_null(aname):
    # json.append('true') # true or null?????
    res='null'
    if aname in ['admin','authenticated','owner','author','friend']: # useris is boolean
        res='true'
    return res

def xml2json(xml_string):
    json=[]
    def traverse2(node):
        parent=node.parentNode
        if parent.nodeType == parent.ELEMENT_NODE:
            if is_html(parent.nodeName):
                # print(dir(node))
                json.append(node.toxml())
            else:
                traverse(node)
        else:
            traverse(node)

    def identity(node):   

        json.append('"')
        for child in node.childNodes:
            json.append(child.toxml().replace('"','\\"'))
        json.append('"')
 
    def traverse(node):
        # myprint(dir(node))
        myprint('traverse',node.toxml(),'+++++++++++++++++++++')
        myprint(''.join(json))
        parent=node.parentNode
        if node.nodeType == node.TEXT_NODE:
            myprint('1')
            myprint('text:',node.nodeValue)
            json.append('"'+node.nodeValue+'"')
        if node.nodeType == node.ELEMENT_NODE:
            myprint('2')
            myprint('element:',node.nodeName)
            if parent.nodeType == node.DOCUMENT_NODE:
                myprint('3')
                json.append('{"'+alower(node.nodeName)+'":')
            if parent.nodeType == node.ELEMENT_NODE:
                myprint('4')
                if is_collection(parent.nodeName):
                    myprint('5')
                    pass
                else:
                    myprint('6')
                    if not node.previousSibling or is_colleclist(parent.nodeName):
                        myprint('7')
                        json.append('{"'+alower(node.nodeName)+'":')
                    else:
                        myprint('8')
                        json.append('"'+alower(node.nodeName)+'":')
            if is_collection(node.nodeName) or is_colleclist(node.nodeName):
                myprint('9')
                json.append('[')

        # ================================
        if node.hasChildNodes():
            i=0
            myprint('10')
            if node.nodeType == node.ELEMENT_NODE and is_html(node.nodeName):
                myprint('11')
                identity(node)
            else:
                myprint('12')
                            
                for child in node.childNodes:
                    if i>0:
                        myprint('13')
                        json.append(',')
                    traverse(child) # RECURSION!!!!!!!!!!!!!!!!
                    i=i+1
        # ================================
        myprint('12bbbbb')
        if not node.hasChildNodes() and node.nodeType != node.TEXT_NODE:
            myprint('14')
            json.append(put_true_or_null(node.nodeName))
            # json.append('true') # true or null?????
        if node.nodeType == node.DOCUMENT_NODE:
            myprint('15')
            json.append('}')
        if node.nodeType == node.ELEMENT_NODE:
            myprint('16')
            if is_collection(node.nodeName) or is_colleclist(node.nodeName):
                myprint('17')
                json.append(']')
            if is_collection(parent.nodeName):
                myprint('18')
                pass
            else:
                myprint('19')
                if not node.nextSibling or  is_colleclist(parent.nodeName):
                    myprint('20')
                    json.append('}')

    def start(xml_string):
        # xml_doc=etree.parse(io.BytesIO(xml_string))
        xmldoc = minidom.parseString(xml_string)
        # myprint(xmldoc)
        # myprint(dir(xmldoc))
        traverse(xmldoc)
        # for child in xml_doc:
        #     myprint(child.tag)

    start(xml_string)
    out=''.join(json)
    outb=out.encode('utf8')
    outb=outb.replace(b'\n',b' ')
    return outb
# restriction on XML:
# no one char tags
# no tag attributes
# lists are marked by mixed case: e.g Pic vs pic or PIC
"""
<e>text</e>                      "e": "text"
<e> <a>text</a> <a>text</a> </e> "e": { "a": ["text", "text"] }
"""

if __name__ == "__main__":
    print('hi')
    xmls=[
        b'<DD><aa>alex</aa></DD>',
        b'<Aa><aa>alex</aa><aa>madon</aa></Aa>',
        b'<ff><Aa><aa>alex</aa><aa>madon</aa></Aa></ff>',
        b'<ff><Aa><aa><gg>bob</gg></aa><aa>madon</aa></Aa></ff>',
        b'<doc><querystring><f>xml</f><f>json</f><q>paris</q></querystring></doc>',
        b'<doc><ok><Pic><pic><id>1</id></pic><pic><id>2</id></pic></Pic></ok></doc>',
        b'<doc><ok><Pic><pic><id>1</id><gid>33</gid></pic><pic><id>2</id><gid>33</gid></pic></Pic></ok></doc>',
        b'<bb><aa>alex</aa><cc>madon</cc></bb>',
        b'<doc><tag/><a>alex</a></doc>',
        b'<bb><aa>alex</aa><aa>madon</aa></bb>', # should fail?
        b'<bb><html>some <b>html</b><a href="http://code.com">code</a></html></bb>', # should fail?
        ]



    for axml in xmls:
        print('+++++++++++++++++++++++++++')
        print(axml)
        ajson=xml2json(axml)
        print(ajson)

        ajson2=json.loads(ajson.decode('utf8'))
        print(ajson2)
