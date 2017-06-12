"""
    validates a dict of user input
    it is used for data INSERT, UPDATE,. so we need to have the exact fields
    we remove the non allowed fields


"""
import re

import atpic.authenticatecrypto
import atpic.captcha
import atpic.log
import atpic.parameters
import atpic.worker
import atpic.indatautils
import atpic.xmlutils

from atpic.redisconst import *
xx=atpic.log.setmod("INFO","validate")

# constraints
# -- constraint _login is lower case and only chars that can be used in DNS
# -- as it is by default copied to _servershort
def validate_remove_silently(indata,hxplo,pxplo,actions,environ):
    # cannotmodify, updatem, change those
    # some fields CANNOT be updated: we block them (remove)
    # like /user/1/gallery/22/pic/333/put
    # should not be able to modify 333,22,1 in the pic tables
    # (except a special move)
    # we do not modify errordata as this function is silent
    yy=atpic.log.setname(xx,'validate_remove_silently')
    atpic.log.debug(yy,'input=',indata,hxplo,pxplo,actions,environ)
    newindata=[]

    # remove captchahidden captchapublic
    # as the should not go into SQL, and they are used only once
    for (key,isfile,value) in indata:
        if not isfile and key in [b'captchahidden',b'captchapublic',b'partition',b'ip',b'id',b'pathstore']:
            pass
        else:
            newindata.append((key,isfile,value))

    atpic.log.debug(yy,'output=',indata)
    return newindata


# ====================================
#  now the classical validation
# ====================================
def not_in(field,indata):
    notin=True
    for (key,isfile,value) in indata:
        if key==field:
            notin=False
        else:
            pass
    return notin

def get_in(field,indata):
    afield=atpic.indatautils.get(indata,field,b'')
    return afield

def mpush(dataerror,field,message):
    yy=atpic.log.setname(xx,'push')
    atpic.log.debug(yy,'input=',dataerror,field,message)
    if field in dataerror.keys():
        dataerror[field].append(message)
    else:
        dataerror[field]=[message,]
    atpic.log.debug(yy,'output=',dataerror)
    return dataerror


def transform_crypt(indata,hxplo,pxplo,actions,environ):
    # this is used a pre processing (before saving into SQL)
    # when a new user is created or an existing user in updated
    # the 'password' that the user entered needs to be encrypted, to be stored in SQL as encrypted
    # we also set default values for name and servershort if let empty
    yy=atpic.log.setname(xx,'transform_crypt')
    atpic.log.debug(yy,'input=(',indata,',',hxplo,',',pxplo,',',actions,',',environ,')')
    if actions == [b'post', b'post'] or  actions == [b'post',] or actions == [b'post', b'put'] or  actions == [b'put',] :
        if (hxplo.list()==[(b'atpiccom', None)] and pxplo.list()==[(b'user', None)]) or (hxplo.list()==[(b'atpiccom', None)] and pxplo.keys()==[b'user']):
            atpic.log.debug(yy,'need to encrypt the password')
            apassword=get_in(b'password',indata)
            apassword_crypted=atpic.authenticatecrypto.mycrypt(apassword)
            indata=atpic.indatautils.update(indata,b'password',apassword_crypted)
            alogin=get_in(b'login',indata)
            defaultpartition=atpic.parameters.get_defaultpartition()
            defaultip=atpic.parameters.get_defaultip()
            if actions == [b'post', b'post'] or  actions == [b'post',]:
                indata=atpic.indatautils.insert_ifnull(indata,b'name',alogin)
                indata=atpic.indatautils.insert_ifnull(indata,b'servershort',alogin)
                indata=atpic.indatautils.insert_ifnull(indata,b'partition',defaultpartition)
                indata=atpic.indatautils.insert_ifnull(indata,b'ip',defaultip)
    return indata

def validate_simple(indata,dataerror,hxplo,pxplo,actions,environ):
    # those are the validation tests that do not require any DB
    # can be unit tested easily
    yy=atpic.log.setname(xx,'validate_simple')
    atpic.log.debug(yy,'input=(',indata,',',dataerror,',',hxplo,',',pxplo,',',actions,',',environ,')')

    if actions == [b'post', b'post'] or  actions == [b'post',]:
        if hxplo.list()==[(b'atpiccom', None)] and pxplo.list()==[(b'user', None)]:
            if not_in(b'login',indata):
                mpush(dataerror,b'login',b'login cannot be empty')
            else:
                alogin=get_in(b'login',indata)
                atpic.log.debug(yy,'login',alogin)
                if not re.match(b"^[0-9a-z]+$", alogin):
                    mpush(dataerror,b'login',b'login should only contain digits and lowercase letters')
            if not_in(b'password',indata):
                mpush(dataerror,b'password',b'password cannot be empty')
            else:
                apass=get_in(b'password',indata)
                if len(apass)<4:
                    mpush(dataerror,b'password',b'password must be longer than 4 characters')

            if not_in(b'email',indata):
                mpush(dataerror,b'email',b'email cannot be empty')
            else:
                aemail=get_in(b'email',indata)
                if len(aemail)<4:
                    mpush(dataerror,b'email',b'email must be longer than 4 characters')
                if not re.match(b'^[a-zA-Z0-9_+=\-\.]+@[a-zA-Z0-9_+=\-\.]+$',aemail):
                    mpush(dataerror,b'email',b'email is not valid')

            if not_in(b'captchapublic',indata):
                mpush(dataerror,b'captchapublic',b'captchapublic cannot be empty')
            if not_in(b'captchapublic',indata):
                mpush(dataerror,b'captchahidden',b'captchahidden cannot be empty')

    if b'title' in atpic.indatautils.keys(indata):
        if atpic.indatautils.get(indata,b'title',b'')==b'Macro4':
            # should append
            mpush(dataerror,b'title',b'title cannot be Macro4')
            mpush(dataerror,b'title',b'title cannot contain 4')
        # if creating a new user: need captcha
    atpic.log.debug(yy,'output=(',indata,',',dataerror,')')
    return (indata,dataerror)

def validate_redis(rediscon,indata,dataerror,hxplo,pxplo,actions,environ):
    # validation tests that require a connection to redis, like captcha
    # captcha
    # when a user ise create (post)
    # the form needs to contain a <captchahid> and a <captchapub>(i.e. in indata)
    # if no captcha: raise error
    # if the is a value, get the hidden value from redis
    # if lenght is OK and if value is the same, then OK
    yy=atpic.log.setname(xx,'validate_redis')
    (indata,dataerror)=atpic.captcha.preprocessing(rediscon,indata,dataerror,hxplo,pxplo,actions,environ)
    return (indata,dataerror)

def validate_sql(db,indata,dataerror,hxplo,pxplo,actions,environ):
    # validation tests that require a SQL connection
    # like unicity on 'login'
    yy=atpic.log.setname(xx,'validate_sql')
    return (indata,dataerror)


def validate(rediscon,db,indata,hxplo,pxplo,actions,environ):
    # WARNING: NOT UNIT tested, but non db parts should
    # some of the validate tests are db based
    # redis (captcha)
    # sql (unique contraints)
    # note in SQL another strategy would be to relay only on SQL exceptions
    yy=atpic.log.setname(xx,'validate')
    atpic.log.debug(yy,'input=',(rediscon,db,indata,pxplo,actions,environ))
    dataerror={}

    (indata,dataerror)=validate_redis(rediscon,indata,dataerror,hxplo,pxplo,actions,environ)
    (indata,dataerror)=validate_sql(db,indata,dataerror,hxplo,pxplo,actions,environ)
    (indata,dataerror)=validate_simple(indata,dataerror,hxplo,pxplo,actions,environ)
    indata=validate_remove_silently(indata,hxplo,pxplo,actions,environ)
    if not dataerror:
        indata=transform_crypt(indata,hxplo,pxplo,actions,environ)
    atpic.log.debug(yy,'output',indata,dataerror)
    return (indata,dataerror)



def postprocessing_noerror(indata,hxplo,pxplo,actions,environ,xmlo,headers,uid):
    """
    When we have a dataerror at 'post' or 'put' time, 
    we need to redisplay the form with the values entered by the user
    """
    yy=atpic.log.setname(xx,'postprocessing')
    atpic.log.debug(yy,'input=',indata,hxplo,pxplo,actions,environ,xmlo,uid)
    # if this is a user creation, create a session
    if actions == [b'post', b'post'] or  actions == [b'post',] or actions == [b'post', b'put'] or  actions == [b'put',] :
        if hxplo.list()==[(b'atpiccom', None)] and pxplo.list()==[(b'user', None)]:
            pass
    # get id from xml
    """
    xml_string=b''.join(xmlo.data.content)
    uid=atpic.xmlutils.get(xml_string,b'/user/id')
    name=indata[0][b'name'][0]
    servershort=name
    (headers,xmlo,session)=atpic.worker.check_loginok_session(uid,servershort,name,xmlo,headers)
    """
    return (xmlo,headers)

def postprocessing_error(indata,dataerror,hxplo,pxplo,actions,environ,xmlo,headers,uid):
    """
    When we have a dataerror at 'post' or 'put' time, 
    we need to redisplay the form with the values entered by the user
    """
    yy=atpic.log.setname(xx,'postprocessing')
    atpic.log.debug(yy,'input=',indata,dataerror,hxplo,pxplo,actions,environ,xmlo,uid)
    atpic.log.debug(yy,'we have a data error, need path')
    # we need to modify the XML and replace the values we got from SQL
    # by the values the user entered
    basepath=atpic.xmlutils.get_deepest_path(hxplo,pxplo,actions,uid)
    # now take an array of user entered values:
    anarray=atpic.indatautils.setdic(indata)
    xml_string=b''.join(xmlo.data.content)
    xml_string=atpic.xmlutils.replace_params(xml_string,basepath,anarray)
    # update the XML with what we have found
    xmlo.data.content=[xml_string,]
    xmlo.data.stack=[]
    return (xmlo,headers)
