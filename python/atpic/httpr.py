"""
Forge the response to a http_async request.

the protocol is vaguely based on HTTP


It is used by fuse file system is do starts and readdir based on path


A read/write to the tokyo db is also provided.
postgresql is the master POSTed to this HTTP server

 /usr/local/apache2/bin/ab -n 10000 -c 10 http://localhost:8882/testdir

"""

import zlib
import re

import atpic.tokyofs


def parse_headers(headers):
    """
    Return the length of the request body if the request is more than headers.

    GET expects 0 more bytes
    POST, PUT expect size>0
    """

    (verb,uri)=splituri(headers[0]) # first line of header
    if verb=="POST":
        # the we need to look at the Content-Length: header
        size=get_content_length(headers)
    else:
        size=0
    return size

def get_content_length(headers):
    """Look for a  Content-Length: header and returns the length in bytes"""
    p = re.compile("Content-Length: *([0-9]+)",re.IGNORECASE)
    size=0
    for header in headers[1:]:
        print "headeris: -------------%s------------" % header
        m=p.search(header)
        if m:
            print "we have a match!"
            size=int(m.groups(0)[0])
            print "size=%s" % size
            break
    return size
        

        
def answer(headers,tokyo,body=""):
    """body is a list of HTTP query fields
    protocol:
    The first element of the list
    GET or STAT /path
    READDIR /path
    POST <xml> is used to transfer from Postgresql to Tokyo db;
    we may have a problem with the terminator
    
    answer can be in gzip format
    """

    theanswer=answerbody(headers,tokyo,body)

    code=[]
    code.append("HTTP/1.1 200 OK")
    code.append("\r\n")
    code.append("Content-Type: application/xhtml+xml; charset=utf-8")
    code.append("\r\n")
    code.append("Content-Length: %s" % len(theanswer))
    code.append("\r\n")
    code.append("\r\n")

    code.append(theanswer)
    # code.append("\r\n")
    # response=code+"\r\n\r\n"+theanswer
    return "".join(code)


def answerbody(headers,tokyo,body):
    """Forge the body of the answer
    headers: the request list (headers) sent by the client received by the server
    tokyo: the tokyo database handler the sever is connected to 
    """
    # analyse the request
    body_list=[]
    (verb,uri)=splituri(headers[0]) # first line of header
    if verb=="GET" or verb=="STAT":
        body_list.append("<answer>")
        body_list.append("<verb>%s</verb>" % verb)
        body_list.append("<uri>%s</uri>" % uri)
        # get from tokyo, we need a tokyo handler
        body_list.append(atpic.tokyofs.stat(uri,tokyo))
        body_list.append("</answer>")

        # body=zlib.compress(body)
    if verb=="POST":
        # we need to insert/update tokyodb
        # TO IMPLEMENT
        # for the momement we just echo the posted body
        body_list.append("".join(body)) # body is a list


    body="".join(body_list)
    return body

def splituri(data):
    """Return the verb and URI"""
    splitted=data.split(" ")
    return (splitted[0],splitted[1])
