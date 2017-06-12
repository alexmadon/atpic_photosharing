#!/usr/bin/python3
import base64
import time
import urllib.parse
from http import cookies
import crypt
import re
import random
import string
import traceback
import zlib
import configparser

import atpic.authenticatesql
import atpic.environment
import atpic.log
import atpic.opensslat
import atpic.mybytes
import atpic.worker
import atpic.parameters
import atpic.getconfig


"""
We implement CAS like authentication. We relaxed CAS restriction of use once on service ticket. Reason: do not want a shared DB.
This is a share nothing.

servicetype can be:
'session': a cookie, or a JSON/XML value
'service': a URL parameter

session: expires when browser closes (CAS) or 1 hour (atpic)
service: short lived (CAS= 5min)

we do not support HTTP Basic on pdns pages.
"""
xx=atpic.log.setmod("INFO","authenticatecrypto")



def mycrypt(password,salt=b''):
    yy=atpic.log.setname(xx,'mycrypt')
    atpic.log.debug(yy,"password,salt=",password,salt)
    salt_length=2
    if salt==b'' or len(salt)!= salt_length:
        chars = string.ascii_lowercase + string.digits
        chars=chars.encode('utf8')
        for i in range(salt_length):
            salt = salt + chr(random.choice(chars)).encode('utf8')
    crypted=crypt.crypt(password.decode('utf8'),salt.decode('utf8'))
    crypted=crypted.encode('utf8')
    atpic.log.debug(yy,'will return crypted=',crypted)
    return crypted

def set_endoflife(ttl):
    """
    ttl: time to life
    return the end of life in seconds
    """
    yy=atpic.log.setname(xx,'set_endoflife')
    atpic.log.debug(yy,'input=',ttl)
    timeseconds=atpic.mybytes.int2bytes(int(time.time())+ttl)
    atpic.log.debug(yy,'output=',timeseconds)
    return timeseconds


def get_key(servicetype,servicename):
    config_array=atpic.getconfig.parse_config()
    key=config_array['crypto_key'].encode('utf8')+servicename+b'-'+servicetype

    return key

def make_cryted_sausage(sausage,key):
    # randomize
    yy=atpic.log.setname(xx,'make_cryted_sausage')
    rint=random.randint(1000,9999)
    rintb=atpic.mybytes.int2bytes(rint)
    
    astring=b'|'.join((rintb,)+sausage) # put display name at the end as there could be a | ?
    atpic.log.debug(yy,'astring',astring)
    # astring=zlib.compress(astring)
    # atpic.log.debug(yy,'compressed astring',astring)


    # blowfish encrypt
    astring_enc=atpic.opensslat.encrypt(astring,key)
    atpic.log.debug(yy,'astring_enc',astring_enc)
    astring_b64 = base64.urlsafe_b64encode(astring_enc)
    atpic.log.debug(yy,'output=',astring_b64)
    return astring_b64

def decode_crypted_sausage(crypted,key):
    yy=atpic.log.setname(xx,'decode_crypted_sausage')
    atpic.log.debug(yy,'input=',(crypted,key))
    # blowfish decrypt
    astring=atpic.opensslat.encrypt(crypted,key,enc=0)
    atpic.log.debug(yy,'astring',astring)
    # astring=zlib.decompress(astring)
    # atpic.log.debug(yy,'decompressed astring',astring)


    splitted=astring.split(b'|') # be careful: should not contain |
    sausage=splitted[1:] # the first element is the random int
    atpic.log.debug(yy,'sausage',sausage)
    return sausage

def make_session(servicetype,servicename,timeseconds,uid,username,displayname):
    """
    servicetype is b'session' or b'service'
    servicename is the HOST name e.g atpic.com or pdns.com
    timeseconds is the end of life in seconds
    """
    yy=atpic.log.setname(xx,'make_session')
    atpic.log.debug(yy,'input=',servicetype,servicename,timeseconds,uid,username,displayname)
    if servicename.endswith(b'.atpic.com'):
        servicename==b'atpic.com'
        
    key=get_key(servicetype,servicename)
    astring_b64=make_cryted_sausage((timeseconds,servicetype,servicename,uid,username,displayname),key)
    return astring_b64

def decode_session(session,servicetype,servicename):
    yy=atpic.log.setname(xx,'decode_session')
    atpic.log.debug(yy,'input',session,servicetype,servicename)
    crypted = base64.urlsafe_b64decode(session)
    key=get_key(servicetype,servicename)
    sausage=decode_crypted_sausage(crypted,key)
    (timeseconds,servicetype,servicename,uid,username,displayname)=sausage
    """
    # blowfish decrypt
    astring=atpic.opensslat.encrypt(crypted,key,enc=0)
    atpic.log.debug(yy,'astring',astring)
    (rintb,timeseconds,servicetype,servicename,uid,username,displayname)=astring.split(b'|')
    # constraint no | in displayname
    """
    atpic.log.debug(yy,'will return=',(servicetype,servicename,timeseconds,uid,username,displayname))
    return (servicetype,servicename,timeseconds,uid,username,displayname)

def check_session_ok(session,servicetype_in,servicename_in):
    # a simple wrapper
    yy=atpic.log.setname(xx,'check_session_ok')
    atpic.log.debug(yy,'+++++++++++++++++++++++++++++')
    atpic.log.debug(yy,'input',(session,servicetype_in,servicename_in))
    try:
        decrypted=decode_session(session,servicetype_in,servicename_in)
        # check the time
        (servicetype,servicename,timeseconds,uid,username,displayname)=decrypted
        atpic.log.debug(yy,'timeseconds',timeseconds)
        if servicetype_in!=servicetype or servicename_in!=servicename:
            atpic.log.debug(yy,'pairs should be the same',(servicetype_in,servicetype),(servicename_in,servicename))
            session_ok=False
        else:
            atpic.log.debug(yy,'type and service are OK')
            timeinsession=atpic.mybytes.bytes2int(timeseconds)
            atpic.log.debug(yy,'timeinsession',timeinsession)
            timenow=int(time.time())
            atpic.log.debug(yy,'timenow',timenow)
            timediff=timeinsession-timenow
            atpic.log.debug(yy,'timediff',timediff)
            if timediff < 0:
                atpic.log.debug(yy,'session too old')
                decrypted=None
                session_ok=False
            else:
                authenticated=True
                session_ok=True
                atpic.log.debug(yy,'session is OK')
    except:
        atpic.log.debug(yy,'session is NOT OK')
        atpic.log.debug(yy,traceback.format_exc())
        decrypted=None
        session_ok=False
    atpic.log.debug(yy,'output=',(session_ok,decrypted))
    return (session_ok,decrypted)


def set_session_cookie(headers,session,cookiedomain):
    yy=atpic.log.setname(xx,'set_session_cookie')
    atpic.log.debug(yy,'input=',(headers,session,cookiedomain))
    headers.append((b'Set-Cookie',b'session='+session+b'; Domain='+cookiedomain+b'; Path=/;'))
    # Set-Cookie: LSID=DQAAAK…Eaem_vYg; Domain=docs.foo.com; Path=/accounts; Expires=Wed, 13-Jan-2021 22:23:01 GMT; Secure; HttpOnly
    atpic.log.debug(yy,'output=',headers)
    return headers


def get_redirect_url(environ):
    yy=atpic.log.setname(xx,'get_redirect_url')
    atpic.log.debug(yy,'input=',(environ))
    url=environ[b'wsgi.url_scheme'] # or b'UWSGI_SCHEME'?
    url=url+b'://'+environ[b'HTTP_HOST']
    # environ[b'PATH_INFO']
    url=url+environ[b'REQUEST_URI']
    return url


def append_service_ticket(url,session):
    # appends a service ticket to an url
    yy=atpic.log.setname(xx,'append_service_ticket')
    atpic.log.debug(yy,'input=',(url,session))
    newurl=b''
    urltuple=urllib.parse.urlsplit(url)
    if urltuple.query==b'':
        newquery=b'?st='+session
    else:
        newquery=b'?'+urltuple.query+b'&st='+session

    newurl=urltuple.scheme+b'://'+urltuple.netloc+urltuple.path+newquery
    atpic.log.debug(yy,"16c tuple",urltuple)
    atpic.log.debug(yy,'16d set a dummy service ticket')
    atpic.log.debug(yy,'output=',newurl)
    return newurl

def login_redirect(headers,servershort,environ):
    # 3 cases:
    # ===========
    # 1) no parameter: redirect to alex.atpic.com
    # 2) redirect=false: no redirect
    # 3) redirect=http://pdns.com, redirect to pdns.com + service ticket
    doredirect=False
    tld=atpic.parameters.get_tld(environ)

    yy=atpic.log.setname(xx,'login_redirect')
    atpic.log.debug(yy,'input=',(headers,servershort,environ))
    url=b''
    # redirect=atpic.environment.get_qs_key(environ,b'redirect',b'') # get it from qs
    redirect=atpic.environment.get_qs_redirect(environ,b'')
    if redirect==b'':
        atpic.log.debug(yy,'redirecting to servershort')
        url=b'http://'+servershort+b'.atpic'+tld
        doredirect=True
    elif redirect==b'false':
        atpic.log.debug(yy,'no redirect asked')
    else:
        atpic.log.debug(yy,'redirect to redirect url',redirect)
        atpic.log.debug(yy,'we need a service ticket')
        doredirect=True
        url=redirect
    atpic.log.debug(yy,'output=',(doredirect,url,headers))
    return (doredirect,url,headers)

def check_redirect(hxplo,pxplo,actions,autor,environ):
    # can be unit tested
    # a redirect can set cookies
    # this is use very early: for both composite and normal XML
    # one that checks if a redirect is needed, 
    # if a service ticket is sent, if a cookie needs to be set
    # pdns does not support HTTP Basic auth
    yy=atpic.log.setname(xx,'check_redirect')
    atpic.log.debug(yy,'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    atpic.log.debug(yy,'input=',(hxplo.list(),pxplo.list(),actions,autor,environ))
    tld=atpic.parameters.get_tld(environ)

    needredirect=False
    url=b''
    headers=[]


    if actions[0]!=b'get':
        atpic.log.debug(yy,'0 action is not get, pass...')
    else:
        pxplo00=pxplo.getmatrix(0,0)
        atpic.log.debug(yy,'0a pxplo00',pxplo00)
        hxplo00=hxplo.getmatrix(0,0)
        atpic.log.debug(yy,'0aa hxplo00',hxplo00)
        if hxplo00 in [b'legacy',b'legacyobject']:
            pass
        elif pxplo00==b'logout':
            atpic.log.debug(yy,'0b pxplo00',pxplo00)
            atpic.log.debug(yy,'0c removing cookies')
            keys=atpic.environment.get_cookies(environ)
            for akey in keys:
                atpic.log.debug(yy,'0d delete cookie',akey,'setting expire in the past')
                headers.append((b'Set-Cookie',akey+b'=dummy; Domain=.atpic'+tld+b'; Expires=Thu, 01 Jan 1970 00:00:00 GMT;'))
            # sent_url=atpic.environment.get_qs_key(environ,b'url',b'') # get it from qs# 
            sent_url=atpic.environment.get_qs_redirect(environ,b'') # get it from qs
            atpic.log.debug(yy,'0e sent_url',sent_url)
            if sent_url!=b'':
                needredirect=True
                url=sent_url
        else:
            session=get_session(environ) # get session from header or cookie
            servicetype=b'session'
            if hxplo00 in [b'atpiccom',b'uname']:
                servicename=b'atpic.com'
            else:
                servicename=hxplo.getmatrix(0,1) # pdns
            atpic.log.debug(yy,'1b servicename',servicename)
            atpic.log.debug(yy,'2 try decoding atpic session')
            (session_ok,decrypted)=check_session_ok(session,servicetype,servicename)
            if session_ok:
                (servicetype,servicename,timeseconds,uid,username,displayname)=decrypted
                atpic.log.debug(yy,'3 decoded OK:',(servicetype,servicename,timeseconds,uid,username,displayname))
                if hxplo00 in [b'atpiccom',b'uname']:
                    # the is a atpic page
                    pxplo00=pxplo.getmatrix(0,0)
                    atpic.log.debug(yy,'pxplo00',pxplo00)
                    if pxplo00==b'redirect':
                        atpic.log.debug(yy,'4a pxplo00 says we need to redirect')
                        # check there is a valid local atpic session (done before)
                        # create a service ticket
                        sent_url=atpic.environment.get_qs_key(environ,b'url',b'') # get it from qs
                        urltuple=urllib.parse.urlsplit(sent_url)
                        servicename=urltuple.netloc
                        servicetype=b'service'
                        atpic.log.debug(yy,'4b servicename',servicename)
                        timeseconds=set_endoflife(60) # TTL 60 seconds
                        new_session=make_session(servicetype,servicename,timeseconds,uid,username,displayname)
                        needredirect=True
                        url=append_service_ticket(sent_url,new_session)
                        atpic.log.debug(yy,'4c url set to',url)
                    else:
                        atpic.log.debug(yy,'5 on atpic we do not need any redirect or cookie set')
                else:
                    atpic.log.debug(yy,'6 on pdns we do not need any redirect or cookie set')
            else:
                atpic.log.debug(yy,'7 failed to validate session',session)
                if hxplo00 not in [b'atpiccom',b'uname']:
                    atpic.log.debug(yy,'checking if there is a valid service ticket in qs')
                    session=atpic.environment.get_qs_key(environ,b'st',b'')
                    servicetype=b'service'
                    (session_ok,decrypted)=check_session_ok(session,servicetype,servicename)
                    if session_ok:
                        (servicetype,servicename,timeseconds,uid,username,displayname)=decrypted
                        atpic.log.debug(yy,'8 service ticket decoded OK:',(servicetype,servicename,timeseconds,uid,username,displayname))
                        atpic.log.debug(yy,'9 create a new session as ST cannot be used')
                        servicetype=b'session'
                        timeseconds=set_endoflife(3600) # TTL 1 hour
                        new_session=make_session(servicetype,servicename,timeseconds,uid,username,displayname)
                        headers=set_session_cookie(headers,new_session,servicename)
                    else:
                        atpic.log.debug(yy,'10 no valid service ticket found')
                        # check is service ticket is marked as notauthenticated
                        if session==b'notauthenticated':
                            atpic.log.debug(yy,'11a there is a dummy serviceticket, no redirect')
                            atpic.log.debug(yy,'11b send a "alreadychecked" cookie')
                            redir_host=environ[b'HTTP_HOST']
                            headers.append((b'Set-Cookie',b'alreadychecked=1; Domain='+redir_host+b';'))
                        elif session!=b'':
                            atpic.log.debug(yy,'11c there was a service ticket but it could not be validated')
                            redir_host=environ[b'HTTP_HOST']
                            headers.append((b'Set-Cookie',b'alreadychecked=1; Domain='+redir_host+b';'))
                        else:
                            # check on pdns if already redirected cookie
                            alreadychecked=atpic.environment.get_cookie(environ,b'alreadychecked')
                            atpic.log.debug(yy,'12 alreadychecked',alreadychecked)
                            if alreadychecked==b'1':
                                atpic.log.debug(yy,'13 has been checked already, no redirect')
                            else:
                                atpic.log.debug(yy,'14 has not been checked, try a redirect')
                                needredirect=True
                                redirecturl=get_redirect_url(environ)
                                atpic.log.debug(yy,'15 redirecturl',redirecturl)
                                query=urllib.parse.urlencode([(b'url',redirecturl),])
                                url=b'http://atpic'+tld+b'/redirect?'+query.encode('utf8')
                else:
                    # this is a atpic page
                    pxplo00=pxplo.getmatrix(0,0)
                    atpic.log.debug(yy,'15 pxplo00',pxplo00,pxplo.list())
                    if pxplo00==b'redirect':
                        atpic.log.debug(yy,'16a we are on atpic /redirect without a valid session')
                        url=atpic.environment.get_qs_key(environ,b'url',b'') # get it from qs
                        atpic.log.debug(yy,'16b url from qs:',url)
                        st=b'notauthenticated'
                        url=append_service_ticket(url,st)
                        needredirect=True

    atpic.log.debug(yy,'17 output',(needredirect,url,headers))

    return (needredirect,url,headers)

def authenticate_nosql(hxplo,pxplo,actions,environ,headers):
    # no SQL here: easy to Unit test!
    # checks is user is authenticated and sets the authenticated user details
    # special urls are /redirect and /login
    # by looking at:
    # 1) authentication header
    # 2) session cookie
    # 3) service ticket
    yy=atpic.log.setname(xx,'authenticate_nosql')
    atpic.log.debug(yy,'input',(hxplo.list(),pxplo.list(),actions,environ,headers))
    authenticated=False
    details=()
    # first we look at a session cookie or header or HTTP basic
    # if session fails to validate: user is not authenticated
    hxplo00=hxplo.getmatrix(0,0)
    atpic.log.debug(yy,'hxplo00',hxplo00)
    if hxplo00 in [b'atpiccom',b'uname']:
        servicename=b'atpic.com'
    else:
        servicename=hxplo00 # pdns

    session=get_session(environ) # get session from header or cookie
    servicetype=b'session'

    # particular case of reset
    pxplo00=pxplo.getmatrix(0,0)
    atpic.log.debug(yy,'pxplo00',pxplo00)
    if pxplo00==b'reset':
        session=pxplo.getmatrix(0,1) # this is the /reset/xzyt special URL
        servicetype=b'session' # temp session (short life)
        atpic.log.debug(yy,'reset session',(session,servicetype))
        tld=atpic.parameters.get_tld(environ)
        cookiedomain=b'.atpic'+tld
        headers=set_session_cookie(headers,session,cookiedomain) # we need a cookie to navigate


    atpic.log.debug(yy,'try decoding atpic session')
    (session_ok,decrypted)=check_session_ok(session,servicetype,servicename)
    if session_ok:
        (servicetype,servicename,timeseconds,uid,username,displayname)=decrypted
        atpic.log.debug(yy,'decoded OK:',(servicetype,servicename,timeseconds,uid,username,displayname))
        authenticated=True
    else:
        atpic.log.debug(yy,'failed to validate session',session)

    if not authenticated and (hxplo00 not in [b'atpiccom',b'uname']):
        atpic.log.debug(yy,'no pdns session found, now checking service ticket')
        service_ticket=atpic.environment.get_qs_key(environ,b'st',None)
        atpic.log.debug(yy,'service_ticket is',service_ticket)
        if service_ticket:
            servicetype=b'service'
            servicename=hxplo00
            atpic.log.debug(yy,'try decoding pdns service_ticket')
            (session_ok,decrypted)=check_session_ok(session,servicetype,servicename)
            if session_ok:
                (servicetype,servicename,timeseconds,uid,username,displayname)=decrypted
                atpic.log.debug(yy,'st decoded OK:',(servicetype,servicename,timeseconds,uid,username,displayname))
                # create a new session cookie local to this pdns
                servicetype=b'session'
                timeseconds=set_endoflife(3600) # TTL 1 hour
                session=make_session(servicetype,servicename,timeseconds,uid,username,displayname)
                # set cookies and headers
                headers=set_session_cookie(headers,session,servicename)
                authenticated=True


    # ---------------------------------------------------------
    # 2 layers: 
    # one that checks if a redirect is need, if a service ticket is sent, if a cookie needs to be set
    # it is called at the top level (composite)

    # one that gets the user details from a session or service ticket
    # it is called at each level (link)

    # 4 classes: /login, /redirect, composite, elementary

    # on pdns pages:
    # try to validate session cookie
    # if session cookie fails to validate, then we look if there is a valid service ticket st
    # if not valid st, then check alreadychecked cookie
    #    if not alreadychecked, then redirect to http://atpic.com/check?return=http://pdns.com/page
    #       on http://atpic.com/check?return=http://pdns.com/page
    #       if has a valid atpic session, then redirect to: http://pdns.com/page?st=ticket
    #       else: redirect to: http://pdns.com/page?checked=true and store a alreadychecked cookie
    #    if alreadychecked, then the user is not authenticated
    # else create a pdns session cookie

    # on pdns pages you have also a link to manually login at:
    # http://atpic.com/login/http/pdns.com/page
    # if login OK, then store a session cookie in atpic.com and redirect to
    # http://pdns.com/page?st=serviceticket
    # (or if local to atpic, to http://atpic.com with no service ticket)

    # ---------------------------------------------------------
    # BAD: 1x1.gif is bad as the first page is always not logged in on pdns.com
    # BADDDDDDDDDDDDDDDDDD: 
    # on pdns pages:
    # try to validate session cookie
    # if session cookie fails to validate, then we look at service ticket
    # if service ticket validates, then set a new session cookie

    # on pdns pages, 
    # first you check if the surfer is already looged in atpic.com
    #  you do a redirect to atpic.com/check?return=http://pdns.com
    # if the user has a valid atpic session cookie, then send a service ticket
    # and log automatically into pdns.com
    # else redirect to atpic.com/login?redirect=http://pdns.com
    # that will redirect to pdns.com with a service ticket
    # BE Carefull to infinite loops!!!!!!
    # or don't do redirects in general: need to press the login link to do a check
    # or do it once only and mark (in cookie or url) that user is not logged in
    # pb with no cookie support (infinite loop)
    # or add a small image: atpic.com/redirect?return=pdns.com/1x1.gif
    # that redirects to to pdns.com/1x1.gif?service_ticket=xxxxxx
    # 1x1 transparent gif is used
    # be careful 1x1 image is not cached
    # http://stackoverflow.com/questions/8671718/shibboleth-and-autologin
    # Problem: that generates a redirect at each page!
    # so needs to be light weight!
    # DIFFICULT: mix private and public content

    # some pages on pdns, you need to be logged in
    # the login page is different from atpic.com/login
    # it point to a atpic.com/login?return=pdns.com
    # pass


    # ---------------------
    # above composite:
    # check for redirect?
    # a redirect is a Location: header but may also contaion othe rheraders like Set-Cookie:
    # There are 2 fcts:
    # one to get display the details (from session cookie or header - or service ticket??)
    # one for the authentication
    # a) single page scenario:
    #     easy
    # b) composite scenario:
    #     need to call before Composite (to redirect) and within each of the composite links

    if authenticated:
        details=(uid,username,displayname)
    atpic.log.debug(yy,'output=',(authenticated,details,headers))
    return (authenticated,details,headers)



# getters

def get_session_from_header(environ):
    """
    Gets from the special header X-Atpic-Session:
    """
    yy=atpic.log.setname(xx,'get_session_from_header')
    session=environ.get(b"HTTP_X_ATPIC_SESSION","")
    atpic.log.debug(yy,'get_session_from_header HTTP_X_ATPIC_SESSION:',session)

    return session
    

def get_session_from_cookie(environ):
    """
    Gets from the cookie:
    """
    yy=atpic.log.setname(xx,'get_session_from_cookie')
    atpic.log.debug(yy,"input",environ)
    session=b''
    try:
        cookieheader=environ.get(b"HTTP_COOKIE",b"")
        atpic.log.debug(yy,'cookieheader',cookieheader)
        C = cookies.SimpleCookie()
        cookieheader=cookieheader.decode('utf8')
        atpic.log.debug(yy,'cookieheader',cookieheader)
        C.load(cookieheader)
        session=C.get("session","")
        atpic.log.debug(yy,'get_session_from_cookie',session)
        session=session.value # this is a Morsel object library/http.cookies.html#morsel-objects
        session=session.encode('utf8')
    except:
        session=b''
    atpic.log.debug(yy,"will return",session)
    return session
    

def get_session(environ):
    """
    Try all the getters in priority
    """
    yy=atpic.log.setname(xx,'get_session')
    atpic.log.debug(yy,"input",environ)
    
    session=get_session_from_header(environ)
    if not session:
        session=get_session_from_cookie(environ)
    atpic.log.debug(yy,"will return",session)
    return session

# authenticators

def authenticate_basic(environ,db):
    # 'HTTP_AUTHORIZATION': 'Basic YWQ6YWQ='
    # client sends:
    # Authorization: Basic YWxleDptYWRvbg==
    yy=atpic.log.setname(xx,'authenticate_basic')
    atpic.log.debug(yy,"input",environ)

    authorizationheader=environ.get(b"HTTP_AUTHORIZATION",b"")
    atpic.log.debug(yy,'Authorization:',authorizationheader)

    pattern=re.compile(b'^Basic +(.*)$')
    match=pattern.match(authorizationheader)
    success=False
    details=()
    if match:
        m1=match.group(1)
        atpic.log.debug(yy,'Match:',m1)
        m1d=base64.urlsafe_b64decode(m1)
        # m1d=m1d.decode('utf8')
        [username,password]=m1d.split(b':')
        atpic.log.debug(yy,'user: ',username)
        atpic.log.debug(yy,'passwd:', password)
        (success,details)=atpic.authenticatesql.check_username_password(username,password,db)
    atpic.log.debug(yy,'will return: (success , details)= ' , (success,details))

    return (success,details)

def authenticate_login(db,actions,environ,indata,headers):
    yy=atpic.log.setname(xx,'authenticate_login')
    tld=atpic.parameters.get_tld(environ)

    (username,password)=atpic.worker.get_username_password(actions,indata)
    (authenticated,details)=atpic.authenticatesql.check_username_password(username,password,db)
    if authenticated:
        atpic.log.debug(yy,"2")
        (aid,servershort,name)=details
        # then generate a session
        servicetype=b'session'
        servicename=b'atpic.com'
        timeseconds=set_endoflife(3600) # needs int
        username=servershort
        displayname=name
        atpic.log.debug(yy,"4",(servicetype,servicename,timeseconds,aid,username,displayname))
        session=atpic.authenticatecrypto.make_session(servicetype,servicename,timeseconds,aid,username,displayname)
        atpic.log.debug(yy,"5",session)
        # set cookies and headers
        cookiedomain=b'.atpic'+tld
        headers=atpic.authenticatecrypto.set_session_cookie(headers,session,cookiedomain)
    return (authenticated,details,headers)

def authenticate(db,hxplo,pxplo,actions,environ,indata,headers):
    # first try to see if there are valid session, headers, cokkies, service ticket
    yy=atpic.log.setname(xx,'authenticate')
    atpic.log.debug(yy,'input=',(db,hxplo,pxplo,actions,environ,headers))
    authenticated=False
    # is that a login page?
    pxplo00=pxplo.getmatrix(0,0)
    if actions[-1]==b'post' and pxplo00==b"login":
        (authenticated,details,headers)=authenticate_login(db,actions,environ,indata,headers)
        atpic.log.debug(yy,'stage0',(authenticated,details,headers))
    if not authenticated:
        # valid session?
        (authenticated,details,headers)=authenticate_nosql(hxplo,pxplo,actions,environ,headers)
        atpic.log.debug(yy,'stage1',(authenticated,details,headers))
    if not authenticated:
        # try sql basic auth
        (authenticated,details)=authenticate_basic(environ,db)
        atpic.log.debug(yy,'stage2 basic:',(authenticated,details))
    atpic.log.debug(yy,'output=',(authenticated,details,headers))
    return (authenticated,details,headers)




if __name__ == "__main__":
    print('hi')
    t1=time.time()
    t2=time.time()
    print(t2-t1)


    sess=make_session(b'session',b'atpic.com',b'1234566',b'1',b'alexmadon',b'Alex M')
    print(sess)
    res=decode_session(sess,b'session',b'atpic.com')
    print(res)

    # =====    
    t3=set_endoflife(300)
    sess=make_session(b'session',b'atpic.com',t3,b'1',b'alexmadon',b'Alex M')
    print('tempses=',sess)
