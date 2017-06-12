#!/usr/bin/python3

import atpic.log
import atpic.wurflapi
import atpic.wurflex
from atpic.redisconst import *


xx=atpic.log.setmod("INFO","capabilities")


def set_capabilities(environ,rediscon,essock):
    """
    Set the client device capabilities using wurfl stored in solr and redis
    """
    wurflserial=b''
    yy=atpic.log.setname(xx,'set_capabilities')
    # clean the string
    user_agent=environ.get(b'HTTP_USER_AGENT',b'')
    atpic.log.debug(yy,'user_agent',user_agent)
    if user_agent!=b'':
        user_agent=atpic.wurflex.sxmlw(environ[b'HTTP_USER_AGENT'])
        # we try first redis
        atpic.log.debug(yy,'cleaned user_agent',user_agent)
        wurflserial=atpic.redis_pie._get(rediscon,REDIS_WF_UA+user_agent) # ua_ stands for user agent
        atpic.log.debug(yy,'wurflserial from redis:',wurflserial)
        if not wurflserial:
            atpic.log.debug(yy,"NO wurflserial in redis, let's use elasticsearch")
            wurflserial=b''
            # if does no exist, then search in elasticsearch and store in redis
            try:
                wurflserial=atpic.wurflapi.set_wurfl_elasticsearch(essock,user_agent)
                atpic.log.debug(yy,'search says wurflserial is',wurflserial)
                atpic.log.debug(yy,'saving in redis',REDIS_WF_UA+user_agent,wurflserial)
                atpic.redis_pie._set(rediscon,REDIS_WF_UA+user_agent,wurflserial)
            except:
                atpic.log.error(yy,'wurfl elasticsearch DEAD !!!!!!!!',user_agent)
                # atpic.log.error(yy,traceback.format_exc())
        else:
            atpic.log.debug(yy,"redis knows about this UA, no elasticsearch necessary")
    else:
        atpic.log.error(yy,'user agent is empty!!!!')
    # should choose a lang
    lang=atpic.lang.get_lang(environ)
    # should choose a format
    if wurflserial:
        mime=atpic.wurflapi.extract_mime_from_serial(wurflserial)
        environ[b'WURFL_MIME']=mime

    format=atpic.format.get_format(environ)
    atpic.log.debug(yy,'aformat',format)
    if wurflserial:
        capabilities=atpic.wurflapi.parse_serial(wurflserial)
    else:
        capabilities={}
    capabilities[b'format']=format
    capabilities[b'lang']=lang
    if lang in (b'he',b'ar'): # hebrew of arabic
        direction=b'rtl'
    else:
        direction=b'ltr'
    capabilities[b'dir']=direction
    atpic.log.debug(yy,'capabilities',capabilities)
    return capabilities
