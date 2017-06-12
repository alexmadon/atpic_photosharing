#!/usr/bin/python3
"""
Deals with PUT/POST indata
"""

import cgi
import io
import os
import re
import subprocess
import tempfile
import urllib.parse


import atpic.dispatcher
import atpic.errors
import atpic.log
import atpic.mybytes
import atpic.jsonat_json2python
import atpic.parameters


xx=atpic.log.setmod("INFO","getindata")
# http://www.w3.org/TR/WD-html40-970917/interact/forms.html
# post: Use the HTTP POST method. This method includes name/value pairs in the body of the form and not in the URL specified by the action attribute. 

# http://stackoverflow.com/questions/4007969/application-x-www-form-urlencoded-or-multipart-form-data
# The MIME types you mention are the two Content-Type headers for HTTP POST requests that user-agents (browsers) must support. The purpose of both of those types of requests is to send a list of name/value pairs to the server. 


def tmp_new(base=b'/tmp'):
    yy=atpic.log.setname(xx,'tmp_new')
    atpic.log.debug(yy,"base",base)
    sfp=tempfile.NamedTemporaryFile(dir=base.decode('utf8'),prefix='atup',delete=False)
    atpic.log.debug(yy,"fname",sfp.name)
    return sfp

def tmp_unlink(fname):
    yy=atpic.log.setname(xx,'tmp_unlink')
    need2clean=atpic.parameters.remove_tmp_files()
    if need2clean:
        atpic.log.debug(yy,"removing",fname)
        os.unlink(fname)
    else:
        atpic.log.debug(yy,"NOT removing",fname)

def parse_header(sline):
    """
    Parses a header line, e.g.:
    Content-Disposition: form-data; name="userfile"; filename="corsica_from_space_small.jpg"
    And returns a KEY value and options
    """
    yy=atpic.log.setname(xx,'parse_header')
    atpic.log.debug(yy,"parse_header",sline)
    p = re.compile(b'-')
    splitted=sline.split(b':')
    header_name=splitted[0]
    header_name=header_name.upper() # decide we use upper case
    header_name=p.sub(b'_',header_name) # regex replace - with _
    header_value=b":".join(splitted[1:])
    atpic.log.debug(yy,"header_name",header_name)
    atpic.log.debug(yy,"header_value",header_value)
    
    (header_main_value, header_options) = cgi.parse_header(header_value.decode('utf8'))

    header_main_value=header_main_value.encode('utf8')
    header_options=atpic.mybytes.env2bytes(header_options)
    atpic.log.debug(yy,"header_main_value",header_main_value)
    atpic.log.debug(yy,"header_options",header_options)
    return (header_name,header_main_value,header_options)    

def multipart_get_the_headers(boundary,filename,positions):
    """
    returns a list [] of (headers,boundary_start, body_start,body_end)
    """
    yy=atpic.log.setname(xx,'multipart_get_the_headers')
    atpic.log.debug(yy,"boundary,filename,positions",boundary,filename,positions)
    # now get the headers:
    atpic.log.debug(yy,"NOW get the headers")
    fp=open(filename,"rb")


    parts=[] # a list of (headers,boundary_start, body_start,body_end)
    boundary_nb=0

    for (position,rest) in positions:
        boundary_nb=boundary_nb+1
        headers={} # a new dict of headers
        fp.seek(position)
        # done not use the 1st line, as it contains the boundary
        line=fp.readline()
        # except to detect end of multipart
        if line.startswith(b'--'+boundary+b'--'):
            atpic.log.debug(yy,"END of multipart at",position)
            pass
        else:
            for i in range(0,10): # put a limit of 10 lines per header
                line=fp.readline()
                atpic.log.debug(yy,"line",line)
                if line==b'\r\n':
                    eoh=fp.seek(0,io.SEEK_CUR)
                    atpic.log.debug(yy,"END of header at",eoh)
                    body_start=eoh
                    body_end=positions[boundary_nb][0]-2
                    parts.append((headers,body_start,body_end))
                    break
                else:
                    # sline=line.decode('utf8')
                    sline=line.rstrip()
                    atpic.log.debug(yy,"sline",sline)
                    (header_name,header_main_value,header_options)=parse_header(sline)
                    headers[header_name]=(header_main_value,header_options)
            atpic.log.debug(yy,"HHHHH",headers)

    fp.close()
    atpic.log.debug(yy,"finished")
    atpic.log.debug(yy,"parts",parts)
    return parts

def multipart_parse_disk(boundary,filename):
    """
    Processes a file on disk using Linux command 'grep'
    Looking for the boundary
    and headers
    Returns a list of positions where a boundary is found
    
    """
    yy=atpic.log.setname(xx,'multipart_parse_disk')
    # time grep -A 3 -n -b --binary-files=text 1b2cdaa65388 /tmp/atupCdDtmV
    # http://stackoverflow.com/questions/2427913/grepping-for-string-containing-dash


    # -b : output the bytes position of match
    # --binary-files=text : consider the binary file as text
    # --max-count=100: avoid floods attacks 
    #        with large files containg a lot of boundaries
    process = subprocess.Popen(['grep', '-b','--binary-files=text','--max-count=100','--', boundary, filename], stdout=subprocess.PIPE)
    (stdout, stderr) = process.communicate()
    atpic.log.debug(yy,"line",type(stdout))
    fp=io.BytesIO(stdout)
    lines=fp.readlines()
    positions=[]
    for line in lines:
        atpic.log.debug(yy,"line",line)
        splitted=line.split(b':')
        position=int(splitted[0])
        rest=b":".join(splitted[1:])
        atpic.log.debug(yy,"position",position)
        atpic.log.debug(yy,"rest",rest)
        positions.append((position,rest))

    fp.close()
    return positions


def multipart_extract_values(headers,filename):
    """
    input: a list [] of (headers,body_start,body_end)
    writes each part to a separate file

    returns a modified 'headers' list with the filename for each part
    """
    yy=atpic.log.setname(xx,'multipart_extract_values')
    newheaders=[]

    atpic.log.debug(yy,"multipart_extract_values",headers,filename)
    fp=open(filename,"rb")
    for (headers,body_start,body_end) in headers:
        # need to decide what to do (in memory or on disk)
        # for the moment: to disk
        body_length=body_end-body_start
        chunk_length=1<<16

        fp.seek(body_start)

        sftp=tmp_new()
        newheaders.append((headers,body_start,body_end,sftp.name.encode('utf8')))
        # division operator
        # http://www.python.org/dev/peps/pep-0238/
        rest=body_length%chunk_length
        floor=body_length//chunk_length
        atpic.log.debug(yy,"floor,rest",floor,rest)
        for i in range(0,floor):
            atpic.log.debug(yy,"read BIG chunk")
            chunk=fp.read(chunk_length)
            sftp.write(chunk)
        # read/write the rest
        chunk=fp.read(rest)
        sftp.write(chunk)
        sftp.close()
    fp.close()
    atpic.log.debug(yy,"will return",newheaders)

    return newheaders

def multipart_summary(newheaders):
    """
    We simplify the headers.
    we want to return a list of [(name, value),]
    but that is a bit more complicated, as value can be a file, with mime and name, hence we return:
    a list of [(name,isfile,value),]
    where value is a bytes if isfile is false
    and value is a (fname,nicename,mimetype) if isfalse is true

    the tmp files comntaining the values are read and deleted
    the binary file names are stored in the dict to be processed later

    """
    yy=atpic.log.setname(xx,'multipart_summary')
    atpic.log.debug(yy,"input=",newheaders)
    alist=[]

    for (header,start,end,fname) in newheaders:
        atpic.log.debug(yy,"summarizing",header,start,end,fname)
        (cdisp,cdict)=header.get(b'CONTENT_DISPOSITION',(b'',{}))
        # CONTENT_DISPOSITION rfc2183.txt
        if cdisp==b'form-data':
            atpic.log.debug(yy,"forma data")
            aname=cdict[b'name']
            if aname==b'userfile':
                atpic.log.debug(yy,"this is a userfile")
                original_name=cdict.get(b'filename',b'')
                ctype=header.get(b'CONTENT_TYPE',(b'',{}))
                original_mime=ctype[0]
                value2store=(fname,original_name,original_mime)
                # flist.append(value2store)
                alist.append((aname,True,value2store))
            else:
                fp=open(fname,"rb")
                value2store=fp.read()
                atpic.log.debug(yy,"value2store",value2store)
                fp.close()
                tmp_unlink(fname)            
                alist.append((aname,False,value2store))
        elif cdisp==b'': # no content disposition specified
            # like in atompub
            # http://feedvalidator.org/
            original_name=b''
            ctype=header.get(b'CONTENT_TYPE',(b'',{}))
            original_mime=ctype[0]
            atpic.log.debug(yy,"original_mime",original_mime)
            value2store=(fname,original_name,original_mime)
            alist.append((b'nocontentdisposition',True,value2store))


    atpic.log.debug(yy,"will return",alist)
    return alist






def dump_stream(environ,base=b'/tmp'):
    """
    Dumps the wsgi input stearm to disk.
    Returns le filename of the tmp file created.
    """
    yy=atpic.log.setname(xx,'dump_stream')
    fp=environ[b'wsgi.input']
    sfp=tmp_new(base)
    atpic.log.debug(yy,"will dump to:",sfp.name)
    needtoget=1<<16
    chunk=fp.read(needtoget)
    while chunk:
        atpic.log.debug(yy,"chunk length",len(chunk))
        sfp.write(chunk)
        atpic.log.debug(yy,"need to get",needtoget)
        chunk=fp.read(needtoget)
    filename=sfp.name.encode('utf8')
    sfp.close()
    fp.close()
    atpic.log.debug(yy,"will return filename:",filename)
    return filename



def multipart_save(environ,indatafilename):
    """
    Saves the POST stream onto the disk.
    """
    # content_type = environ.get('CONTENT_TYPE', 'application/x-www-form-urlencoded')
    # or use the cgi
    yy=atpic.log.setname(xx,'multipart_save')
    atpic.log.debug(yy,"input=(environ,indatafilename)=",(environ,indatafilename))
    (ctype, pdict) = cgi.parse_header(environ[b'CONTENT_TYPE'].decode('utf8'))
    ctype=ctype.encode('utf8')
    atpic.log.debug(yy,"cgi ctype",ctype)
    atpic.log.debug(yy,"cgi pdict",pdict)
    boundary=pdict["boundary"].encode('utf8')
    atpic.log.debug(yy,"boundary",boundary)

    # then we look for boundaries
    positions=multipart_parse_disk(boundary,indatafilename)
    atpic.log.debug(yy,"2positions",positions)
    headers=multipart_get_the_headers(boundary,indatafilename,positions)
    atpic.log.debug(yy,"2headers",headers)
    newheaders=multipart_extract_values(headers,indatafilename)
    atpic.log.debug(yy,"2newheaders",newheaders)
    alist=multipart_summary(newheaders)

    atpic.log.debug(yy,"will return",alist)
    return alist

# http://curl.haxx.se/docs/httpscripting.html
# NO curl -d @vid/1.mpg http://alex.atpic.faa/gallery/3/pic
# YES curl --form title=title1 --form upload=@vid/1.mpg http://alex.atpic.faa/gallery/3/pic

# http://en.wikipedia.org/wiki/MIME#Multipart_messages
# command line tool: 
# /usr/bin/mpack
# /usr/bin/munpack
# time grep -A 3 -n -b --binary-files=text 1b2cdaa65388 /tmp/atupCdDtmV

# should check valid fields, can be unit tested
# http://wsgi.org/wsgi/Specifications/handling_post_forms
# content_type = environ.get('CONTENT_TYPE', 'application/x-www-form-urlencoded')
# return (content_type.startswith('application/x-www-form-urlencoded'
#         or content_type.startswith('multipart/form-data'))
# large file in wsgi:
# http://hg.python.org/cpython/file/default/Lib/cgi.py
# http://wiki.pylonshq.com/display/pylonscookbook/Hacking+Pylons+for+handling+large+file+upload
# http://stackoverflow.com/questions/1103940/upload-a-potentially-huge-textfile-to-a-plain-wsgi-server-in-python
# http://debuggable.com/posts/parsing-file-uploads-at-500-mb-s-with-node-js:4c03862e-351c-4faa-bb67-4365cbdd56cb
# or use the cgi
# fill a hash with the boundary characters
# read until EOF
# http://stackoverflow.com/questions/1035340/reading-binary-file-in-python
# http://www.ietf.org/rfc/rfc2046.txt
# /usr/share/doc/RFC/links/rfc2046.txt.gz
# dash-boundary := "--" boundary
#                   ; boundary taken from the value of
#                   ; boundary parameter of the
#                   ; Content-Type field.
# for line in environ['wsgi.input']:
# while (i + boundary.length <= chunk.length) {
#   if (chunk[i + boundary.length - 1] in boundaryChars) {
#     // worst case, go back to byte by byte parsing until a non-matching char occurs
#     break;
#   }
#   i += boundary.length;
# }


def get_indata_wrapper(environ,base="/tmp"):
    try:
         indata=get_indata(environ,base)
    except atpic.errors.Error413:
        raise # re-raise the error
    except:
        raise atpic.errors.DataError()
    return indata


def parse_qs2bytes(indata):
    """
    Trasforms to best a qs structure
    """
    yy=atpic.log.setname(xx,'parse_qs2bytes')
    atpic.log.debug(yy,"input",indata)
    new_indata={}
    for key in indata.keys():
        atpic.log.debug(yy,"key",key)
        nkey=key.encode('utf8')
        vallist=[]
        for val in indata[key]:
            vallist.append(val.encode('utf8'))
        new_indata[nkey]=vallist
        
    atpic.log.debug(yy,"output",new_indata)
    return new_indata



def check_size(indatafilename,maxsize):
    sstat=os.stat(indatafilename)
    size=sstat.st_size
    # maxsize=1<<16
    # maxsize=2
    if size >  maxsize:
        raise atpic.errors.Error413(b'size:',atpic.mybytes.int2bytes(size),b'bytes, input data too big for this content type.')

def urlencoded_save(environ,indatafilename):
    yy=atpic.log.setname(xx,'urlencoded_save')
    alist=[]
    atpic.log.debug(yy,"content type application/x-www-form-urlencoded")

    # check the size
    check_size(indatafilename,1<<27) # 134217728
    fp=open(indatafilename,'rb')
    qs=fp.read() # need to check the size of the chunk read SECURITY
    fp.close()
    atpic.log.debug(yy,"qs",type(qs),qs)
    qss=qs.decode('utf8')
    indata=urllib.parse.parse_qsl(qss, keep_blank_values=False, strict_parsing=False)
    atpic.log.debug(yy,"parse_qsl gives indata=",indata)
    # indata=parse_qs2bytes(indata)
    # atpic.log.debug(yy,"parse_qs gives indata in bytes=",indata)
    for (key,value) in indata:
        alist.append((key.encode('utf8'),False,value.encode('utf8'))) 

    tmp_unlink(indatafilename)

    return alist



def json_save(indatafilename):
    yy=atpic.log.setname(xx,'json_save')
    atpic.log.debug(yy,"indatafilename=",indatafilename)
    alist=[]
    # check the size
    check_size(indatafilename,1<<16)
    fp=open(indatafilename,'rb')
    ajson=fp.read() # need to check the size of the chunk read SECURITY
    fp.close()
    ajson_parsed=atpic.jsonat_json2python.parse(ajson)
    for (key,value) in ajson_parsed:
        alist.append((key,False,value))
    tmp_unlink(indatafilename)
    return alist

def get_indata(environ,base=b"/tmp"):
    """
    This deals with Write requests to server (POST, PUT)
    It can handle several content types:
    forms application/x-www-form-urlencoded multipart/form-data
    or direct image 
    returns a pair:
    (indata,infiles)
    indata is a dictionary
    infiles is a list of triplet file rows:
    [(fname,original_name,original_mime),]

    we always stream to disk
    we do not always clean the disk

    data IS NOT validated.
    """

    yy=atpic.log.setname(xx,'get_indata')
    alist=[]

    atpic.log.debug(yy,"get_indata",environ)
    action=environ[b'REQUEST_METHOD']
    action=action.lower()
    verb=action
    atpic.log.debug(yy,"verb",verb)
    
    if verb in (b'post',b'put'): # what about ['post','delete'] and HEAD?
        # problem: curl -v -X HEAD http://alex.atpic.faa
        # potential DoS, not anymore but does keep-alive
        atpic.log.debug(yy,"we need content type")

        # first we save to disk
        indatafilename=dump_stream(environ,base)

        # then we get the content type
        content_type = environ.get(b'CONTENT_TYPE', b'application/x-www-form-urlencoded')

        atpic.log.debug(yy,"content_type:" , content_type)

        (ctype, pdict) = cgi.parse_header(content_type.decode('utf8'))
        ctype=ctype.encode('utf8')
        atpic.log.debug(yy,"ctype:" , ctype)

        if content_type.startswith(b'application/x-www-form-urlencoded'):
            atpic.log.debug(yy,"content type application/x-www-form-urlencoded")
            alist=urlencoded_save(environ,indatafilename)

        elif content_type.startswith(b'multipart/form-data'):
            atpic.log.debug(yy,"content type multipart/form-data")
            alist=multipart_save(environ,indatafilename)
            # do NOT remove indatafilename yet!

        elif content_type.startswith(b'multipart/related'): # rfc2387
            atpic.log.debug(yy,"content type multipart/related")
            raise Exception(b"Format multipart/related is not supported.")
            # /usr/share/doc/RFC/links/rfc2387.txt.gz
            # see also RFC/1521
            # rfc1341/7_2_Multipart for CRLF
            # atom publishing protocol /usr/share/doc/RFC/links/rfc5023.txt.gz
            # The Atom Syndication Format /usr/share/doc/RFC/links/rfc4287.txt.gz
        elif content_type.startswith(b'application/json'): # rfc2387
            atpic.log.debug(yy,"content type is application/json")
            alist=json_save(indatafilename)
        else:
            # aimed at streaming image/jpg, videos, etc....
            # SECURITY: need a protection on MIME types
            atpic.log.debug(yy,"content type OTHER")
            original_name= environ.get(b'HTTP_SLUG', b'')
            atpic.log.debug(yy,'original_name from slug',original_name)
            original_mime=ctype # need to parse content_type
            alist.append((b'contentypeother',True,(indatafilename,original_name,original_mime)))
            # do NOT remove indatafilename yet!
    else:
        atpic.log.debug(yy,"we do not need content type")
        pass

    atpic.log.debug(yy,"will return: alist=",alist)
    return alist



if __name__ == "__main__":
    pass
