#!/usr/bin/python3
# in py3k, print signature is: def print(*args, sep=' ', end='\n', file=None)

# logging http://stackoverflow.com/questions/812422/why-does-python-logging-package-not-support-printing-variable-length-args
import cgi
import copy
import datetime
import io
import json
from lxml import etree
import os
import random
import re
import subprocess
import sys
import tempfile
import time
import traceback
import urllib.parse
import wsgiref.headers
import xml.dom.minidom


import atpic.allowed_objects
import atpic.authenticatecrypto
import atpic.authenticatesql
import atpic.autorize
import atpic.captcha
import atpic.composite
import atpic.cleaner
import atpic.errors
import atpic.libpqalex
import atpic.dispatcher
import atpic.elasticsearch_queries
import atpic.forgesql
import atpic.format
import atpic.getindata
import atpic.hashat
import atpic.indatautils
import atpic.journal
import atpic.json_elas2atpic
import atpic.lang
import atpic.listfields
import atpic.log
import atpic.mybytes
import atpic.queryparser
import atpic.needindex
import atpic.parameters
import atpic.pathbased
import atpic.processinfiles
import atpic.sendmail
import atpic.solr
import atpic.stats
import atpic.capabilities
import atpic.validate
import atpic.wikidiff
import atpic.wiki_lines
import atpic.wiki_rst
import atpic.wsob
import atpic.xml2json_etree
import atpic.xmlob
import atpic.xmlutils
import atpic.xsl
import atpic.xsllib
import atpic.xslt_client
from atpic.redisconst import *

xx=atpic.log.setmod("DEBUG","worker")



def prunt(*args, sep=' ', end='\n', out=None):
    print(*args, sep=sep, end=end, file=out)
def print_time(*args):
    print(args)
    

def get_user_details_from_uid(uid,db): # get_uname
    yy=atpic.log.setname(xx,'get_user_details_from_uid')
    t1=time.clock()
    query=b"select id,_name,_servershort from _user where id=$1"
    result=atpic.libpqalex.pq_exec_params(db,query,(uid,))
    result=atpic.libpqalex.process_result(result)
    t2=time.clock()
    print_time('get_user_details_from_uid (ms)',1000.0*(t2-t1))
    return result[0]

def check_end_collection(depth,pxplo,actions):
    """
    Check we have a collection and that we are at the end of the object list
    """
    yy=atpic.log.setname(xx,'check_end_collection')
    atpic.log.debug(yy,'input(',depth,',',pxplo,',',actions,')')
    if depth==len(pxplo) and pxplo.getmatrix(len(pxplo)-1,1)==None and actions[-1]==b'get':
        res=True
    elif depth==len(pxplo)-1 and pxplo.getmatrix(len(pxplo)-1,0)==b'revision' and actions[-1]==b'get':
        revs=pxplo.getmatrix(len(pxplo)-1,1)
        if revs:
            if re.match(b"^[0-9]+$",revs):
                res=False
            else:
                res=True
        else:
            res=True

    else:
        res=False
    atpic.log.debug(yy,'will return',res)
    return res


def convert_sqltime_xmltime(sqltime):
    yy=atpic.log.setname(xx,'convert_sqltime_xmltime')
    try:
        datetimefirst=datetime.datetime.strptime(sqltime.decode('utf8'),"%Y-%m-%d %H:%M:%S.%f" )
    except:
        try:
            datetimefirst=datetime.datetime.strptime(sqltime.decode('utf8'),"%Y-%m-%d %H:%M:%S")
        except:
            datexml=''
            # raise
    try:
        datexml=datetimefirst.strftime("%Y-%m-%dT%H:%M:%S.%f")
    except:
        pass
    return datexml.encode('utf8')


def fix_date_value(key,value):
     if key[:5]==b'_date' and key not in (b'_datetimeoriginal',b'_datetimedigitized',b'_date'):
         value=convert_sqltime_xmltime(value)
     return value
 

def data_hide(key,hxplo,pxplo,actions):
    """
    Tells if that key needs to be secret and hidden
    """
    yy=atpic.log.setname(xx,'data_hide')
    atpic.log.debug(yy,'input=',key,hxplo,pxplo,actions)
    # default is show it (do not hide)
    needtohide=False
    if key==b'_password': # need to hide the password even encrypted
        needtohide=True
    if key==b'_email': # need to hide the mail if not the user or admin

        atpic.log.debug(yy,'pxplo.list()',pxplo.list())
        atpic.log.debug(yy,'pxplo.keys()',pxplo.keys())
        atpic.log.debug(yy,'actions',actions)

        if pxplo.list()==[(b'forgot', None)]:
            atpic.log.debug(yy,'this is a forgot email, do not hide it for now....')
            needtohide=False # set to false????
        elif pxplo.keys()==[b'user'] and actions==[b'get', b'put']:
            atpic.log.debug(yy,'user wants to update his email')
            needtohide=False
        else:
            atpic.log.debug(yy,'need to hide email')
            needtohide=True
    if key==b'_login': # need to hide _login if not the user
        if pxplo.list()==[(b'forgot', None)]:
            atpic.log.debug(yy,'this is a forgot login, do not hide it for now....')
            needtohide=False # set to false????
        else:
            atpic.log.debug(yy,'need to hide login')
            needtohide=True
    atpic.log.debug(yy,'output=',needtohide)
    return needtohide

def display_one_object(line,depth,hxplo,pxplo,actions,xmlo,autoresult,environ):
    # can be unit tested
    # 'autoresult' is the autorization result

    # dates and datetimes need to be XML compatible XSD:
    # xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    # postgresql: The output format of the date/time types can be set to one of the four styles ISO 8601, SQL (Ingres), traditional POSTGRES (Unix date format), or German. The default is the ISO format

    yy=atpic.log.setname(xx,'display_one_object')
    atpic.log.debug(yy,'input',line,depth,hxplo.list(),pxplo.list(),actions,xmlo,autoresult,environ)
    newline=display_one_object_newline(line,depth,hxplo,pxplo,actions,xmlo,autoresult,environ)
    for (key,value) in newline: # the SQL column should be filtered: 
        xmlo.data.push(key)
        xmlo.data.append(value)
        xmlo.data.pop()
    atpic.log.debug(yy,'will return xmlo.data.content=',xmlo.data.content)
    return xmlo    



def display_one_object_newline(line,depth,hxplo,pxplo,actions,xmlo,autoresult,environ):
    # from a line input (dict)
    # returns a new line which is a LIST, ordered by key
    yy=atpic.log.setname(xx,'display_one_object_newline')
    atpic.log.debug(yy,'input',line,depth,hxplo.list(),pxplo.list(),actions,xmlo,autoresult,environ)
    atpic.log.debug(yy,"KEYS,",line.keys())

    newdict={}

    for key in line.keys(): # the SQL column should be filtered: 
        # this is the date in XML compatible format:
        value=fix_date_value(key,line[key]) 
        # e.g do not display the password (even encrypted)! hide it!
        needtohide=data_hide(key,hxplo,pxplo,actions)
        if needtohide:
            atpic.log.debug(yy,'hiding key',key)
        else:
            if key[:1]==b"_": # the sql fields usually start with _: remove it
                skey=key[1:]
            else:
                skey=key
            # check if skey starts with pathstore or pathstorewater
            # if autoresult==watermarked, then only show hashes for watermarked
            # if autoresult==autorized, then show all hashes
            # push that shortened key
            # if skey.startswith(b'datestore'):
            if skey==b'artefact':
                atpic.log.debug(yy,'artefact=',value)
                if value!=b'':
                    artefacts=value.split(b'|')
                    for anartefact in artefacts:
                        artedetails=anartefact.split(b';')
                        resolutioncode=artedetails[0]
                        extension=artedetails[1]
                        pathondisk=artedetails[2]
                        pid=artedetails[3]
                        partition=line[b'_partition']

                        hashvalue=atpic.hashat.forge_pathstorehash(pid,resolutioncode,pathondisk,partition,extension)


                        hashkey=b'pathstore_'+resolutioncode
                        if autoresult==b'watermarked':
                            if resolutioncode.startswith(b'w'): # watermark
                                newdict[hashkey]=hashvalue
                        elif autoresult==b'authorized':
                            newdict[hashkey]=hashvalue


            elif skey.startswith(b'pathstore'):
                try:
                    if value!=b'':
                        pid=line[b'id']
                        extension=line[b'_extension']
                        resolution=re.sub(b'[^0-9]', b'', skey)
                        pathondisk=value
                        partition=line[b'_partition']
                        resolutioncode=b'0'
                        hashvalue=atpic.hashat.forge_pathstorehash(pid,resolutioncode,pathondisk,partition,extension)


                        # hashvalue=atpic.hashat.dohash(pid,resolution,pathondisk)
                        # hashvalue=line[b'_partition']+hashvalue+b'.'+extension
                        hashkey=skey # +b'hash'
                        if autoresult==b'watermarked':
                            if skey.startswith(b'pathstorewater'):
                                newdict[hashkey]=hashvalue
                        elif autoresult==b'authorized':
                            newdict[hashkey]=hashvalue
                except:
                    atpic.log.error(yy,'could not process date',skey,value,traceback.format_exc())
            elif skey==b'wikitext':
                newdict[skey]=value
                # newdict[b'wikihtml']=atpic.wiki_rst.convert(value,hxplo,pxplo) # need DB access so not good in this function: need to postpone to post processing? could be a special zeromq layer
                lines=atpic.wiki_lines.get_lines(environ)
                if lines:
                    (line_from,line_to)=lines
                    newdict[b'wikilines']=atpic.wiki_lines.extract(value,line_from,line_to)
            else:
                newdict[skey]=value

    # now calculate width
    # check if this is a true pic object
    # see get_resolution_todo(amax)
    if b'_width' in line.keys() and  b'_height' in line.keys():
        if line[b'_width'] and line[b'_height']:
            thewidth=atpic.mybytes.bytes2int(line[b'_width'])
            theheight=atpic.mybytes.bytes2int(line[b'_height'])
            atpic.log.debug(yy,"(thewidth,theheight)=",(thewidth,theheight))
            amax=atpic.mybytes.bytes2int(max(thewidth,theheight))
            ratio=min(thewidth,theheight)/max(thewidth,theheight)
            for res in [b'1024',b'600',b'350',b'160',b'70']:
                resolutioncode=b'pathstore_r'+res
                resint=atpic.mybytes.bytes2int(res)
                smaller=atpic.mybytes.int2bytes(int(ratio*resint))
                if resolutioncode in newdict.keys():
                    widthkey=b'width_r'+res
                    heightkey=b'height_r'+res
                    if thewidth>theheight:
                        atpic.log.debug(yy,"landscape")
                        newdict[widthkey]=res
                        newdict[heightkey]=smaller
                    else:
                        atpic.log.debug(yy,"portrait")
                        newdict[widthkey]=smaller
                        newdict[heightkey]=res
    # sort by key
    newline=sorted(newdict.items())

    atpic.log.debug(yy,'will return newline=',newline)
    return newline   


def actions_transform(actions,dataerror):
    """
    Transforms actions to do forgesql: if an error, then we need to represent 
    the form
    """
    yy=atpic.log.setname(xx,'actions_transform')
    atpic.log.debug(yy,'input',actions,dataerror)
    if dataerror:
        atpic.log.debug(yy,'has error')
        newactions=[]
        if len(actions)==1:
            newactions=[b'get',actions[0]]
        else:
            newactions=[b'get',actions[1]]
    else:
        atpic.log.debug(yy,'has no error')
        newactions=actions
    atpic.log.debug(yy,'output=',newactions)
    return newactions

def data_clean(indata,pxplo,atype,actions,environ):
    """
    Transforms the indata dictionnary into one that can be presented in XML
    This is the version that will be stored in SQL
    """
    # we start we a simple method:
    # we XML clean all fields
    # we TXT clean title
    yy=atpic.log.setname(xx,'data_clean')
    atpic.log.debug(yy,'input=',indata)
    new_indata=[]
    for (key,isfile,value) in indata:
        if not isfile:
            if key in (b'wikitext',b'wikilines',):
                value=atpic.cleaner.cleanwiki(value) # 
            else:
                value=atpic.cleaner.html(value) # we keep some HTML tags
            # note that they can still be removeed at XSL time
            # to really display them, you need the XLS 'identity' mode
        
        new_indata.append((key,isfile,value))
    atpic.log.debug(yy,'output=',new_indata)
    return new_indata

def what_needed(hxplo,pxplo,actions,environ,format):
    # lists the transformations to apply
    yy=atpic.log.setname(xx,'what_needed')
    atpic.log.debug(yy,'input=',hxplo,pxplo,actions,environ,format)
    needxml=False
    needxsl=False
    needtrans=False
    
    # get some QUERY_STRING parameter values
    showxsl=atpic.environment.get_qs_key(environ,b"showxsl",False)
    if pxplo.getmatrix(0,0) not in (b'robots.txt',b'favicon.ico',b'captcha',b'1x1.gif',b'redirect',b'sitemap.xml',b'logout',b'dragdrop.js'):
        if showxsl:
            needxml=False
            needxsl=True
        else:
            needxml=True
            if format==b"xml" or format==b'json':
                needxsl=False
            else:
                needxsl=True
    # if atype in ("home","tree","blog"):
    atpic.log.debug(yy,'pxplo.list()',pxplo.list())
    atpic.log.debug(yy,'pxplo.keys()',pxplo.keys())
    atpic.log.debug(yy,'will return:',(needxml,needxsl,needtrans))

    return (needxml,needxsl,needtrans)




def xslt_apply_dyna(output_xsl,output_xml):
    yy=atpic.log.setname(xx,'xslt_apply_dyna')
    atpic.log.debug(yy,'input1=',(output_xsl))
    atpic.log.debug(yy,'input2=',(output_xml))
    atpic.log.debug(yy,'1')
    xslt_doc = etree.parse(io.BytesIO(output_xsl))
    atpic.log.debug(yy,'2')
    transform = etree.XSLT(xslt_doc)
    atpic.log.debug(yy,'3')

    xml_doc = etree.parse(io.BytesIO(output_xml))
    atpic.log.debug(yy,'4')
    xml_doc_new = transform(xml_doc)
    atpic.log.debug(yy,'5')
    atpic.log.debug(yy,"outtype32", type(xml_doc_new),dir(xml_doc_new))
    output=str(xml_doc_new)
    output=output.encode('utf8')
    return output

def xslt_apply_ps(output_xsl,output_xml):
    """
    The xslt transformation is made forking a process to the xsltproc program.
    """
    yy=atpic.log.setname(xx,'xslt_apply_ps')
    atpic.log.debug(yy,type(output_xml))
    p1=subprocess.Popen(['xsltproc','/home/madon/public_html/perso/entreprise/sql_current/site/atpic/python/atpic/all.xsl','-'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    output=p1.communicate(input=output_xml)[0] # send bytes
    return output


def xslt_apply_client(xml_bytes):
    """
    zmq based client server
    """
    rec=atpic.xslt_client.send(xml_bytes)
    return rec


def dispatcher_toxml(hxplo,pxplo,actions):
    xml=[]
    xml.append(b'<route>')
    xml.append(b'<actions>')
    for action in actions:
        xml.append(b'<'+action+b'/>')
    xml.append(b'</actions>')

    xml.append(b'<hxplo>'+hxplo.toxml()+b'</hxplo>')
    xml.append(b'<pxplo>'+pxplo.toxml()+b'</pxplo>')
    signature=atpic.dispatcher.signature(hxplo,pxplo,actions)
    xml.append(b'<signature>'+signature+b'</signature>')
    xml.append(b'</route>')
    xmls=b''.join(xml)
    return xmls

def work(rediscon,hxplo,pxplo,actions,autor,environ):
    yy=atpic.log.setname(xx,'work')
    headers=[]
    try:
        check_allowed_function(hxplo,pxplo,actions)
        check_allowed_hvalues(hxplo,pxplo)

        # first we get the format: it is used to choose the correct XSL, then to set the content-type header

        # set the wurfl capabilities
        db=atpic.globalcon.db
        essock=atpic.globalcon.essock
        capabilities=atpic.capabilities.set_capabilities(environ,rediscon,essock)

        # format=atpic.format.get_format(environ)
        format=capabilities[b'format']
        atpic.log.debug(yy,'aformat',format)
        # needxml?
        (needxml,needxsl,needtrans)=what_needed(hxplo,pxplo,actions,environ,format)
        atpic.log.debug(yy,'needxml',needxml,'needxsl',needxsl,'needtrans',needtrans)
        # check for redirect
        if needxml:
            # this is done for composite and normal XML
            (needredirect,url,headers)=atpic.authenticatecrypto.check_redirect(hxplo,pxplo,actions,autor,environ)
            atpic.log.debug(yy,'needredirect',(needredirect,url,headers))
            if needredirect:
                raise atpic.errors.Error302(url,headers)
        # do we need XML?
        if needxml:

            # indata
            # SECURITY: we parse before knowing if authorized!
            # may be OK but need to clean well

            # /etc/nginx/nginx.conf protection: SECURITY
            # nginx debug on # error_log /var/log/nginx/error.log debug;

            # client_body_in_file_only clean;
            # client_body_buffer_size 32K;
            # client_max_body_size 300M;
            # sendfile on;
            # send_timeout 300s;
            # (client_body_temp_path  /spool/nginx/client_temp 1 2;)
            # client_body_temp_path  /tmp/nginx
            # --http-client-body-temp-path=/var/lib/nginx/body --http-fastcgi-temp-path=/var/lib/nginx/fastcgi --http-log-path=/var/log/nginx/access.log --http-proxy-temp-path=/var/lib/nginx/proxy --http-scgi-temp-path=/var/lib/nginx/scgi --http-uwsgi-temp-path=/var/lib/nginx/uwsgi 
            # emulate slow network: tc qdisc del dev eth0 root tbf rate 128Kbit burst 10Kb lat 1562.5s

            # http://wiki.nginx.org/HttpUwsgiModule#uwsgi_buffer_size
            # http://code.google.com/p/wsgidav/
            # http://cwells.net/2012/05/02/nginx-uwsgi-and-wsgidav/
            # http://python.6.x6.nabble.com/Most-WSGI-servers-close-connections-to-early-td2210123.html
            # http://forum.nginx.org/read.php?2,217034,217034
            # nginx streaming to temp file:
            # 2011/10/21 14:01:24 [warn] 24547#0: *2408454 an upstream response is buffered to a temporary file /var/lib/nginx/fastcgi/5/69/0000017695 while reading upstream, client: 1.1.1.1, server: www.someserver.com, request: "GET /edit.html?id=6816841 HTTP/1.1", upstream: "fastcgi://192.168.1.5:9000", host: "www.someserver.com", referrer: "http://www.someserver.com/c.html"
            # inotify-tools
            # inotifywait --monitor --event CREATE --event DELETE /tmp
            # alex:
            # 2013/07/03 14:21:04 [debug] 11682#0: *1 hashed path: /var/lib/nginx/body/0000000001
            # 2013/07/03 14:21:05 [debug] 11682#0: *1 file cleanup: fd:12 /var/lib/nginx/body/0000000001

            # root@acer:/var/log/nginx#  inotifywait --recursive --monitor --event CREATE --event DELETE /var/lib/nginx/body
            # Setting up watches.  Beware: since -r was given, this may take a while!
            # Watches established.
            # /var/lib/nginx/body/ CREATE 0000000003
            # /var/lib/nginx/body/ DELETE 0000000003
            # --http-client-body-temp-path=PATH set path to the http client request body
            # --http-proxy-temp-path=PATH set path to the http proxy temporary files

            tmpdevice=b"/tmp"
            indata=atpic.getindata.get_indata_wrapper(environ,tmpdevice)
            atpic.log.debug(yy,"8a indata",indata)
            indata=data_clean(indata,hxplo,pxplo,actions,environ)
            atpic.log.debug(yy,"8b indata",indata)


            # do the authentication for both xml and composite
            (headers,authenticated,details,aid)=authenticate_any(db,hxplo,pxplo,rediscon,actions,environ,indata,headers)

            compolist=compolist_init(hxplo,pxplo,actions,autor,environ,capabilities)
            compolist=compolist_faa(compolist,environ)

            output_xlist=[]
            output_xlist.append(b'<response>')
            output_xlist.append(atpic.xmlob.xmlurl(environ))
            # inject the capabilities:
            output_xlist.append(inject_capabilities(capabilities))

            output_xlist.append(dispatcher_toxml(hxplo,pxplo,actions))
            # inject readonly
            readonly=atpic.parameters.get_readonly()
            if readonly:
                output_xlist.append(b'<readonly/>')
            block_ifreadonly_and_write(hxplo,pxplo,actions,readonly,aid)

            # inject authentication
            if authenticated:
                output_xlist.append(inject_authentication(details))

            
            output_xlist.append(b'<Component>')
            while len(compolist)> 0:
                output_xlist.append(b'<component>')
                acomponent=compolist[0]
                compolist=compolist[1:]
                link=acomponent
                backup=atpic.composite.env_backup(environ)
                atpic.composite.create_env(link,environ)
                # atpic.log.debug(yy,'environ_new',environ_new)
                atpic.log.debug(yy,'environ_newrequest_uri',environ[b'REQUEST_URI'],link)
                (hxplo,pxplo,actions,autor)=atpic.dispatcher.dispatcher(environ) # DANGEROUS: dangerous: need to avoid infinite loops!
                hxplo=atpic.xplo.Xplo(hxplo)
                pxplo=atpic.xplo.Xplo(pxplo)
                # headers=[] # what about the cookies? 
                (headers,output_xml_one,compolist)=work_xml(db,essock,rediscon,hxplo,pxplo,actions,autor,environ,indata,capabilities,headers,authenticated,details,aid,compolist)
                atpic.composite.env_restore(backup,environ)
                output_xlist.append(output_xml_one)
                output_xlist.append(b'</component>')
            output_xlist.append(b'</Component>')
            output_xlist.append(b'</response>')
            output_xml=b''.join(output_xlist)
            atpic.log.debug(yy,'output_xml',output_xml)

        # do we need XSL?
        if needxsl:
            output_xsl=work_xsl(format,environ)

        # now we set the output, headers and status
        # content-type headers should be unit tested: function of needxml, needxsl, redir, gzip?
        # we know in advance what headers should be
        # status should be passed on as exceptions in the work could modify it

        output=b''

        if needxml and not needxsl:
            if format==b'json':
                headers.append((b'Content-type',b'application/json; charset=utf-8'))


                output=atpic.xml2json_etree.xml2json(output_xml)
                # ajson2=json.loads(output.decode('utf8')) # check jsonb is valid loading it
            else:
                headers.append((b'Content-type',b'text/xml; charset=utf-8'))
                output=output_xml
        if needxsl and not needxml:
            # headers.append((b'Content-type',b'application/xslt+xml; charset=utf-8'))
            headers.append((b'Content-type',b'text/plain; charset=utf-8'))
            output=output_xsl
        if needxsl and needxml:
            headers.append((b'Content-type',atpic.format.format2mime(format)))
            # transform XML with XSL to target format
            output=xslt_apply_dyna(output_xsl,output_xml)
            # output=xslt_apply_ps(output_xsl,output_xml)
            # output=xslt_apply_client(output_xml)
        if not needxml and  not needxsl:
            atpic.log.debug(yy,"work special, captcha, robots.txt, etc...")
            (status,headers,output)=work_special(rediscon,hxplo,pxplo,actions,autor,environ)

        atpic.log.debug(yy,'endtype2',type(output))
        status=b'200 Ok'

    # ================================================
    #  ORDER IS IMPORTANT!!!!!! put redirect LAST!!!!
    # ================================================
    except atpic.errors.Error404 as e:
        atpic.log.info(yy,'404 error on',e.args)
        output=b' '.join(e.args)
        status=b'404 Not Found'
    except atpic.errors.Error413 as e:
        atpic.log.info(yy,'413 error on',e.args)
        output=b' '.join(e.args)
        status=b'413 Request Entity Too Large'
    except UnicodeDecodeError as e:
        atpic.log.error(yy,traceback.format_exc())
        atpic.log.debug(yy,'####',e,sep='X')
        # output=b'unicode decode error'
        output=e.__str__().encode('utf8')
        status=b'404 Data Error'
    except atpic.errors.Error302 as e:
        # we process redirects as exceptions 
        atpic.log.debug(yy,'error302',e,e.url,e.headers)
        status=b'302 Redirect'
        headers=e.headers
        headers.append((b'Location', e.url))
        output=b'redirecting to '+e.url

    finally:
        pass
    """
        # 1) we free the DB connection if we had one, if no we exhaust it
        try:
            atpic.libpqalex.close(db)
            pass
        except:
            pass
        try:
            essock.close()
        except:
            pass
    """
    return (status,headers,output)

def work_robots():
    output=b"""
# DISallow by default robots
User-agent: *
Disallow: /

# too many repeated hits, too quick
User-agent: litefinder
Disallow: /

# Yahoo. too many repeated hits, too quick
User-agent: Slurp
Disallow: /

# too many repeated hits, too quick
User-agent: Baidu
Disallow: /

User-agent: MJ12bot
Disallow: /

User-agent: twiceler
Disallow: /

User-agent: psbot
Disallow: /

User-agent: msnbot
Disallow: /

User-agent: Googlebot
Disallow: /

Sitemap: http://atpic.com/sitemap.xml
"""
    return output

def work_sitemap():
    output=b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url>
<loc>http://atpic.com</loc>
<changefreq>daily</changefreq>
<priority>0.9</priority>
</url>
</urlset>"""
    return output



def work_favicon():
    output=b'\x00\x00\x01\x00\x01\x00\x10\x10\x10\x00\x01\x00\x04\x00(\x01\x00\x00\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00\x04\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\xff\xff\xff\x00\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x10\x00\x00\x00\x00\x00\x00\x01\x10\x00\x00\x00\x00\x00\x00!\x11\x12!\x12!\x11\x12!\x11\x11!\x12\x11\x11\x12!\x12\x11!\x12\x11""!\x11\x11!\x12\x11\x11\x12!\x11\x12!\x12!\x11\x12\x00\x00\x00\x00\x00\x00\x00\x00"""!\x12"""!\x12\x11""!\x12"!\x11\x11""!\x12"!\x11\x11""!\x12"!\x12\x11"!\x11\x11\x12"\x11\x12"!\x11\x11\x12""""""""\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    return output

def work_1x1gif():
    # ===================================
    # to generate that 1x1 GIF file:
    # convert -size 1x1 xc:transparent 1.gif
    # f=open('1.gif','rb')
    # a=f.read()
    # print(a)
    output=b'GIF89a\x01\x00\x01\x00\xf0\x00\x00\x00\x00\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
    return output

def work_special(rediscon,hxplo,pxplo,actions,autor,environ):
    # rediscon is needed for captcha
    # for captcha and robots.txt
    yy=atpic.log.setname(xx,'work_special')
    atpic.log.debug(yy,'input=',(rediscon,hxplo,pxplo,actions,autor,environ))
    check_allowed_function(hxplo,pxplo,actions)
    status=b'200 Ok'
    headers=[]
    output=b''
    atpic.log.debug(yy,'iiiii pxplo',pxplo,dir(pxplo))
    if pxplo.getmatrix(0,0)==b'captcha':
        atpic.log.debug(yy,'doing captcha')
        captchapubblic=pxplo.getmatrix(0,1)
        atpic.log.debug(yy,'captchapubblic',captchapubblic)
        output=work_captcha(rediscon,captchapubblic)
        headers.append((b'Content-type',b'image/png'))
    elif pxplo.getmatrix(0,0)==b'robots.txt':
        atpic.log.debug(yy,'doing robots.txt')
        output=work_robots()
        headers=[(b'Content-type',b'text/plain')]
    elif pxplo.getmatrix(0,0)==b'sitemap.xml':
        atpic.log.debug(yy,'doing sitemap.xml')
        output=work_sitemap()
    elif pxplo.getmatrix(0,0)==b'favicon.ico':
        atpic.log.debug(yy,'doing favicon.ico')
        status=b'200 Ok'
        output=work_favicon()
        headers=[(b'Content-type',b'image/x-icon'),]
    elif pxplo.getmatrix(0,0)==b'redirect' or pxplo.getmatrix(0,0)==b'logout' :
        atpic.log.debug(yy,'doing /redirect or /logout')
        # if there is an url, check user is authentication,
        # then create a service ticket
        # and append it to the redirect url
        # then raise a Error302 exception
        output=b'redirecting'
        headers=[(b'Content-type',b'text/plain'),]
        # this is done for composite and normal XML
        (needredirect,url,headers)=atpic.authenticatecrypto.check_redirect(hxplo,pxplo,actions,autor,environ)
        atpic.log.debug(yy,'needredirect',(needredirect,url,headers))
        if needredirect:
            raise atpic.errors.Error302(url,headers)
    elif pxplo.getmatrix(0,0)==b'dragdrop.js' :
        headers=[(b'Content-type',b'application/javascript'),]
        output=b"""
function postonefile(file){
   var oOutput = document.getElementById('filesStatus');
   var formData = new FormData();
   formData.append(file.name, file);
   var oReq = new XMLHttpRequest();
   oReq.open("POST", "http://alex.atpic.faa/gallery/1/pic", true);
   oReq.onload = function(oEvent) {
       if (oReq.status == 200) {
            oOutput.innerHTML = oOutput.innerHTML+file.name+" Uploaded!<br \/>";
       } else {
            oOutput.innerHTML = oOutput.innerHTML+"Error " + oReq.status + " occurred uploading your file.<br \/>";
       }
   }
   oReq.send(formData);
}

function uploadFiles(url, files) {
   for (var i = 0, file; file = files[i]; ++i) {
       // alert(file);
       postonefile(file);
   }

}

function fileSelect(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    if (window.File && window.FileReader && window.FileList && window.Blob) {
        var files = evt.dataTransfer.files;
 
        var result = '';
        var file;
        for (var i = 0; file = files[i]; i++) {
            result += '<li>' + file.name + ' ' + file.size + ' bytes</li>';
        }
        document.getElementById('filesInfo').innerHTML = '<ul>' + result + '</ul>';
        url="http://alex.atpic.faa/gallery/1/pic";
        uploadFiles(url, files);
    } else {
        alert('The File APIs are not fully supported in this browser.');
    }
}
 
function dragOver(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    evt.dataTransfer.dropEffect = 'copy';
}
 
var dropTarget = document.getElementById('dropTarget');
dropTarget.addEventListener('dragover', dragOver, false);
dropTarget.addEventListener('drop', fileSelect, false);


"""
    else:
        atpic.log.debug(yy,'unkown situation')
        output=b'unkown special situation'
        headers=[(b'Content-type',b'text/plain'),]
    atpic.log.debug(yy,'output=',(status,headers,output))
    return (status,headers,output)


def work_captcha(rediscon,captchapublic):
    # generate a captcha image and stpore it into redis
    # when submitting a form, you will invalidate the captcha in redis
    yy=atpic.log.setname(xx,'work_captcha')
    atpic.log.debug(yy,'input',captchapublic)
    captchahidden=atpic.redis_pie._get(rediscon,REDIS_CAPTCHA+captchapublic)
    if not captchahidden:
        captchahidden=b'error'
    image=b''
    image=atpic.captcha.spit_image(captchahidden)
    return image

def work_xsl(format,environ):
    """
    Returns bytes (not string, not file)
    """
    # we do not use <h1>...<h4>
    # just <div>, <a> and <img>
    # then do CSS
    yy=atpic.log.setname(xx,'work_xsl')
    output_function=atpic.xsllib.xml2xhtml
    output=output_function(format,environ)
    atpic.log.debug(yy,'output=',(output))
    return output


def selldns2user(selldns,rediscon,db):
    yy=atpic.log.setname(xx,'selldns2user')
    try:
        query=b"select id from _user where _pdns=$1"
        values=[selldns,]
        # a prepared statement
        statement=b''
        result1=atpic.libpqalex.pq_prepare(db,statement,query)
        result=atpic.libpqalex.pq_exec_prepared(db,statement,values)
        result=atpic.libpqalex.process_result(result)
        uid=result[0][b"id"]
    except:
        raise atpic.errors.Error404(b'Private DNS ',selldns,b' is not known.')
    # uid=b''
    return uid

def uname2user(uname,rediscon,db):
    yy=atpic.log.setname(xx,'uname2user')
    try:
        query=b"select _user.id from _user where _user._servershort=$1"
        values=[uname,]
        # a prepared statement
        statement=b''
        result1=atpic.libpqalex.pq_prepare(db,statement,query)
        result=atpic.libpqalex.pq_exec_prepared(db,statement,values)
        result=atpic.libpqalex.process_result(result)
        atpic.log.debug(yy,'result',result)
        uid=result[0][b"id"]
    except:
        raise atpic.errors.Error404(b'Could not find user DNS',uname)
    return uid


def get_facet_list(essock,facettype,path,uid):
    # get a list of facets depending on the path
    # can be unit tested for most types
    # note that getting the path facets require a elasticsearch search

    yy=atpic.log.setname(xx,'get_facet_list')
    atpic.log.debug(yy,'input=',(facettype,path))
    if facettype in [b'treenav',b'vtreenav',]:
        path=path.strip(b'/')
        pathtype=facettype[0:-3] # b'tree' or b'vtree'
        pathlist=atpic.elasticsearch_queries.get_facet_path_list_list(essock,uid,path,pathtype)
    elif facettype in [b'blognav']:
        pathlist=atpic.elasticsearch_queries.get_facet_date_list(path)
    elif facettype in [b'geonav']:
        pathlist=atpic.elasticsearch_queries.get_facet_geo_list(path)

    atpic.log.debug(yy,"pathlist=",pathlist)
    return pathlist

def get_json_facet_msearch(facettype,pathlist,uid,aid):
    yy=atpic.log.setname(xx,'get_json_facet_msearch')
    atpic.log.debug(yy,"input=",(facettype,pathlist,uid,aid))
    if facettype in [b'treenav',b'vtreenav']:
        pathtype=facettype[0:-3] # b'path'
        ajson=atpic.elasticsearch_queries.forge_facet_path_list_search(uid,pathlist,aid,pathtype)
    elif facettype in [b'blognav']:
        ajson=atpic.elasticsearch_queries.forge_facet_date_search(pathlist,uid,aid)
    elif facettype in [b'geonav']:
        ajson=atpic.elasticsearch_queries.forge_facet_geo_search(pathlist,uid,aid)
    atpic.log.debug(yy,"output=",ajson)
    return ajson


def display_xml_up(facettype,path):
    # complete the navigation menu with a 'up' path
    yy=atpic.log.setname(xx,'display_xml_up')
    atpic.log.debug(yy,"input=",(facettype,path))
    uppath=b''
    if facettype in (b'treenav',b'vtreenav',):
        if path==b'/':
            uppath=b''
        else:
            splitted=path.split(b'/')
            atpic.log.debug(yy,'splitted',splitted)
            truncated=splitted[:-1]
            atpic.log.debug(yy,'truncated',truncated)
            if truncated==[b'']:
                uppath=b'/'
            else:
                uppath=b'/'.join(truncated)
    elif facettype in (b'blognav',):
        cleaned=atpic.dateutils.remove_nondigits(path)
        atpic.log.debug(yy,'cleaned',cleaned)
        alen=len(cleaned)
        if alen==4:
            uppath=b'/'
        elif alen==6:
            uppath=b'/'+cleaned[0:4]
        elif alen==8:
            uppath=b'/'+cleaned[0:4]+b'/'+cleaned[4:6]
    elif facettype in (b'geonav',):
        splitted=path.split(b'/')
        atpic.log.debug(yy,'splitted',splitted)
        if len(splitted)==5:
            (dummy,xminb,xmaxb,yminb,ymaxb)=splitted
            atpic.log.debug(yy,'(xminb,xmaxb,yminb,ymaxb)=',(xminb,xmaxb,yminb,ymaxb))
            # http://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
            (xmin,xmax,ymin,ymax)=map(atpic.mybytes.bytes2float,(xminb,xmaxb,yminb,ymaxb))
            atpic.log.debug(yy,'(xmin,xmax,ymin,ymax)=',(xmin,xmax,ymin,ymax))
            dx=xmax-xmin
            dy=ymax-ymin
            atpic.log.debug(yy,'dx',dx)
            atpic.log.debug(yy,'dy',dy)
            if dx>=360 or dy>=180:
                pass
            else:
                nxmin=xmin-(dx/2)
                nxmax=xmax+(dx/2)
                nymin=ymin-(dy/2)
                nymax=ymax+(dy/2)
                (uxmin,uxmax,uymin,uymax)=map(atpic.mybytes.float2bytes,(nxmin,nxmax,nymin,nymax))
                atpic.log.debug(yy,'(uxmin,uxmax,uymin,uymax)',(uxmin,uxmax,uymin,uymax))
                uppath=b'/'+b'/'.join((uxmin,uxmax,uymin,uymax))
    xml=b'<up>'+uppath+b'</up>'
    atpic.log.debug(yy,'output',xml)
    return xml




def work_xml_journal(hxplo,pxplo,actions,environ,xmlo,uid,aid):
    yy=atpic.log.setname(xx,'work_xml_journal')
    atpic.log.debug(yy,"input=",(hxplo.list(),pxplo.list(),actions,environ,xmlo,uid,aid))
    xmlo.data.push(b'JOURNAL')
    path=b''
    if pxplo.getmatrix(0,0)==b'journal':
        path=pxplo.getmatrix(0,1)


    query=b"tree:"+path
    pathtype=b'tree'
    # (pathsearchtype,query)=set_searchquery(pxplo,environ,uid)
    atpic.log.debug(yy,"searchquery",query)
    query=atpic.elasticsearch_queries.forge_atpicquery_below(pathtype,path,uid)
    atpic.log.debug(yy,"searchquery",query)
    afrom=b'0'
    size=getperpage(hxplo,actions,environ)
    queryjson=atpic.elasticsearch_queries.query2json(query,aid,afrom,size)
    atpic.log.debug(yy,"queryjson",queryjson)

    xmlo.data.pop()
    return xmlo


def work_xml_belownav(db,essock,hxplo,pxplo,actions,environ,xmlo,uid,aid):
    # first we look the directory facets up
    # using a first elasticesearch search
    # then for each facet we get the sample picture
    # http://alex.atpic.faa/search?q=uid:1&start=2&f=xml
    # http://alex.atpic.faa/search?q=uid:1&start=2&size=1&f=xml

    yy=atpic.log.setname(xx,'work_xml_belownav')
    atpic.log.debug(yy,"input=",(db,hxplo.list(),pxplo.list(),actions,environ,xmlo,uid,aid))

    facettype=pxplo.getmatrix(0,0)
    path=pxplo.getmatrix(0,1)

    # set three variables:
    path=pxplo[facettype]
    atpic.log.debug(yy,"path",path,"pathtype",facettype)

    pathlist=get_facet_list(essock,facettype,path,uid)
    atpic.log.debug(yy,"pathlist",pathlist)

    (xmlo,popnb)=wrap_xmlo_user(db,hxplo,pxplo,uid,xmlo,environ)
    xmlo.data.push(facettype.upper())
    xml=display_xml_up(facettype,path)
    xmlo.data.append(xml)
    if len(pathlist)>0:

        ajson=get_json_facet_msearch(facettype,pathlist,uid,aid)
        atpic.log.debug(yy,"ajson=",ajson)
        
        bjson=atpic.elasticsearch_queries.send_msearch(essock,ajson)
        atpic.log.debug(yy,"bjson",bjson)
        xml=atpic.json_elas2atpic.display_facets(pathlist,bjson,aid)
        xmlo.data.append(xml)
    xmlo.data.pop()
    xmlo=unwrap_xmlo_user(popnb,xmlo)
    atpic.log.debug(yy,"output",xmlo)
    return xmlo


def wrap_xmlo_user(db,hxplo,pxplo,uid,xmlo,environ):
    """
    Used to wrap under a user xml tag
    """
    popnb=0
    if uid!=b'':
        popnb=popnb+1
        xmlo.data.push(b'USER')
        line=get_user_details_from_uid(uid,db)
        depth=1
        actions=[b'get']
        autoresult=b''
        xmlo=display_one_object(line,depth,hxplo,pxplo,actions,xmlo,autoresult,environ)
        # xmlo.data.push(b'id') # could add more than just the uid
        # xmlo.data.append(uid)
        # xmlo.data.pop()
    return (xmlo,popnb)

def unwrap_xmlo_user(popnb,xmlo):
    for apop in range(0,popnb):
        xmlo.data.pop()
    return xmlo

def set_searchquery(pxplo,environ,uid):
    # returns empty b'' query if no search is needed
    yy=atpic.log.setname(xx,'set_searchquery')
    pxplo00=pxplo.getmatrix(0,0)
    if pxplo00==b'search':
        envq=atpic.environment.get_qs_key(environ,b'q',b'') # query
        atpic.log.debug(yy,"envq",envq)
        query=envq
        if uid:
            atpic.log.debug(yy,"we got a uid")
            if envq!=b'':
                atpic.log.debug(yy,"modifying as we got a uid")
                query=query+b' uid:'+uid
        atpic.log.debug(yy,"query2",query)
        pathsearchtype=b'search'
    else:
        path=pxplo.getmatrix(0,1)
        pathsearchtype=pxplo.getmatrix(0,0) # eg. search, geosearch, treesearch, datesearch
        pathtype=pathsearchtype[0:-6]
        atpic.log.debug(yy,"path=",path,"pathtype",pathtype)
        query=atpic.elasticsearch_queries.forge_atpicquery_below(pathtype,path,uid)
    return (pathsearchtype,query)


def work_xml_below(db,essock,hxplo,pxplo,actions,environ,xmlo,uid,aid,compolist):
    # first lookup the gallery id on disk from the path
    yy=atpic.log.setname(xx,'work_xml_below')
    atpic.log.debug(yy,"input=",(db,hxplo.list(),pxplo.list(),actions,environ,xmlo,uid,aid,compolist))
    (pathsearchtype,query)=set_searchquery(pxplo,environ,uid)
    atpic.log.debug(yy,"searchquery",query)
    
    (xmlo,popnb)=wrap_xmlo_user(db,hxplo,pxplo,uid,xmlo,environ)
    xmlo.data.push(pathsearchtype.upper())
    asize=getperpage(hxplo,pxplo,environ) # atpic.environment.get_qs_key(environ,b"size",b'10')
    astart=atpic.environment.get_qs_key(environ,b"start",b'0')
    arank=atpic.environment.get_qs_key(environ,b"rank",b'')
    atpic.log.debug(yy,"navigation is based on (start,size,rank)",(astart,asize,arank))
    if query!=b'':
        try:
            if arank:
                asize_query=b'1'
                astart_query=atpic.mybytes.int2bytes(-1+atpic.mybytes.bytes2int(arank))
            else:
                asize_query=asize
                astart_query=astart
            bjson=atpic.elasticsearch_queries.send_query(essock,query,astart_query,asize_query,uid,aid)
            atpic.log.debug(yy,"bjson",bjson)
            (hits_total,xmlstring,compolist)=atpic.json_elas2atpic.display(bjson,astart,asize,arank,aid,compolist,environ)
            # put in the head the hits number
            xmlo.head.push(b'hits')
            xmlo.head.append(hits_total)
            xmlo.head.pop()
            perpage=getperpage(hxplo,pxplo,environ)
            xmlo.head.append(b'<size>'+perpage+b'</size>')

            if arank==b'':
                xmlo.data.push(b'Pic')
            xmlo.data.append(xmlstring)
            if arank==b'':
                xmlo.data.pop()
        except:
            atpic.log.error(yy,traceback.format_exc())
            atpic.log.error(yy,'we continue anyway')
            
    xmlo.data.pop()
    xmlo=unwrap_xmlo_user(popnb,xmlo)
    # compolist.append(b'http://atpic.com/user')

    return (xmlo,compolist)


def set_path(hxplo,pxplo,actions,environ,depth,line):
    """
    Set the 'url' attribute in the xml response for each object
    """
    yy=atpic.log.setname(xx,'set_path')
    osl=[]
    i=0
    for (key,value) in pxplo.list()[0:depth]:
        i=i+1
        if key==b'user':
            pass
        else: 
            try:
                if key==b'g':
                    key=b'gallery'
                osl.append(key)
                if i<depth:
                    osl.append(value)
            except:
                pass

    osls=b'/'.join(osl)
    # overload some special:
    if pxplo.keys()[0:depth]==[b'user',b'gallery',b'g']:
        osls=b'gallery'
    elif pxplo.keys()[0:depth]==[b'user',b'gallery',b'gallery']:
        osls=b'gallery'

    elif pxplo.keys()[0:depth]==[b'user',b'gallery',b'path']:
        osls=b'gallery'

    if pxplo.keys()[0:depth]==[b'user',]:
        apath=b'http://'+environ[b'HTTP_HOST'][-9:]+b'/user'+osls+b'/'+line[b'id']
    else:
        apath=b'http://'+environ[b'HTTP_HOST']+b'/'+osls+b'/'+line[b'id']

    atpic.log.debug(yy,"set_path(",hxplo,pxplo,actions,environ[b'HTTP_HOST'],depth,line[b'id'],apath,")")

    return apath





def set_pic_urls(hxplo,pxplo,actions,environ,depth,line,secret):
    # creates a dictionnary of pic urls
    yy=atpic.log.setname(xx,'set_pic_urls')
    # res={b'xxurl':b'gggggggggggg'}
    atpic.log.debug(yy,"input=",hxplo,pxplo,actions,environ,depth,line)
    ip=environ[b'SERVER_ADDR']
    plist=list()
    plist.append(b'http://'+ip)
    plist.append(b'u'+pxplo[b'user'])
    plist.append(pxplo[b'gallery'])
    plist.append(secret)
    # if pxplo.keys()==[b'user',b'gallery',b'pic']: # pic collection
    plist.append(line[b'id'])
    # else:
    #     plist.append(pxplo[b'pic'])

    fasturl=b'/'.join(plist)
    res={b'fasturl':fasturl}
    atpic.log.debug(yy,"output=",res)
    return res



def get_form_list_fields(tag):
    """
    For any object (maybe need the full list)
    gives the list of fileds to display
    in a POST form
    need to do also the GET list
    """
    if tag==b'gallery':
        lf=[b'cols',
            b'counter',
            b'css_gallery',
            b'css_pic',
            b'datefirst',
            b'datelast',
            b'dir',
            # 'id', # will be set automatically with the sql INSERT
            b'isroot',
            b'lat',
            b'lon',
            b'mode',
            b'rows',
            b'secret',
            b'skin_gallery',
            b'skin_pic',
            b'style',
            b'template_gallery',
            b'template_pic',
            b'text',
            b'title',
            # 'user', # should not be modifed as it is the parent
            ]
    return lf


def xml_form(pxplo,actions,environ,xmlo):
    # def xml_form(pxplo,new_olist,atype,actions,environ,xmlo):
    yy=atpic.log.setname(xx,'xml_form')
    atpic.log.debug(yy,'entering xml_form(',pxplo,actions,environ,xmlo)
    tag=pxplo.keys()[-1]
    xmlo.data.push(tag)
    tablename=atpic.forgesql.create_tablename(pxplo.keys())

    list_fields=atpic.listfields.get_fields_write(tablename)
    for fi in list_fields:
        xmlo.data.push(fi)
        xmlo.data.pop()
        
    xmlo.data.pop()
    return xmlo

# need to get the atom Slug header to make an easy post with filename
# http://bitworking.org/projects/atom/draft-ietf-atompub-protocol-13.html#rfc.section.9.6
# http://code.google.com/apis/picasaweb/docs/2.0/developers_guide_protocol.html#PostPhotos
#       Slug: plz-to-love-realcat.jpg

# Content-Type: image/jpeg
# Content-Length: 47899
# Slug: plz-to-love-realcat.jpg
# 
# ...binary image data goes here...

def set_tmpdevice(tmpdevice,pxplo,depth,line):
    """
    tmp device: it is better to put files on a tmp directory 
    in the same partition as content
    """
    yy=atpic.log.setname(xx,'set_tmpdevice')
    atpic.log.debug(yy,"setting tmpdevice, intial:" , tmpdevice)
    atpic.log.debug(yy,pxplo)
    atpic.log.debug(yy,depth)
    atpic.log.debug(yy,line)
    if depth==1 and pxplo.getmatrix(0,0)==b"user" and pxplo.getmatrix(0,1):
        atpic.log.debug(yy,"tmpdevice NEEDS CHANGE")
        tmpdevice=b"" # line[b"partition"]
        tmpdevice=tmpdevice+b"/tmp"
    atpic.log.debug(yy,"will return tmpdevice=" , tmpdevice)

    return tmpdevice




def effective_len(pxplo):
    # handles revision
    yy=atpic.log.setname(xx,'effective_len')
    atpic.log.debug(yy,"input=",pxplo.list())
    olist_len=len(pxplo)
    atpic.log.debug(yy,'olist_len1=',olist_len)
    lastone=pxplo.getmatrix(len(pxplo)-1,0)
    if lastone==b'revision':
        olist_len=olist_len-1
    atpic.log.debug(yy,"will return olist_len=" ,olist_len)
    return olist_len

def work_xml_sql_queryvalues(hxplo,pxplo,actions,environ,xmlo,indata,uid,aid):
    """
    Returns a list of [(query,values),] for later execution,
    one element per depth
    Is basically a call to forgesql
    """
    yy=atpic.log.setname(xx,'work_xml_sql_queryvalues')
    atpic.log.debug(yy,'input=',hxplo,pxplo,actions,environ,xmlo,uid,aid)

    pxplo=atpic.xmlutils.set_virtualpxplo(hxplo,pxplo,uid)
    #  for the SQL API, we create a virtual pxplo that has the user id prepended


    olist_len=effective_len(pxplo)

    atpic.log.debug(yy,'olist_len2=',olist_len)
    queryvalues=list()
    if olist_len>0:
        for depth in range(1,olist_len+1):
            atpic.log.debug(yy,"+++++ Depth",depth) 
            # can be unit tested
            mystart=atpic.environment.get_qs_key(environ,b"start",b'0')
            atpic.log.debug(yy,"mystart=",mystart)
            myend=atpic.environment.get_qs_key(environ,b"end",b'0')
            atpic.log.debug(yy,"myend=",myend)
            lang=atpic.lang.get_lang(environ)
            atpic.log.debug(yy,"lang=",lang)

            # can be unit tested
            if mystart!=b'0':
                myfromto=b'from'
            else:
                if myend!=b'0':
                    myfromto=b'to'
                    mystart=myend
                else:
                    myfromto=b'from'

            perpage=getperpage(hxplo,pxplo,environ)
            atpic.log.debug(yy,"perpage=",perpage)
            (query,query_args)=atpic.forgesql.forge_query(pxplo,actions,depth,lang,environ,indata=indata,start=mystart,perpage=perpage,fromto=myfromto,authid=aid)
            atpic.log.debug(yy,'appending',(query,query_args))
            queryvalues.append((query,query_args))

    atpic.log.debug(yy,'will return',queryvalues)
    
    return queryvalues


def work_xml_sql_get_async(query_list):
    yy=atpic.log.setname(xx,'work_xml_sql_get_async')
    result_list=atpic.libpqalex.async_query(query_list)
    atpic.log.debug(yy,'will return:',result_list)
    return result_list

def work_xml_sql_get_sync(db,queryvalues):
    """
    Execute a list of queries synchronously
    """
    yy=atpic.log.setname(xx,'work_xml_sql_get_sync')
    atpic.log.debug(yy,'input',db,queryvalues)
    results=list()
    i=0
    for (query,query_args) in queryvalues:
        i=i+1
        atpic.log.debug(yy,'++++++++++ query',i,'+++++++++++++')
        if query==b"":
            atpic.log.debug(yy,"QUERY IS EMPTY")
            result=list()
            pass
        else:
            atpic.log.debug(yy,query,query_args)
            ps=atpic.libpqalex.pq_prepare(db,b'',query)

            result=atpic.libpqalex.pq_exec_prepared(db,b'',query_args) # query_args is a list
            result=atpic.libpqalex.process_result(result)

        atpic.log.debug(yy,'appending result:', result)
        results.append(result)

    atpic.log.debug(yy,'will return:',result)
    return results

def work_xml_sql_get_pipe(db,queryvalues):
    """
    Execute a list of queries synchronously
    """
    yy=atpic.log.setname(xx,'work_xml_sql_get_sync')
    results=list()
    # send all queries in one go (pipeline)
    for (query,query_args) in queryvalues:
        if query==b"":
            atpic.log.debug(yy,"QUERY IS EMPTY")
            query=b'SELECT 1 as _one'

        ps=atpic.libpqalex.pq_send_query_params(db,query,query_args)

    # fetch the results
    for (query,query_args) in queryvalues:
        result=atpic.libpqalex.pq_get_result(db) # query_args is a list
        result=atpic.libpqalex.process_result(result)
        atpic.log.debug(yy,'appending result:', result)
        results.append(result)

    atpic.log.debug(yy,'will return:',result)
    return results

def work_xml_sql_get(db,queryvalues):
    """
    Get the results executing the sql queries
    Asynchronously for get and synchronously for put,post,delete
    """
    yy=atpic.log.setname(xx,'work_xml_sql_get')
    results=work_xml_sql_get_sync(db,queryvalues)
    # results=work_xml_sql_get_async(queryvalues)
    # results=work_xml_sql_get_pipe(db,queryvalues)
    return results


def getperpage(hxplo,pxplo,environ):
    # this is rather fast: it may be called more than once for the same component
    yy=atpic.log.setname(xx,'getperpage')
    atpic.log.debug(yy,"input=",(hxplo.list(),pxplo.list(),environ))
    perpage=atpic.environment.get_qs_key(environ,b"size",b'10')
    if atpic.mybytes.bytes2int(perpage)>100:
        perpage=b'100'
    if hxplo.list()==[(b'atpiccom', None)] and pxplo.list()==[(b'search', None)]:
        atpic.log.debug(yy,"match atpic.om/search")
        if b'w=HOME' in environ.get(b'QUERY_STRING',b''):
            atpic.log.debug(yy,"match w=HOME")
            perpage=b'7'
    elif pxplo.list()==[(b'search', None)] :
        if b'w=HOME' in environ.get(b'QUERY_STRING',b''):
            perpage=b'7'

    atpic.log.debug(yy,"output= (perpage) =",perpage)
    return perpage

def boundaries_startend(result,hxplo,pxplo,environ):
    # can be unit tested
    # eliminates the first and last if necessary
    loopstart=0
    loopend=len(result)
    hasnext=False
    hasprevious=False
    yy=atpic.log.setname(xx,'boundaries_startend')

    mystart=atpic.environment.get_qs_key(environ,b"start",b'0')
    atpic.log.debug(yy,"mystart=",mystart)
    myend=atpic.environment.get_qs_key(environ,b"end",b'0')
    atpic.log.debug(yy,"myend=",myend)
    perpage=getperpage(hxplo,pxplo,environ)
    mystart_int=atpic.mybytes.bytes2int(mystart)
    myend_int=atpic.mybytes.bytes2int(myend)
    perpage_int=atpic.mybytes.bytes2int(perpage)
    if len(result)>1:
        firstid=result[0][b'id']
        firstid_int=atpic.mybytes.bytes2int(firstid)
        lastid=result[len(result)-1][b'id']
        lastid_int=atpic.mybytes.bytes2int(lastid)
        if mystart_int>0:
            if firstid_int<=mystart_int:
                hasprevious= True # xmlo.data.append(b'<hasprevious/>') # hasmore
                loopstart=1 # do not display the first one
                if len(result)>perpage_int+1: # 11
                    hasnext=True # xmlo.data.append(b'<hasnext/>') # hasmore
                    loopend=perpage_int+1 # 11
            else:
                if len(result)>perpage_int: # 10
                    hasnext=True # xmlo.data.append(b'<hasnext/>') # hasmore
                    loopend=perpage_int # 10
        elif myend_int>0:
            if lastid_int >= myend_int:
                hasnext=True # xmlo.data.append(b'<hasnext/>') # hasmore
                loopend=len(result)-1
                if len(result)>perpage_int+1: # 11:
                    hasprevious= True # xmlo.data.append(b'<hasprevious/>') # hasmore
                    loopstart=1
            else:
                if len(result)>perpage_int: # 10:
                    hasprevious= True # xmlo.data.append(b'<hasprevious/>') # hasmore
                    loopstart=1
        elif mystart_int==0 and myend_int==0:
            if len(result)>perpage_int: # 10:
                hasnext=True # xmlo.data.append(b'<hasnext/>') # hasmore
                loopend=perpage_int # 10
    return (loopstart,loopend,hasprevious,hasnext)


def work_xml_sql_show(hxplo,pxplo,actions,environ,xmlo,results,autoresult,uid):
    # there is one result per depth
    # NO sql or redis is needed here
    tmpdevice=b"/tmp"
    secret=b''
    yy=atpic.log.setname(xx,'work_xml_sql_show')
    atpic.log.debug(yy,"input=",(hxplo.list(),pxplo.list(),actions,environ,xmlo,results,autoresult))
    # need to have the virtual
    pxplo=atpic.xmlutils.set_virtualpxplo(hxplo,pxplo,uid)
    # olist_len=len(pxplo)
    olist_len=effective_len(pxplo)

    if olist_len>0:
        for depth in range(1,olist_len+1):
            atpic.log.debug(yy,"+++++ Depth",depth)
            result=results[depth-1]
            # get the input, when this is the max depth and put/post, 
            # can be unit tested
            # this can be unit tested
            lastobject=pxplo.getmatrix(depth-1,0) # the object at the depth rank
            if result==list():
                atpic.log.debug(yy,"RESULT IS EMPTY")
                # it may be normal e.g. if ['get','post']
                if depth==olist_len:
                    if actions==['get','post']:
                        xmlo=xml_form(pxplo,actions,environ,xmlo)
                is_end_collection=check_end_collection(depth,pxplo,actions)
                if is_end_collection:
                    atpic.log.debug(yy,'end of empty collection, write it anyway')
                    xmlo.data.push(lastobject[0:1].upper()+lastobject[1:]) # push Gallery
                    xmlo.data.pop()

                lastid=pxplo.getmatrix(depth-1,1)
                if len(result)==0 and (depth<olist_len or (depth==olist_len and lastid!=None)):
                    atpic.log.debug(yy,'result is zero (depth, olist_len, getmatrix)',(depth,olist_len,lastid))
                    raise atpic.errors.Error404(lastobject,lastid,b"could not be found")



            else:
                # result
                is_end_collection=check_end_collection(depth,pxplo,actions)
                if is_end_collection:
                    xmlo.data.push(lastobject[0:1].upper()+lastobject[1:]) # push Gallery
                atpic.log.debug(yy,"result111",result)
                atpic.log.debug(yy,"result111 length",len(result))
                # hasmore?
                # one before, 10 lines, one after
                
                loopstart=0
                loopend=len(result)
                if is_end_collection:
                    (loopstart,loopend,hasprevious,hasnext)=boundaries_startend(result,hxplo,pxplo,environ)
                    
                    if hasprevious: 
                        xmlo.head.append(b'<hasprevious/>')
                    if hasnext:
                        xmlo.head.append(b'<hasnext/>')
                    perpage=getperpage(hxplo,pxplo,environ)
                    xmlo.head.append(b'<size>'+perpage+b'</size>')
                for line in result[loopstart:loopend]:
                    tmpdevice=set_tmpdevice(tmpdevice,pxplo,depth,line)
                    # os.makedirs(tmpdevice,exist_ok=True) # too expensive
                    newdic={}
                    if lastobject==b'gallery':
                        secret=line[b'_secret']
                    if depth<olist_len:
                        xmlo.data.push(lastobject.upper(),newdic) # set the url= in the XML xmlo
                    else:
                        xmlo.data.push(lastobject,newdic)
                    atpic.log.debug(yy,"line:",line)
                    xmlo=display_one_object(line,depth,hxplo,pxplo,actions,xmlo,autoresult,environ)
                    if is_end_collection: # in a collection we close each element
                        xmlo.data.pop()
                if is_end_collection:
                    xmlo.data.pop() # pop Gallery

    for ai in range(0,len(xmlo.data.stack)):
        xmlo.data.pop()

    return xmlo





def display_dataerror(dataerror,xmlo):
    yy=atpic.log.setname(xx,'display_dataerror')
    if dataerror:
        atpic.log.debug(yy,'has dataerror')
        haserror=True
        xmlo.error.append(b"<code>400</code>") # what is the correct code???
        xmlo.error.append(b"<message>Data Error</message>")
        xmlo.error.push(b'dataerror')
        for key in dataerror.keys():
            xmlo.error.push(key)
            for message in dataerror[key]:
                xmlo.error.push(b'message')
                xmlo.error.append(message)
                xmlo.error.pop()
            xmlo.error.pop()
        xmlo.error.pop()
    else:
        pass
    return xmlo

def set_sqldataerror(dataerror,sqlerror):
    yy=atpic.log.setname(xx,'set_sqldataerror')
    atpic.log.debug(yy,'input=',(dataerror,sqlerror))
    # dataerror[b'login']=[b'BBBBBBloginAY',]
    if sqlerror[b'sqlstate']==b'23505': # unique constraint violation
        match=re.search(b'__u_([^"]+)"',sqlerror[b'primary'])
        if match:
            field=match.group(1)
            atpic.log.debug(yy,'match on',field)
            if field not in dataerror.keys():
                dataerror[field]=[]
            dataerror[field].append(b'Unique key violation on '+field)
        else:
            dataerror[b'generic']=[b'Generic unique constraint violation',]
    atpic.log.debug(yy,'output=',dataerror)
    return dataerror

def work_xml_sql(rediscon,db,indata,dataerror,hxplo,pxplo,actions,environ,xmlo,uid,aid,autoresult):
    # NEW
    # WARNING: this is not unit tested!
    # try to avoid modifying this code
    # and post process the XML file generated

    # need to extract forgesql and lipqalex to be able 
    # 1) to unit test
    # 2) to have the choice between
    #    parallel async sql queries and just serial queries

    yy=atpic.log.setname(xx,'work_xml_sql')
    atpic.log.debug(yy,'input=',(rediscon,db,indata,dataerror,hxplo,pxplo,actions,environ,xmlo,uid,aid,autoresult))

    # do not raise an exception as we need to re-present the form
    # (haserror,xmlo)=display_dataerror(dataerror,xmlo)

    # newactions is a trick used to present again the SQL data in the form
    newactions=actions_transform(actions,dataerror)
    atpic.log.debug(yy,'newactions',newactions)
    # get the SQL queries and arguments to execute:
    queryvalues=work_xml_sql_queryvalues(hxplo,pxplo,newactions,environ,xmlo,indata,uid,aid)
    atpic.log.debug(yy,'(queryvalues)=',(queryvalues))

    # execute the SQL queries, first try:
    sqlerror=None
    try:
        results=work_xml_sql_get(db,queryvalues) # get the values from SQL
    except atpic.libpqalex.Fatal as e:
        atpic.log.debug(yy,'FATALerror',e.state) # if =b'23505', then unique constraint violation
        sqlerror=copy.deepcopy(e.state)

    if sqlerror:
        # try again
        dataerror=set_sqldataerror(dataerror,sqlerror)
        newactions2=actions_transform(actions,dataerror)
        atpic.log.debug(yy,'newactions2',newactions2)
        # get the SQL queries and arguments to execute:
        queryvalues=work_xml_sql_queryvalues(hxplo,pxplo,newactions2,environ,xmlo,indata,uid,aid)
        atpic.log.debug(yy,'(queryvalues)2=',(queryvalues))
        results=work_xml_sql_get(db,queryvalues) # get the values from SQL

    # present them in a XML
    xmlo=work_xml_sql_show(hxplo,pxplo,actions,environ,xmlo,results,autoresult,uid)
    # if haserror: need to replace the sql values by the form values
    # and fill the <error> xmlo
    xmlo=display_dataerror(dataerror,xmlo)
    atpic.log.debug(yy,'xmlo.data.content=',(b''.join(xmlo.data.content)))
    atpic.log.debug(yy,'output=',(xmlo))
    return (xmlo,dataerror)

def set_presentation_head(hxplo,pxplo,xmlo,environ):
    yy=atpic.log.setname(xx,'set_presentation_head')
    xmlo.head.append(b'<presentation>')
    xmlo.head.append(b'<column>3</column>')
    xmlo.head.append(b'</presentation>')


def set_authorization_head(xmlo,autor,gallerymode,isauthenticated,isfriend,isowner,isauthor,isadmin,isinsecret,autoresult):
    yy=atpic.log.setname(xx,'set_authorization_head')
    xmlo.headauthorization.stack=[]
    xmlo.headauthorization.content=[]
    xmlo.headauthorization.append(b'<mode>',autor,b'</mode>',sep='')
    if gallerymode:
        xmlo.headauthorization.append(b'<gallerymode>',gallerymode,b'</gallerymode>',sep='')
    xmlo.headauthorization.append(b'<useris>')
    if isauthenticated:
        xmlo.headauthorization.append(b'<authenticated/>')
    if isfriend:
        xmlo.headauthorization.append(b'<friend/>')
    if isowner:
        xmlo.headauthorization.append(b'<owner/>')
    if isauthor:
        xmlo.headauthorization.append(b'<author/>')
    if isadmin:
        xmlo.headauthorization.append(b'<admin/>')
    if isinsecret:
        xmlo.headauthorization.append(b'<insecret/>')

    xmlo.headauthorization.append(b'</useris>')
    xmlo.headauthorization.append(b'<result>'+autoresult+b'</result>')

def get_username_password(actions,indata):
    yy=atpic.log.setname(xx,'get_username_password')
    username=atpic.indatautils.get(indata,b'username',b'')
    password=atpic.indatautils.get(indata,b'password',b'')
    atpic.log.debug(yy,"output=", (username,password))
    return (username,password)

def form_display_xml_login(username,password,xmlo):
    xmlo.data.append(b"<login><username>",username,b"</username><password>",password,b"</password></login>",sep=b'')
    return xmlo

def work_xml_login(hxplo,pxplo,actions,environ,indata,xmlo,headers,authenticated,details,aid):
    # need headers to store the session cookie
    # curl -d "username=myuser&password=mypass" "http://atpic.faa/login?f=xml"
    # curl -d "username=myuser&password=mypass" "http://atpic.faa/login?f=xml&redirect=false"
    yy=atpic.log.setname(xx,'work_xml_login')
    atpic.log.debug(yy,"input=",(hxplo,pxplo,actions,environ,indata,xmlo,headers,authenticated,details,aid))
    (username,password)=get_username_password(actions,indata)
    if actions==[b'post']:
        xmlo=process_login_details(username,password,hxplo,pxplo,actions,environ,xmlo,headers,authenticated,details,aid)
    else:
        # this is a GET
        xmlo=form_display_xml_login(username,password,xmlo)

    atpic.log.debug(yy,"output=",(headers,xmlo))
    return xmlo

def get_session_from_setcookie(headers):
    yy=atpic.log.setname(xx,'get_session_from_setcookie')
    atpic.log.debug(yy,"input=",headers)
    session=b''
    for (name,value) in headers:
        if name==b'Set-Cookie':
            if value.startswith(b'session='):
                pattern=re.compile(b'session=([^;]+);')
                b=pattern.match(value)
                session=b.group(1)
    atpic.log.debug(yy,"output=",session)
    return session

def process_login_details(username,password,hxplo,pxplo,actions,environ,xmlo,headers,authenticated,details,aid):
    # check that username and password entered are correct
    # if correct create a sesssion
    # store the cookie
    # and may generate a service ticket
    yy=atpic.log.setname(xx,'process_login_details')
    atpic.log.debug(yy,"input",(username,password,hxplo,pxplo,actions,environ,xmlo,headers,authenticated,details,aid))
    if authenticated:
        atpic.log.debug(yy,"6",headers)
        session=get_session_from_setcookie(headers)
        xmlo.data.append(b"<session>",session,b"</session>",sep='') # NEED TO GET session from cookie
        atpic.log.debug(yy,"7",session)
        # there are several kinds of redirect:
        # 3 cases:
        # ===========
        # 1) no parameter: redirect to alex.atpic.com
        # 2) redirect=false: no redirect
        # 3) redirect=http://pdns.com, redirect to pdns.com + service ticket
        (aid,servershort,name)=details
        (doredirect,url,headers)=atpic.authenticatecrypto.login_redirect(headers,servershort,environ)
        atpic.log.debug(yy,"8",(doredirect,url,headers))
        if doredirect:
            raise atpic.errors.Error302(url,headers)
    else:
        # there was an error: bad login
        # redisplay the form with some error code
        xmlo.error.append(b"<code>401</code>")
        xmlo.error.append(b"<message>Bad login</message>")
        xmlo=form_display_xml_login(username,password,xmlo)
    atpic.log.debug(yy,"output=",(headers,xmlo))
    return xmlo



def compolist_faa(compolist,environ):
    """
    Replaces .com in host names with .faa
    Look at xsllib.py too
    """
    compolist2=[]
    tld=atpic.parameters.get_tld(environ)
    if tld!=b'.com':
        pattern=re.compile(b'([^:]+)://([^/]+)\.com')
        for ele in compolist:
            newele=pattern.sub(b'\\1://\\2.faa',ele)
            compolist2.append(newele)
    else:
        compolist2=compolist
    return compolist2

def compolist_init(hxplo,pxplo,actions,autor,environ,capabilities):
    """
    Easy to unit test
    """
    compolist=[]
    yy=atpic.log.setname(xx,'compolist_init')
    atpic.log.debug(yy,hxplo,pxplo,actions,autor,environ,capabilities,sep=',')
    if hxplo.keys()==[b'atpiccom'] and pxplo.list()==[]:
        atpic.log.debug(yy,"Doing Atpic HOME1 (composite)")
        # compolist.append(b'http://atpic.com/login')
        compolist.append(b'http://atpic.com/search?q=sort:random&amp;w=HOME')
        # compolist.append(b'http://atpic.com/news')

    elif hxplo.keys()==[b'uname'] and pxplo.keys()==[] :
        atpic.log.debug(yy,"Doing USER HOME1 (composite)")
        # we do NOT need the uid, 
        # as search below alex.atpic.com/search gets the uid
        compolist.append(b"http://"+hxplo[b'uname']+b".atpic.com/search?q=sort:random&amp;w=HOME")

    elif hxplo.keys()in ([b'legacy'],[b'legacyobject']):
        atpic.log.debug(yy,"Legacy not supported")
        raise atpic.errors.Error404(b'Legacy url not supported.')
    elif hxplo.keys()==[b'selldns'] and pxplo.keys()==[] :
        atpic.log.debug(yy,"Doing USER HOME SELLDNS (composite)")
        # we do NOT need the uid, 
        # as search below alex.atpic.com/search gets the uid
        compolist.append(b"http://"+hxplo[b'selldns']+b"/search?q=sort:random&amp;w=HOME")
    elif pxplo.getmatrix(0,0) in [b'tree',b'vtree',b'blog',b'geo']: # belownav
        mtype=pxplo.getmatrix(0,0)
        alen=len(mtype)
        rank=atpic.environment.get_qs_key(environ,b"rank",b'')
        if rank==b'':
            compolist.append(b"http://"+environ[b"HTTP_HOST"]+b"/"+mtype+b"nav"+environ[b'PATH_INFO'][alen+1:]+b"?w="+mtype.upper())
        compolist.append(b"http://"+environ[b"HTTP_HOST"]+b"/"+mtype+b"search"+environ[b'PATH_INFO'][alen+1:]+b"?w="+mtype.upper())

    else:
        atpic.log.debug(yy,"Doing normal URLs (non composite)")
        compolist.append(b"http://"+environ[b"HTTP_HOST"]+environ[b'PATH_INFO'])

    atpic.log.debug(yy,'will return',compolist)
    return compolist



def check_allowed_hvalues_basic(hxplo,pxplo):
    # this can be unit tested
    # make some checks on (key,val) pairs that we know will fail in SQL
    # because of incorrect format
    # this is PRE-PROCESSING (pre sql)
    yy=atpic.log.setname(xx,'check_allowed_hvalues_basic')

    notvalid=b''
    atpic.log.debug(yy,'input=',hxplo.list(),',',pxplo.list())
    for (key,val) in pxplo.list():
        atpic.log.debug(yy,'key,val',key,val)
        if val:
            if key in [b'faq',b'tree',b'treenav',b'treesearch',b'vtree',b'vtreenav',b'vtreesearch',b'blog',b'blognav',b'blogsearch',b'geo',b'geonav',b'geosearch',b'journal',b'wiki',b'reset']:
                pass
            elif key in [b'revision']:
                # we expect numbers or number,number
                if not re.match(b"^[0-9]+$", val) and not re.match(b"^[0-9]+,[0-9]+$", val):
                    atpic.log.debug(yy,'invalid!')
                    notvalid=b"value '"+val+b"' is not valid for key '"+key+b"'"

            else:
                # we expect numbers
                if not re.match(b"^[0-9]+$", val):
                    atpic.log.debug(yy,'invalid!')
                    notvalid=b"value '"+val+b"' is not valid for key '"+key+b"'"
                else:
                    atpic.log.debug(yy,'valid...')
        else:
            atpic.log.debug(yy,'none is valid')
    atpic.log.debug(yy,'output=',notvalid)
    return notvalid

def check_allowed_hvalues(hxplo,pxplo):
    yy=atpic.log.setname(xx,'check_allowed_hvalues')
    res=check_allowed_hvalues_basic(hxplo,pxplo)
    if res==b'':
        atpic.log.debug(yy,'Ok');
    else:
        atpic.log.debug(yy,'NOTOk');
        raise atpic.errors.Error404(res)


def block_ifreadonly_and_write(hxplo,pxplo,actions,readonly,aid):
    # raises an exception if try to write to a readonly system
    # now the read only feature
    # readonly=atpic.parameters.get_readonly()
    # THIS can easily be Unit Tested: does not depend on config
    #  and not DB connection
    if readonly and not atpic.autorize.check_authenticated_isadmin(aid):
        # we need to limit
        pxplo00=pxplo.getmatrix(0,0)
        if pxplo00 != b'login':
            for aaction in actions:
                if aaction in [b'put',b'delete',b'post']:
                    raise atpic.errors.Error404(b"HTTP verb",aaction,b"is not supported; System is in read-only mode.")
                    # pass

def check_allowed_function(hxplo,pxplo,actions):
    yy=atpic.log.setname(xx,'check_allowed_function')
    atpic.log.debug(yy,'input=',(hxplo.list(),pxplo.list(),actions))
    # check we support this call (avoid accessing hidden tables)
    # this is PRE PROCESSING
    signature=atpic.dispatcher.signature(hxplo,pxplo,actions)
    atpic.log.debug(yy,'signature',signature)
    if signature not in atpic.allowed_objects.allowed_signatures:
        raise atpic.errors.Error404(b"pattern ",signature,b" is not valid")

    # for aaction in actions:
    #    if aaction not in atpic.allowed_objects.actions_list:
    #        raise atpic.errors.Error404("HTTP verb",aaction,"is not supported")





def inject_authentication(details):
    yy=atpic.log.setname(xx,'inject_authentication')
    atpic.log.debug(yy,"input",details)
    xmle=atpic.xmlob.Xmle() # elementary object
    xmle.append(b"<authentication>")
    xmle.append(b"<uid>",details[0],b"</uid>",sep='')
    xmle.append(b"<short>",details[1],b"</short>",sep='')
    xmle.append(b"<displayname>",details[2],b"</displayname>",sep='')
    xmle.append(b"</authentication>")
    output=b''.join(xmle.content)
    atpic.log.debug(yy,"output",output)
    return output


def inject_capabilities(capabilities):
    xmle=atpic.xmlob.Xmle()
    xmle.push(b"capabilities")
    for key,value in capabilities.items():
        xmle.push(key)
        xmle.append(value)
        xmle.pop()
    xmle.pop()
    output=b''.join(xmle.content)
    return output

def inject_exploded(xmlo,hxplo,pxplo):
    xmlo.head.push(b"exploded")
    longlist=hxplo.items()+pxplo.items()
    for key,value in longlist:
        xmlo.head.push(b'item')
        xmlo.head.push(b'key')
        xmlo.head.append(key)
        xmlo.head.pop()
        xmlo.head.push(b'value')
        if value:
            xmlo.head.append(value)
        xmlo.head.pop()
    for key,value in longlist:
        xmlo.head.pop()

    xmlo.head.pop()
    return xmlo



def set_uid_from_host(hxplo,pxplo,rediscon,db):
    yy=atpic.log.setname(xx,'set_uid_from_host')
    atpic.log.debug(yy,"input",(hxplo.list(),pxplo.list(),rediscon,db))
    if hxplo.haskey(b'uname'):
        atpic.log.debug(yy,"transforming uname into uid")
        uname=hxplo.getkey(b'uname')
        uid=uname2user(uname,rediscon,db)
        # create a new path xplotded with 'user' prepended; NOT GOOD
        # pxplo=atpic.xplo.Xplo([(b'user',uid),]+pxplo.list())
        # atpic.log.debug(yy,"new pxplo",pxplo)
    elif hxplo.haskey(b'selldns'):
        atpic.log.debug(yy,"transforming selldns into uid")
        selldns=hxplo.getkey(b'selldns')
        uid=selldns2user(selldns,rediscon,db)
        # create a new path xplotded with 'user' prepended
        # pxplo=atpic.xplo.Xplo([(b'user',uid),]+pxplo.list())
        atpic.log.debug(yy,"new pxplo",pxplo)
    else:
        uid=b''
    atpic.log.debug(yy,"uidis",uid)
    atpic.log.debug(yy,"output=",uid)
    return uid


def work_xml_authenticate(rediscon,db,hxplo,pxplo,actions,environ,indata,headers): 
    """
    This calls the authentication layer (except for composite)
    This raises an exception if not authenticated.
    If authenticated sets a boolen and returns a list of user details.
    """
    yy=atpic.log.setname(xx,'work_xml_authenticate')
    atpic.log.debug(yy,"input=",(rediscon,db,hxplo,pxplo,actions,environ,headers))
    authenticated=False
    details=()
    (authenticated,details,headers)=atpic.authenticatecrypto.authenticate(db,hxplo,pxplo,actions,environ,indata,headers)
    atpic.log.debug(yy,"output=", (authenticated,details,headers))
    return (authenticated,details,headers)


def authenticate_any(db,hxplo,pxplo,rediscon,actions,environ,indata,headers):
    # get the uid based on env
    yy=atpic.log.setname(xx,'authenticate_any')
    atpic.log.debug(yy,"input",(db,hxplo,pxplo,rediscon,actions,environ,headers))
    # authenticate
    (authenticated,details,headers)=work_xml_authenticate(rediscon,db,hxplo,pxplo,actions,environ,indata,headers) # WHY DO YOU NEED HEADERS?????? to set a cookie
    try:
        (aid,servershort,name)=details
    except:
        (aid,servershort,name)=(b'',b'',b'')
    atpic.log.debug(yy,"output=",(headers,authenticated,details,aid))
    return (headers,authenticated,details,aid)

def iswiki_error(hxplo,pxplo):
    yy=atpic.log.setname(xx,'iswiki_error')
    atpic.log.debug(yy,'input=',(hxplo.list(),pxplo.list()))
    iswiki=False
    wiki404=b''
    if b'wiki' in pxplo.keys():
        iswiki=True
        wiki404=b'<wikierror/>'
    atpic.log.debug(yy,'output=',(iswiki,wiki404))
    return (iswiki,wiki404)

def work_xml(db,essock,rediscon,hxplo,pxplo,actions,autor,environ,indata,capabilities,headers,authenticated,details,aid,compolist):
    """
    Returns a string (not bytes, not file)
    """
    # headers: headers to output (a list that will be modified and returned)
    # 'format' and 'showxsl' are passed in environ['QUERY_STRING'] 
    # not in environ['PATH_INFO']
    # lang: from header, IP or cookie (preferences)
    # file:///home/madon/doc/python-3.3a0-docs-html/library/http.cookies.html
    # wiki: from cookie (preferences)
    # format: from QUERY_STRING, or header, or user agent
    # resolution: from cookie, or host name e.g. r600.alex.atpic.com
    # (useful to GET pictures on filesystem, mod_rewrite can work on cookies though)
    # showxsl: from QUERY_STRING
    # start (page): from QUERY_STRING
    # id: from HTTP_HOST, PATH_INFO (via dispatcher)

    yy=atpic.log.setname(xx,'work_xml')
    atpic.log.debug(yy,'input=',(db,rediscon,hxplo.list(),pxplo.list(),actions,autor,environ,capabilities,headers,authenticated,details,aid))
    # we store in a XML object
    xmlo=atpic.xmlob.Xmlo() # create a Xml Object to store the head, error and data parts
    atpic.log.debug(yy,"1 environ1",environ)
    try:
        # is it a known function?, raise a atpic.errors.Error404 if not
        # some PRE PROCESSING:
        check_allowed_function(hxplo,pxplo,actions)
        check_allowed_hvalues(hxplo,pxplo)



        # at this stage we have aid the authenticated ID or b'' and uid the uname (site) uiserid or b''

        uid=set_uid_from_host(hxplo,pxplo,rediscon,db) # NOT AUTHENTICATION!!!!!

        # authorization:
        # at this stage we have user and gallery if necessary
        # if gallery in pxplo.keys()
        # get gallery mode (friend, private or public)
        # if mode is friend, then check authenticated user is a friend (SQL)
        pxplovirtual=atpic.xmlutils.set_virtualpxplo(hxplo,pxplo,uid)
        (autor,gallerymode,isauthenticated,isfriend,isowner,isauthor,isadmin,isinsecret,autoresult)=atpic.autorize.autorize(pxplovirtual,actions,autor,environ,authenticated,details,db)  # need virtual pxplo
        # set the authorization in head
        set_authorization_head(xmlo,autor,gallerymode,isauthenticated,isfriend,isowner,isauthor,isadmin,isinsecret,autoresult)


        xmlo.head.append(dispatcher_toxml(hxplo,pxplo,actions))
        set_presentation_head(hxplo,pxplo,xmlo,environ)
        if autoresult==b'notauthorized':
            raise atpic.errors.Error401(b'Not autorized')


        # dispatch using the 'atype' value
        # we first do special non composite stuff:
        
        pxplo00=pxplo.getmatrix(0,0)
        pxplo10=pxplo.getmatrix(1,0)
        

        atpic.log.debug(yy,"2 (pxplo00,pxplo10)=",(pxplo00,pxplo10))

        rank=atpic.environment.get_qs_key(environ,b"rank",b'')
        atpic.log.debug(yy,'2a rank=',rank)



        if pxplo00==b"faq":
            xmlo=work_xml_faq(db,hxplo,pxplo,actions,environ,xmlo)
            atpic.log.debug(yy,"3 Doing FAQQ")
        elif pxplo00==b"login":
            atpic.log.debug(yy,"4 Doing special login")
            xmlo=work_xml_login(hxplo,pxplo,actions,environ,indata,xmlo,headers,authenticated,details,aid) # was cookieslist
        elif pxplo00==b"reset":
            xmlo.data.append(b'<reset/>')
            atpic.log.debug(yy,"4 reset xmlo=",xmlo)

        # navigation
        elif pxplo00 in [b'treenav',b'vtreenav',b'blognav',b'geonav']:
            atpic.log.debug(yy,"5 Doing NAVIGATION")
            xmlo=work_xml_belownav(db,essock,hxplo,pxplo,actions,environ,xmlo,uid,aid)
        elif pxplo00 in [b'search',b'treesearch',b'vtreesearch',b'blogsearch',b'geosearch']:
            atpic.log.debug(yy,"6 Doing BELOW1")
            (xmlo,compolist)=work_xml_below(db,essock,hxplo,pxplo,actions,environ,xmlo,uid,aid,compolist)
        elif pxplo00 in [b'journal',]:
            atpic.log.debug(yy,"7 Doing journal")
            xmlo=work_xml_journal(hxplo,pxplo,actions,environ,xmlo,uid,aid)
        else:
            atpic.log.debug(yy,"8 Doing EEELSE")
            # more PRE-PROCESSING
            indata2=copy.deepcopy(indata) # use deepcopy as dictionary with lists
            (indata2,dataerror)=atpic.validate.validate(rediscon,db,indata2,hxplo,pxplo,actions,environ)
            atpic.log.debug(yy,"8c indata2",indata2,dataerror)
            atpic.log.debug(yy,'8d (indata,indata2)',(indata,indata2))
            # processing in SQL
            (xmlo,dataerror)=work_xml_sql(rediscon,db,indata2,dataerror,hxplo,pxplo,actions,environ,xmlo,uid,aid,autoresult)
            atpic.log.debug(yy,'9a xmlo.data.content=',(b''.join(xmlo.data.content)))
            # POST PROCESSING:
            atpic.log.debug(yy,'9b (indata,indata2)',(indata,indata2))
            if dataerror: # there are errors, reuse original indata
                atpic.log.debug(yy,'10a There were ERRORS!',dataerror)
                (xmlo,headers)=atpic.validate.postprocessing_error(indata,dataerror,hxplo,pxplo,actions,environ,xmlo,headers,uid)
                atpic.log.debug(yy,'10b xmlo.data.content=',(b''.join(xmlo.data.content)))
            else: # there are no errors
                xmlo=atpic.processinfiles.process_infiles(xmlo,actions,indata,db)
                atpic.log.debug(yy,'11a xmlo.data.content=',(b''.join(xmlo.data.content)))
                (xmlo,headers)=atpic.validate.postprocessing_noerror(indata2,hxplo,pxplo,actions,environ,xmlo,headers,uid) # was cookieslist instead of headers both in input and output
                atpic.log.debug(yy,'11b xmlo.data.content=',(b''.join(xmlo.data.content)))

            xmlo=atpic.captcha.postprocessing(rediscon,dataerror,hxplo,pxplo,actions,xmlo)
            xmlo=atpic.wikidiff.postprocessing(hxplo,pxplo,actions,xmlo)
            xmlo=atpic.wiki_rst.postprocessing(db,hxplo,pxplo,actions,xmlo,aid,uid,environ)
            xmlo=atpic.sendmail.postprocessing(dataerror,hxplo,pxplo,actions,indata,environ,xmlo)
            # xmlo=atpic.wikicaching.postprocessing(hxplo,pxplo,actions,xmlo)
            atpic.log.debug(yy,'12 xmlo.data.content=',(b''.join(xmlo.data.content)))
            atpic.needindex.indexweb(rediscon,hxplo,pxplo,actions)
            atpic.stats.update_stats(rediscon,hxplo,pxplo,actions)
            atpic.journal.update_journal(essock,hxplo,pxplo,actions,indata,environ,uid,aid,b''.join(xmlo.data.content))
    except atpic.errors.DataError as e:
        xmlo.data_flush()
        xmlo.error.push(b"code")
        xmlo.error.append(b"401")
        xmlo.error.pop()
        xmlo.error.push(b"message")
        xmlo.error.append(b"Data error")
        xmlo.error.pop()
        atpic.log.error(yy,traceback.format_exc())

    except atpic.errors.Error401 as e:
        atpic.log.info('ERROR401',e.args)
        xmlo.data_flush()
        xmlo.error.push(b"code")
        xmlo.error.append(b"401")
        xmlo.error.pop()
        xmlo.error.push(b"message")
        # xmlo.error.append(b' '.e.args)
        xmlo.error.append(*e.args)
        xmlo.error.pop()

    except atpic.errors.Error404 as e:
        atpic.log.info('ERROR404',e.args)
        xmlo.data_flush()
        xmlo.error.push(b"code")
        xmlo.error.append(b"404")
        xmlo.error.pop()
        xmlo.error.push(b"message")
        xmlo.error.append(b' '.join(e.args)) # xmlo.error.append(*e.args)
        xmlo.error.pop()
        # mark a wiki 404 to make wiki page creation easier
        (iswiki,wiki404)=iswiki_error(hxplo,pxplo)
        if iswiki: 
            xmlo.error.append(wiki404)


    except atpic.libpqalex.Fatal as e:
        xmlo.data_flush()
        xmlo.error.push(b"code")
        xmlo.error.append(b"401")
        xmlo.error.pop()
        xmlo.error.push(b"message")
        xmlo.error.append(b"SQL error")
        xmlo.error.pop()
        xmlo.error.push(b"sqlcode")
        xmlo.error.append(e.state[b'sqlstate']) # if =b'23505', then unique constraint violation
        # see http://www.postgresql.org/docs/9.1/static/errcodes-appendix.html
        # happens when POST twice the same file name in a gallery
        xmlo.error.pop()
        atpic.log.error(yy,'SQLFatal error',e.state)
        atpic.log.error(yy,traceback.format_exc())
    except urllib.error.URLError as e: # solr error
        xmlo.data_flush()
        xmlo.error.push(b"code")
        xmlo.error.append(b"501")
        xmlo.error.pop()
        xmlo.error.push(b"message")
        xmlo.error.append(b"Index error")
        xmlo.error.pop()
        atpic.log.error(yy,traceback.format_exc())

    finally:
        # clean up:
        pass
    output=xmlo.getvalue(hxplo,pxplo,actions,autor,environ)
    atpic.log.debug(yy,"endtype",type(output))

    return (headers,output,compolist)



if __name__ == "__main__":
    print("alex","madon",sep="")
