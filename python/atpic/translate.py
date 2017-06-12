"""Translate functions"""

from lxml import etree
import io

import atpic.log
# import logging



xx=atpic.log.setmod("INFO","translate")

def extract_id(xml_bytes):
    """This returns a dictionnary of Phrase ID and Phrase in English
    Input is a XML string with some <t id="">bbbbb</t>"""
    
    xml_doc = etree.parse(io.BytesIO(xml_bytes))

    print(dir(xml_doc))
    res=xml_doc.findall('.//t') # all <t> tags
    print(res[0])
    print(dir(res))
    adict={}

    for i in range(0,len(res)):
        ele=res[i]
        print(dir(ele))
        tid=ele.get(b'id')
        tid=tid.encode('utf8')
        # print('i=',i,res[i])
        # print(dir(res[i]))
        # print('tag',res[i].tag)
        # print('text',res[i].text)
        # print('text',res[i].items())
        # ss=etree.tostring(res[i])
        # print(ss)
        sss=ele.text.encode('utf8') # take the node's text
        sss=sss+b''.join(etree.tostring(child) for child in ele.iterdescendants()) # appedn what is inside
        print(i,tid,sss)
        adict[tid]=sss
    print('will return',adict)
    return adict
