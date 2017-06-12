#!/usr/bin/python3
import urllib.parse
from  xml.dom import minidom
import xml.dom.minidom
import xml.dom
import io
# import logging
import xml.sax
from io import BytesIO


import atpic.log
from atpic.mybytes import *


xx=atpic.log.setmod("INFO","composite")

# we do not accept XML attributes
# as we take the common denominator of XML and json

def explode(xmlcomposite,parenthost):
  yy=atpic.log.setname(xx,'explode')
  class ABContentHandler(xml.sax.ContentHandler):
    def __init__(self):
      xml.sax.ContentHandler.__init__(self)
      self.before=""
      self.middle=""
      self.after=""
      self.position="before"
      self.links=[]
      self.alink=""
    def startElement(self, name, attrs):
      atpic.log.debug(yy,"startElement '" + name + "'")
      if name=="composite":
        self.position="middle"
      elif name=="link":
        pass
      elif self.position=="before":
        self.before+="<"+name+">"
      elif  self.position=="after":
        self.after+="<"+name+">"

    def endElement(self, name):
      atpic.log.debug(yy,"endElement '" + name + "'")
      if name=="composite":
        self.position="after"
      elif name=="link":
        self.links.append(self.alink)
        self.alink=""
      elif self.position=="before":
        self.before+="</"+name+">"
      elif  self.position=="after":
        self.after+="</"+name+">"

    def characters(self, content):
      atpic.log.debug(yy,"characters '" + content + "'")
      if self.position=="middle":
        self.alink+=content
      elif self.position=="before":
        self.before+=content
      elif  self.position=="after":
        self.after+=content


  xmlcomposite=BytesIO(xmlcomposite) # .decode('utf8')  
  ch=ABContentHandler()
  xml.sax.parse(xmlcomposite,ch)
  before=ch.before.encode('utf8')
  after=ch.after.encode('utf8')
  links=[]
  for alink in ch.links:
    if parenthost[-4:]==b'.faa':
      alink=alink.replace('.com','.faa')
    links.append(alink.encode('utf8'))
  return (before,after,links)



def reset_env(url,environ):
    """
    Restore an environ after modification by create_env()
    """
    yy=atpic.log.setname(xx,'reset_env')
    urltuple=urllib.parse.urlsplit(url)
    atpic.log.debug(yy,"tuple",urltuple)
    tu1=urltuple[1] # .encode('utf8')
    tu2=urltuple[2] # .encode('utf8')
    tu3=urltuple[3] # .encode('utf8')
    tu3=tu3.replace(b'&amp;',b'&')
    environ[b'HTTP_HOST']=tu1
    environ[b'PATH_INFO']=tu2
    environ[b'QUERY_STRING']=tu3
    if environ[b'QUERY_STRING']==b'':
        environ[b'REQUEST_URI']=environ[b'PATH_INFO']
    else:
        environ[b'REQUEST_URI']=environ[b'PATH_INFO']+b'?'+environ[b'QUERY_STRING']
    return environ


def env_backup(environ):
    return (environ[b'HTTP_HOST'],environ[b'PATH_INFO'],environ[b'QUERY_STRING'],environ[b'REQUEST_URI'])

def env_restore(backup,environ):
    environ[b'HTTP_HOST']=backup[0]
    environ[b'PATH_INFO']=backup[1]
    environ[b'QUERY_STRING']=backup[2]
    environ[b'REQUEST_URI']=backup[3]

def create_env(url,environ):
    """
    Sets a wsgi like environ for a GET url
    Overrides some of the env passed

    PATH_INFO
    QUERY_STRING (REQUEST_URI)
    HTTP_HOST
    """
    yy=atpic.log.setname(xx,'create_env')
    atpic.log.debug(yy,"INPUT: environ:",environ)
    
    # urllib.parse.urlparse(urlstring, scheme='', allow_fragments=True)
    urltuple=urllib.parse.urlsplit(url)
    atpic.log.debug(yy,"tuple",urltuple)
    tu1=urltuple[1] # .encode('utf8')
    tu2=urltuple[2] # .encode('utf8')
    tu3=urltuple[3] # .encode('utf8')
    tu3=tu3.replace(b'&amp;',b'&')
    environ[b'HTTP_HOST']=tu1
    environ[b'PATH_INFO']=tu2
    if environ[b'QUERY_STRING']==b"":
        environ[b'QUERY_STRING']=tu3
    elif tu3==b'':
        pass
    else:
        environ[b'QUERY_STRING']=tu3+b"&"+environ[b'QUERY_STRING'] # &amp;

    # now we forge the request_uri based on the previous variables
    if environ[b'QUERY_STRING']==b'':
        environ[b'REQUEST_URI']=environ[b'PATH_INFO']
    else:
        environ[b'REQUEST_URI']=environ[b'PATH_INFO']+b'?'+environ[b'QUERY_STRING']
    atpic.log.debug(yy,"OUTPUT: new environ",environ)
    # Parse a URL into six components, returning a 6-tuple. This corresponds to the general structure of a URL: scheme://netloc/path;parameters?query#fragment.
    atpic.log.debug(yy,"====================================")
    return environ


if __name__ == "__main__":
    xmlcomposite=b"<composite><link>http://atpic.com/login</link><link>http://atpic.com/search?sort=random</link><link>http://atpic.com/news</link></composite>"
    lista=explode(xmlcomposite)
    print(lista)
