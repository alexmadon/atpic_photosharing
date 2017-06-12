# import logging
import io
import urllib.parse
import re
from lxml import etree

import atpic.levenshtein
import atpic.log
import atpic.zmq_elastic_client
import atpic.jsonat_json2python


xx=atpic.log.setmod("INFO","wurflapi")


def set_wurfl_elasticsearch(essock,user_agent):
    """
    Algorithm is simple:
    1) give me your best match in elasticsearch
    2) take the best match and get its levenshtein distance:
    if too far, fallback to desktop browser
    """
    yy=atpic.log.setname(xx,'set_wurfl_elasticsearch')
    atpic.log.debug(yy,user_agent)
    # some cleansing
    user_agent2compare=user_agent # save
    user_agent=user_agent.replace(b'"',b'\"')

    query=b'{ "query" : { "match" : { "ua": "'+user_agent+b'"}},"size" : 1}'
    atpic.log.debug(yy,query)

    uri=b'/wurfl/agent/_search'
    content=atpic.zmq_elastic_client.http_general(essock,b'GET',uri,query)

    atpic.log.debug(yy,'(content)',(content))
    ajson_parsed=atpic.jsonat_json2python.parse(content)
    atpic.log.debug(yy,'++++++++++++++++')
    atpic.log.debug(yy,'ajson_parsed=',ajson_parsed[b'hits'][b'hits'][0])
    res=ajson_parsed[b'hits'][b'hits'][0][b'_source']
    uafound=res[b'ua']
    atpic.log.debug(yy,'uafound=',uafound)

    distance=atpic.levenshtein.levenshtein(user_agent2compare,uafound)
    atpic.log.debug(yy,'distance',distance)
    if distance> 15:
        atpic.log.debug(yy,'distance>15, we fallback to desktop')
        mobi=b'd'
        atpic.log.debug(yy,'compare to IE',user_agent)
        p = re.compile(b'MSIE 6\.')
        if p.search(user_agent):
            atpic.log.debug(yy,'MATCH IE')
            mime=b'html'
        else:
            mime=b'xhtml'
    else:
        atpic.log.debug(yy,'distance is small, we trust the data')
        if res[b'iw']==b'true': # is_wireless_device
            mobi=b'm'
            resol=b'|'.join([res[b'rw'],res[b'rh'],res[b'mw'],res[b'mh']]) # b'|'.join([res[b'resolution_width'],res[b'resolution_height'],res[b'max_image_width'],res[b'max_image_height']])
        else:
            mobi=b'd'
        sup=res[b'xs'] # res[b'xhtml_support_level']
        if float(sup)> 1.0:
            mime=b'xhtml'
        else:
            mime=b'html'

    ret=b'|'.join([mobi,mime])
    if mobi==b'm':
        ret=ret+b'|'+resol
        
    atpic.log.debug(yy,'ret',ret)
    # ret=b''
    return ret


def set_wurfl_solr(user_agent):
    """
    Algorithm is simple:
    1) give me your best match in Solr
    2) take the best match and get its levenshtein distance:
    if too far, fallback to desktop browser
    """
    yy=atpic.log.setname(xx,'set_wurfl_solr')
    atpic.log.debug(yy,user_agent)
    # some cleansing
    user_agent2compare=user_agent
    user_agent=user_agent.replace(b'\\',b'\\\\')
    user_agent=user_agent.replace(b':',b'\:')
    user_agent=user_agent.replace(b'[',b'\[')
    user_agent=user_agent.replace(b']',b'\]')
    user_agent=user_agent.replace(b'(',b'\(')
    user_agent=user_agent.replace(b')',b'\)')
    query=urllib.parse.urlencode([(b'q',user_agent),(b'fl',b'*,score'),(b'rows',b'1')])
    # query=b'q='+user_agent
    atpic.log.debug(yy,query)
    solr_query_url_wurfl=b"http://localhost:8984/solr/select?"+query.encode('utf8') # +user_agent

    xmldata=atpic.solr.solr_query(solr_query_url_wurfl)
    xml_string=io.BytesIO(xmldata)
    xml_doc = etree.parse(xml_string)
    els=xml_doc.xpath(b'/response/result/doc/*')
    results=[]
    matched_user_agent=b''
    score=0
    res={}
    for el in els:
        attrib=el.attrib['name'].encode('utf8')
        if attrib==b'score':
            score=float(el.text.encode('utf8'))
        if attrib==b'user_agent':
            matched_user_agent=el.text.encode('utf8')
            atpic.log.debug(yy,'matched',matched_user_agent)
        elif attrib==b'fall_back' or attrib==b'id':
            pass
        else:
            res[attrib]=el.text.encode('utf8')
        # id fall_back user_agent max_image_width max_image_height resolution_width resolution_height is_wireless_device xhtml_support_level preferred_markup score
    atpic.log.debug(yy,res)
    distance=atpic.levenshtein.levenshtein(user_agent2compare,matched_user_agent)
    print('distance',distance)
    if distance> 15:
        # we fallback to desktop
        mobi=b'd'
        atpic.log.debug(yy,'SSSS',user_agent)
        p = re.compile(b'MSIE 6\.')
        if p.search(user_agent):
            atpic.log.debug(yy,'MATCH')
            mime=b'html'
        else:
            mime=b'xhtml'
    else:
        if res[b'is_wireless_device']==b'true':
            mobi=b'm'
            resol=b'|'.join([res[b'resolution_width'],res[b'resolution_height'],res[b'max_image_width'],res[b'max_image_height']])
        else:
            mobi=b'd'
        sup=res[b'xhtml_support_level']
        if float(sup)> 1.0:
            mime=b'xhtml'
        else:
            mime=b'html'

    ret=b'|'.join([mobi,mime])
    if mobi==b'm':
        ret=ret+b'|'+resol

    return ret


def extract_mime_from_serial(serial):
    res=[]
    serial_splitted=serial.split(b'|')
    mime=serial_splitted[1]
    return mime

def parse_serial(serial):
    res={}
    serial_splitted=serial.split(b'|')
    
    if serial_splitted[0]==b'd':
        atype=b'desktop'
    else:
        atype=b'mobile'

    res[b'type']=atype
    res[b'wformat']=serial_splitted[1]
    if len(serial_splitted)>2:
        res[b'resolution_width']=serial_splitted[2]
        res[b'resolution_height']=serial_splitted[3]
        res[b'max_image_width']=serial_splitted[4]
        res[b'max_image_height']=serial_splitted[5]
    return res


if __name__ == "__main__":
    print("alex","madon",sep="")
