import traceback
import os
import uwsgi
import ssl

import atpic.zmq_elastic_client
import atpic.log
import atpic.redis_pie
import atpic.libpqalex



xx=atpic.log.setmod("INFO","globalcon")

global essock
global rediscon
global db
global requestid
global mysslcontext

def set_essock():
    global essock
    yy=atpic.log.setname(xx,'set_essock')
    try:
        essock=atpic.zmq_elastic_client.connect_first()
        atpic.log.debug(yy,'essock',essock)
    except:
        essock=None
        atpic.log.error(yy,traceback.format_exc())

def set_rediscon():
    global rediscon
    yy=atpic.log.setname(xx,'set_rediscon')
    try:
        rediscon=atpic.redis_pie.connect_first()
        atpic.log.debug(yy,'rediscon',rediscon.getsockname())
    except:
        rediscon=None
        atpic.log.error(yy,traceback.format_exc())

def set_db():
    global db
    yy=atpic.log.setname(xx,'set_db')
    try:
        db=atpic.libpqalex.db_native()
        atpic.log.debug(yy,'db',db)
    except:
        atpic.log.error(yy,traceback.format_exc())

def set_mysslcontext():
    global mysslcontext
    yy=atpic.log.setname(xx,'set_mysslcontext')
    try:
        mysslcontext=ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        atpic.log.debug(yy,'mysslcontext',mysslcontext)
    except:
        atpic.log.error(yy,traceback.format_exc())

def myconnect():
    global requestid
    yy=atpic.log.setname(xx,'myconnect')
    atpic.log.info(yy,'entering myconnect')
    atpic.log.info(yy,'setting global connections')
    set_essock()
    set_rediscon()
    set_db()
    set_mysslcontext()
    requestid=0
    atpic.log.info(yy,'leaving myconnect')

def incr():
    global requestid
    yy=atpic.log.setname(xx,'incr')
    atpic.log.debug(yy,'trying to increment counter')
    requestid=requestid+1
    atpic.log.debug(yy,'requestid',requestid)
    # if requestid==10:
    #     atpic.log.debug(yy,'RELOADING AT 10')
    #     uwsgi.reload()
    return requestid
