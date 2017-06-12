#!/usr/bin/python3
"""
Authentication functions 
It authenticates based on a session: no SQL needed.
"""

import hashlib
import random
import time
import math
import crypt
import re
import string
import base64
from http import cookies


import atpic.authenticatesql
from atpic.mybytes import *
import atpic.log


xx=atpic.log.setmod("INFO","authenticate")


def session_make(userid):
    yy=atpic.log.setname(xx,'session_make')
    atpic.log.debug(yy,'userid',userid)
    string=b''
    for i in range(5):
        type = random.randint(1,3);
        if type == 1:
            string = string + chr(random.randint(48,57)).encode('utf8'); 
            # for capital(rand(65,90))
            # for small caps(rand(97,122))
        if (type == 2 or type == 3): 
            string = string + chr(random.randint(97,122)).encode('utf8');
    randompart=string
    atpic.log.debug(yy,"randompart",randompart)
    mytime=time.time()
    timepart=int2bytes(int(mytime/3600))
    hashpart=session_hashpart_make(userid,timepart,randompart)
    sessionid=b'-'.join((userid,timepart,randompart,hashpart))
    atpic.log.debug(yy,'session_make',sessionid)
    return sessionid

def session_hashpart_make(userid,timepart,randompart):
    yy=atpic.log.setname(xx,'session_hashpart_make')
    atpic.log.debug(yy,"input:",userid,timepart,randompart)
    toencode=userid+b"keytoEncrypTmd5"+randompart+b"TimePart"+timepart
    # toencode_bytes=toencode.encode("utf8")
    m=hashlib.md5()
    m.update(toencode)
    hexd=m.hexdigest()
    res=hexd[0:20].encode('utf8')
    atpic.log.debug(yy,"will return:",res)
    return res

def secret_make():
    # see PHP function make_new_secret_id()
    # returns a 'secret' used to hide the path of private galleries
    yy=atpic.log.setname(xx,'secret_make')
    string=b""
    for i in range(20):
        string = string + chr(random.randint(97,122)).encode('utf8')
    atpic.log.debug(yy,"will return",string)
    return string

def session_validate(session):
    # validates a session
    # if valid session returns the UID
    # else returns an exception
    # see PHP function get_id($sessionid,$table,$socket)
    yy=atpic.log.setname(xx,'session_validate')
    atpic.log.debug(yy,'session_validate %s' % session)
    mytime=time.time()
    hour=int(mytime/3600)
    (userid,timepart,randompart,hashpart)=session.split(b'-')
    atpic.log.debug(yy,userid,timepart,randompart,hashpart)
    if len(session)<10:
        atpic.log.debug(yy,' session %s not in the right format' % session)
        raise Exception # Your sesssion '$sessionid' is not in the right format! Please make sure you allow cookies from the domain atpic.com.<br/><br/> If you `believe your session should be set correctly, please contact us with the following code:<br/>Session sent: $sessionid.
    if (int(timepart) < (hour-1)) or (int(timepart) > hour):
        atpic.log.debug(yy,'session too old',session)
        raise Exception # Your session is too old!");//or too new
    if not re.match(b"^[0-9]+$", userid):
        atpic.log.debug(yy,'session has bad user id',session)
        raise Exception # "Bad userid $userid format in session!"
    if not re.match(b"^.{5}$", randompart):
        atpic.log.debug(yy,'session has bad random part',session)
        raise Exception # "Bad randompart $randompart format in session!"
    # allow sessions created this hour or the hour before
    if (hashpart!=session_hashpart_make(userid,timepart,randompart)
        and hashpart!=session_hashpart_make(userid,hour-1,randompart)):
        atpic.log.debug(yy,'session has bad hash part',session)
        raise Exception # send_404("Bad session!");
    uid=int2bytes(int(userid))
    atpic.log.debug(yy,"will return",uid)
    return uid
#
#
#


def base64username_encode(uid,username,displayname):
    """
    returns a base64 encoded string of a serailzation of 
    uid,username,displayname
    """
    yy=atpic.log.setname(xx,'base64username_encode')
    atpic.log.debug(yy,"input:",(uid,username,displayname))
    astring=uid+b'|'+username+b'|'+displayname # contraint: no | in usernames
    # astring=astring.encode("utf8")

    encoded = base64.b64encode(astring)
    # encoded=encoded.decode("utf8")
    atpic.log.debug(yy,"will return:",encoded)
    return encoded

def base64username_decode(encoded):
    yy=atpic.log.setname(xx,'base64username_decode')
    atpic.log.debug(yy,"input:",encoded)
    # encoded=encoded.encode("utf8")
    astring = base64.b64decode(encoded)
    # astring=decoded.decode("utf8")
    splitted=astring.split(b'|')
    atpic.log.debug(yy,splitted)
    # splitted[0]=int(splitted[0])
    res=tuple(splitted)
    atpic.log.debug(yy,"will return:",res)
    return res


def base64session_hashpart_make(encoded):
    """
    Takes the md5 of a (base64 encoded) string
    """
    yy=atpic.log.setname(xx,'base64session_hashpart_make')
    atpic.log.debug(yy,"input:",encoded)
    toencode=b"mybase64"+encoded
    # toencode_bytes=toencode.encode("utf8")
    m=hashlib.md5()
    m.update(toencode)
    hexd=m.hexdigest()
    atpic.log.debug(yy,"hexd",hexd)
    res=hexd[0:10].encode('utf8')
    atpic.log.debug(yy,"will return",res)
    return res

def base64session_make(uid,username,displayname):
    yy=atpic.log.setname(xx,'base64session_make')
    atpic.log.debug(yy,"input:",(uid,username,displayname))
    encoded=base64username_encode(uid,username,displayname)
    hashed=base64session_hashpart_make(encoded)
    session=encoded+b'-'+hashed
    atpic.log.debug(yy,"will return:",session)
    return session

def base64session_validate(session):
    # split with -
    yy=atpic.log.setname(xx,'base64session_validate')
    atpic.log.debug(yy,"input",session)
    splitted=session.split(b'-')
    # check that md5 of base64 part matches md5 part
    base64part=splitted[0]
    md5part=splitted[1]
    atpic.log.debug(yy,'md5part',md5part)
    md5part_expected=base64session_hashpart_make(base64part)
    atpic.log.debug(yy,'md5part_expected',md5part_expected)
    if md5part == md5part_expected:
        atpic.log.debug(yy,'validddd')
        res=(True,base64username_decode(base64part))
    else:
        res=(False,())
    atpic.log.debug(yy,"will return:",res)
    return res


# FULL session
# http://stackoverflow.com/questions/686217/maximum-on-http-header-values
# http://stackoverflow.com/questions/1097651/is-there-a-practical-http-header-length-limit
# For Apache, I found this Server Limits for Apache Security article that lists these directives:
# 
#   # allow up to 100 headers in a request
#   LimitRequestFields 100
#   # each header may be up to 8190 bytes long
#   LimitRequestFieldsize 8190

def fullsession_make(userid,username,displayname):
    yy=atpic.log.setname(xx,'fullsession_make')
    atpic.log.debug(yy,"input:",(userid,username,displayname))
    session=session_make(userid)
    base64session=base64session_make(userid,username,displayname)
    fullsession=session+b'-'+base64session
    atpic.log.debug(yy,"will return",fullsession)
    return fullsession

def fullsession_validate(fullsession):
    yy=atpic.log.setname(xx,'fullsession_validate')
    atpic.log.debug(yy,"input:",fullsession)
    valid=False
    details=()
    try:
        splitted=fullsession.split(b'-')
        atpic.log.debug(yy,'splitted',splitted)
        session_splitted=splitted[0:4]
        atpic.log.debug(yy,'session_splitted',session_splitted)

        base64session_splitted=splitted[4:]
        atpic.log.debug(yy,'base64session_splitted',base64session_splitted)
        session=b'-'.join(session_splitted)
        base64session=b'-'.join(base64session_splitted)
        atpic.log.debug(yy,'fullsession_validate session',session)
        atpic.log.debug(yy,'fullsession_validate base64session',base64session)
        
        uid=session_validate(session)
        (valid,details)=base64session_validate(base64session)
    except:
        atpic.log.debug(yy,'there was an exception',)
        # raise
    atpic.log.debug(yy,"result:",(valid,details))
    return (valid,details)





def authenticate_session(environ):
    # try authenticate by session (cookie, header) and by HTTP Basic auth
    # needs to return:
    # userid,username,displayname
    # if authentication is successful
    # so that it can be stored in the XML response
    yy=atpic.log.setname(xx,'authenticate_session')
    atpic.log.debug(yy,"input",environ)
    session=get_session(environ)
    atpic.log.debug(yy,'authenticate_session %s' % session)
    atpic.log.debug(yy,'session is %s' % session)
    # (1, (True, [1, 'alexmadon', 'Alex Madon']))=fullsession_validate(session)
    (valid,details)=fullsession_validate(session)
    #
    atpic.log.debug(yy,"will return",(valid,details))
    return (valid,details)

def authenticate(environ,db):
    yy=atpic.log.setname(xx,'authenticate')
    atpic.log.debug(yy,'authenticate', environ)
    success=False
    details=()

    (success,details)=authenticate_session(environ)
    if not success:    
        (success,details)=authenticate_basic(environ,db)
    atpic.log.debug(yy,'will return: (success , details)= ' , (success,details))
    return (success,details)

if __name__ == "__main__":
    encoded=base64username_encode(b'1',b'alexmadon',b'Alex Madon')
    print(encoded)
    base64username_decode(encoded)
    session=base64session_make(b'1',b'alexmadon',b'Alex Madon')
    print(session)
    valid=base64session_validate(session)
    print('valid',valid)
    fullsession=fullsession_make(b'1',b'alexmadon',b'Alex Madon')
    print('fullsession',fullsession)
    res=fullsession_validate(fullsession)
    print(res)
