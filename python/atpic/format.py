"""
Similar to lang.py

guesses the output format
xml, xhtml, html, rss
based from
header
query_string, etc...

'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'


see also user_agent.py

"""
# import logging
import atpic.log
import re

import atpic.environment



"""
Guesses the format used to do XSL.
"""
xx=atpic.log.setmod("INFO","format")


def get_format_from_wurfl_header(environ):
    format=b''
    if b"WURFL_MIME" in environ:
        format=environ[b"WURFL_MIME"]
    return format

def get_format_from_header(environ):
    """
    Parses the Accept if exists
    Choose a shortformat if one of mime listed is known.
    """
    yy=atpic.log.setname(xx,'get_format_from_header')
    format=b''
    if b"HTTP_ACCEPT" in environ:
        header=environ[b"HTTP_ACCEPT"]
        atpic.log.debug(yy,'header',header)
        # begin copy from http://svn.pythonpaste.org/Paste/trunk/paste/httpheaders.py
        formats = [v for v in header.split(b",") if v]
        qs = []
        for format in formats:
            atpic.log.debug(yy,'format',format)
            pieces = format.split(b";")
            format, params = pieces[0].strip().lower(), pieces[1:]
            q = 1
            for param in params:
                if b'=' not in param:
                    # Malformed request; probably a bot, we'll ignore
                    continue
                lvalue, rvalue = param.split(b"=")
                lvalue = lvalue.strip().lower()
                rvalue = rvalue.strip()
                if lvalue == b"q":
                    q = float(rvalue)
            qs.append((format, q))
        atpic.log.debug(yy,"NotSorted",qs)
        # qs.sort(lambda a, b: -cmp(a[1], b[1]))
        # for py3k the above sort does not work anymore:
        # http://www.daniweb.com/code/snippet216801.html
        import operator
        index1 = operator.itemgetter(1)
        qs.sort(key=index1, reverse=True)
        atpic.log.debug(yy,"Sorted",qs)

        result=[format for (format, q) in qs]
        # end copy
        atpic.log.debug(yy,'result',result)
        # if result[0]:
        if b'application/xhtml+xml' in result:
            format=b'xhtml'
        elif b'text/html' in  result:
            format=b'html'
        elif b'application/xml' in result:
            format=b'xml'
        else:
            format=b''
    return format

def mime2format():
    """
    This is the list of allowed Mime/shortformat for XSL transforms
    """
    yy=atpic.log.setname(xx,'mime2format')
    return [
    b"text/html",
    b"application/xhtml+xml",
    b"application/xml",
    b"application/json",
    b"application/rss+xml",
    b"application/atom+xml",
    b"application/vnd.google-earth.kml+xml", # kml
    b"application/x-shockwave-flash", # swf flash
    ]




"""
    $mime_array["image/jpeg"]="jpg";
    $mime_array["image/gif"]="gif";
    $mime_array["image/png"]="png";
    //$mime_array["image/tiff"]="tiff";
    $mime_array["video/mp2p"]="mpg"; // 
    $mime_array["video/mpeg"]="mpg";
    $mime_array["video/quicktime"]="mov";
    $mime_array["video/x-msvideo"]="avi";
    $mime_array["video/x-ms-asf"]="asf";
    $mime_array["video/mp4"]="mp4";



zcat  /usr/share/doc/RFC/links/rfc5023.txt.gz|grep --color atom|grep Content

 Content-Type: application/atom+xml;type=entry
       Content-Type: application/atom+xml;type=entry;charset="utf-8"
       Content-Type: application/atom+xml;type=entry
       Content-Type: application/atom+xml;type=entry;charset="utf-8"
16.1.  Content-Type Registration for 'application/atomcat+xml'
"""

def format2mime(format):
    mime=b"text/plain"

    if format==b"xhtml":
        mime=b"application/xhtml+xml; charset=utf-8"
    elif format==b"html":
        mime=b"text/html; charset=utf-8"
    elif format==b"xml":
        mime=b"text/xml; charset=utf-8"
    return mime

def format_short():
    return [
        b'html',
        b'xhtml',
        b'xml',
        b'rss',
        b'atom',
        b'mobi',
        b'swf',
        b'map',
        b'json',
]

def get_format_from_query_string(environ):
    yy=atpic.log.setname(xx,'get_format_from_query_string')
    format=atpic.environment.get_qs_key(environ,b'f',b'')
    atpic.log.debug(yy,'I got',format)
    if format in format_short():
        atpic.log.debug(yy,'testing',format,'in format_short')

        res=format
    else:
        res=b''
    atpic.log.debug(yy,'will return',res)
    return res

def get_format_from_cookie(environ):
    yy=atpic.log.setname(xx,'get_format_from_cookie')
    val=atpic.environment.get_cookie(environ,b'format')
    atpic.log.debug(yy,'will return',val)
    return val
    
def get_format(environ):
    yy=atpic.log.setname(xx,'get_format')
    # define the format precedence
    atpic.log.debug(yy,'input=',environ)
    format=get_format_from_query_string(environ)
    if format==b'':
        format=get_format_from_cookie(environ)
    if format==b'':
        format=get_format_from_header(environ)
    if format==b'':
        format=get_format_from_wurfl_header(environ)
    if format==b'':
        format=b'xhtml'
    atpic.log.debug(yy,'setting format to',format)
    return format


if __name__=="__main__":
    unittest.main()
