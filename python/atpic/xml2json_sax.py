#!/usr/bin/python3
# look at:
# https://github.com/hay/xml2json/blob/master/xml2json.py

import xml.sax
from io import BytesIO
import json # to validate
import io

from lxml import etree


import atpic.log
xx=atpic.log.setmod("INFO","xml2json_sax")

def is_collection(atag):
    collection=False
    if len(atag)==1:
        collection=False
    else:
        if atag[0:1].upper()==atag[0:1] and atag[1:2].upper()!=atag[1:2]:
            collection=True
        elif atag[0:1].upper()!=atag[0:1] and atag[1:2].upper()==atag[1:2]:
            collection=True
    if atag==b'pathinfo':
        collection=True

    return collection

def get_current(name):
    if is_collection(name):
        (ctype,cvalue,ccount)=(b'collection',name,0) 
    else:
        (ctype,cvalue,ccount)=(b'entry',name,0)
    return (ctype,cvalue,ccount)

def myprint(*args):
    print(*args)
    pass

def xml2json(xmlstring):
    yy=atpic.log.setname(xx,'xml2json')
    class ABContentHandler(xml.sax.ContentHandler):
        def __init__(self):
            xml.sax.ContentHandler.__init__(self)
            self.json=[]
            self.stacktype=[(b'entry',b'dummy',0)]

        def startElement(self, name, attrs):
            atpic.log.debug(yy,"startElement '" + name + "'")
            name=name.encode('utf8')
            (ctype,cvalue,ccount)=get_current(name)
            (ptype,pvalue,pcount)=self.stacktype.pop()
            if ctype==b'entry':
                if ptype==b'collection':
                    pcount=pcount+1
            self.stacktype.append((ptype,pvalue,pcount))
            self.stacktype.append((ctype,cvalue,ccount))
            myprint('stacktype1=',self.stacktype)
            myprint('1111',(ctype,cvalue,ccount),(ptype,pvalue,pcount))
            if ctype==b'entry':
                if ptype==b'collection':
                    if pvalue==b'pathinfo':
                        self.json.append(b'{"'+cvalue+b'":')
                else:
                    if pvalue!=cvalue:
                        self.json.append(b'{"'+cvalue+b'":')
            else:
                self.json.append(b'{"'+cvalue+b'":[')
            myprint('1111',b''.join(self.json))

        def endElement(self, name):
            myprint('2222',self.stacktype) 
            name=name.encode('utf8')
            atpic.log.debug(yy,"endElement", name)
            (ctype,cvalue,ccount)=get_current(name)
            (ptype,pvalue,pcount)=self.stacktype.pop()
            if ptype==b'char':
                (pptype,ppvalue,ppcount)=self.stacktype.pop()
            last=self.json.pop()
            self.json.append(last)
            lastchar=last[-1:]    
            myprint('2222 lastchar',last,lastchar)
 
            if ptype==b'char':
                self.json.append(b'"'+pvalue+b'"')
            elif ptype==b'entry':
                if lastchar==b':':
                    self.json.append(b'null')
            if ctype==b'entry':
                if ptype==b'char':
                    if pptype==b'entry':
                        self.json.append(b'}X')
                    else:
                        self.json.append(b'}Y')

                else:
                    if ptype==b'entry':
                        self.json.append(b'}Z')
                    else:
                        self.json.append(b'}T')
                
            else:
                self.json.append(b']')

            myprint('2222',b''.join(self.json))
 

        def characters(self, content):
            content=content.encode('utf8')
            atpic.log.debug(yy,"characters",content)
            (ptype,pvalue,pcount)=self.stacktype.pop()
            if ptype==b'char':
                self.stacktype.append((ptype,pvalue+content,0))
            else:
                self.stacktype.append((ptype,pvalue,0))
                self.stacktype.append((b'char',content,0))
            # self.jsonl.append('"'+content+'"')
            myprint('stacktype3=',self.stacktype) 

    xmlstring=BytesIO(xmlstring) # .decode('utf8') ) 
    ch=ABContentHandler()
    xml.sax.parse(xmlstring,ch)
    json=b''.join(ch.json)
    myprint('stacktype=',ch.stacktype) 
    return json



def xml2json2(xml_string):
    xml_doc=etree.parse(io.BytesIO(xml_string))
    print(xml_doc)
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
        b'<doc><pathinfo><f>xml</f><f>json</f><q>paris</q></pathinfo></doc>',
        b'<doc><ok><Pic><pic><id>1</id></pic><pic><id>2</id></pic></Pic></ok></doc>',
        b'<doc><tag/><a>alex</a></doc>',
        ]



    for axml in xmls:
        print('+++++++++++++++++++++++++++')
        print(axml)
        ajson=xml2json2(axml)
        print(ajson)
        # ajson2=json.loads(ajson.decode('utf8'))
        # print(ajson2)
    print(is_collection(b'aa'))
    print(is_collection(b'Aa'))
    print(is_collection(b'f'))
