#!/usr/bin/python3
import io

from lxml import etree
import re

import atpic.log
import atpic.diffalex

xx=atpic.log.setmod("INFO","wikidiff")


def postprocessing(hxplo,pxplo,actions,xmlo):
    yy=atpic.log.setname(xx,'postprocessing')
    atpic.log.debug(yy,'input=',(hxplo.list(),pxplo.list(),actions,xmlo))
    if pxplo.keys()==[b'wiki',b'revision']:
        atpic.log.debug(yy,'this is a wiki revision')
        revs=pxplo.getmatrix(1,1)
        atpic.log.debug(yy,'revs=',revs)
        if revs:
            pattern=re.compile(b'^([0-9]+),([0-9]+)$')
            b=pattern.match(revs)
            if b:
                atpic.log.debug(yy,'matched b=',b)
                xml_string=b''.join(xmlo.data.content)
                atpic.log.debug(yy,'xml_string=',xml_string)
                xml_doc = etree.parse(io.BytesIO(xml_string))
                if hxplo.keys()==[b'uname']:
                    path='/USER/Wiki/wiki'
                else:
                    path='/Wiki/wiki'
                el=xml_doc.xpath(path)
                wikitexts=[]
            
                counter=2
                for onel in el:
                    atpic.log.debug(yy,'onel',onel)
                    atpic.log.debug(yy,dir(onel))
                    wtext=onel.find('wikitext')
                    wikitext=wtext.text
                    atpic.log.debug(yy,'wtext',wtext,wikitext)
                    wikitexts.append(wikitext)
                    onel.tag="wiki"+str(counter)
                    counter=counter-1

                    """
                wikidiff=etree.Element("wikidiff")
                
                wikitext1=etree.Element("wikitext1")
                wikitext1.text=wikitexts[1]
                
                wikitext2=etree.Element("wikitext2")
                wikitext2.text=wikitexts[0]
                """
      


                diffarr=atpic.diffalex.diff_xml(wikitexts[1],wikitexts[0])
                
                
                atpic.log.debug(yy,'diffarr=',diffarr)
                atpic.log.debug(yy,'diffarr=',dir(diffarr))
                diff=etree.Element("wikitextdiff")
                
                
                for (op, data) in diffarr:
                    data = data.replace("&", "&amp;")
                    data = data.replace("<", "&lt;")
                    # data = data.replace(">", "&gt;")
                    # data = data.replace("\n", "&#182;\n")
                    # 182=para http://en.wikipedia.org/wiki/Pilcrow
                    if op == +1:
                        tag="insert"
                    elif op == -1:
                        tag="delete"
                    elif op == 0:
                        tag="equal"
                    node=etree.XML("<"+tag+">"+data+"</"+tag+">")
                    diff.append(node)
                    """
                wikidiff.append(wikitext1)
                wikidiff.append(wikitext2)
                wikidiff.append(diff)
                """
                """
                if hxplo.keys()==[b'uname']:
                    Wiki=xml_doc.find('Wiki')
                    atpic.log.debug(yy,'Wiki',Wiki)

                    Wiki.getparent().replace(Wiki,wikidiff)
                    # update the XML with what we have found
                else:
                    atpic.log.debug(yy,'replacing root element')
                    xml_doc=wikidiff
                    """


                if hxplo.keys()==[b'uname']:
                    path='/USER/Wiki'
                else:
                    path='/Wiki'
                Wiki=xml_doc.xpath(path)
                Wiki[0].append(diff)
                Wiki[0].tag="wikidiff"

                xml_string=etree.tostring(xml_doc)
                atpic.log.debug(yy,'xml_string=',xml_string)

                xmlo.data.content=[xml_string,]
                xmlo.data.stack=[]
    atpic.log.debug(yy,'output=',xmlo)

    return xmlo

if __name__ == "__main__":
    
    
    print('hi')
