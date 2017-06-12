import re
import traceback
import socket
import hashlib


import atpic.antidos
import atpic.anticsrf
import atpic.dispatcher
import atpic.errors
import atpic.mybytes
import atpic.log
import atpic.worker
import atpic.xplo
import atpic.redis_pie                 
import atpic.globalcon

xx=atpic.log.setmod("INFO","wsgiat")

def wsgi(environ):
    """
    WSGI wrapper and dispatcher
    sets: status,headers,output
    """
    # search for 
    # object (pic, gallery, artist, ...)
    # method (POST, GET)
    # action (view, update, insert, delete, list, manage)
    # format (rss, xhtml, html, xml, json)
    # redirect

    # convert early to bytes

    environ=atpic.mybytes.env2bytes(environ)

    yy=atpic.log.setname(xx,'wsgi')
    try:
        requestid=atpic.globalcon.incr()
        atpic.log.info(yy,'input=',requestid,environ.get(b'REQUEST_METHOD',b''),environ.get(b'HTTP_HOST',b''),environ.get(b'PATH_INFO',b''))
        # atpic.log.info(yy,'input=',environ.get(b'REQUEST_METHOD',b''),environ.get(b'HTTP_HOST',b''),environ.get(b'PATH_INFO',b''))

        atpic.anticsrf.protect(environ) # really fast CSRF protection
        atpic.antidos.blacklist(environ) # really fast blacklist
        # rediscon=get_rediscon() # get redis connection early:
        rediscon=atpic.globalcon.rediscon
        atpic.antidos.protect(rediscon,environ) # protect from DoS using requests counts

        # we take care of HEAD requests
        if environ[b'REQUEST_METHOD']==b'HEAD':
            environ[b'REQUEST_METHOD']=b'GET'

        (hlist,plist,actions,autor)=atpic.dispatcher.dispatcher(environ) # normalize replacing values by names
        hxplo=atpic.xplo.Xplo(hlist)
        pxplo=atpic.xplo.Xplo(plist)
        (status,headers,output)=atpic.worker.work(rediscon,hxplo,pxplo,actions,autor,environ)

    except atpic.errors.AntidosError:
        errmsg=b'You IP has been blacklisted. Please try again later.'
        (status,headers,output)=(b'503 Service Unavailable',[(b'Content-type', b'text/plain')],errmsg)
        atpic.log.info(yy,traceback.format_exc())

    except atpic.errors.AnticsrfError:
        errmsg=b'We are blocking a possible CSRF attack. Please do not try to change the Referer HTTP header.'
        (status,headers,output)=(b'510 Not Extended',[(b'Content-type', b'text/plain')],errmsg)
        atpic.log.info(yy,traceback.format_exc())


    except socket.error:
        errmsg=b'Atpic socket error.'
        (status,headers,output)=(b'503 Service Unavailable',[(b'Content-type', b'text/plain')],errmsg)
        atpic.log.error(yy,traceback.format_exc())
    except:
        errmsg=b'Error: AAAAAAAAAAAlex %s' + traceback.format_exc().encode('utf8')
        m=hashlib.md5()
        m.update(errmsg)
        hexd=m.hexdigest().encode('utf8')
        errmsg=b'Oooops... This is an unexpected error. For more information contact us mentioning error code '+hexd
        (status,headers,output)=(b'401 Internal Error',[(b'Content-type', b'text/plain')],errmsg)
        atpic.log.error(yy,hexd,traceback.format_exc())

    # 503 Service Unavailable
    """
    finally:
        try:
            rediscon.quit()
        except:
            pass
    """
    atpic.log.debug(yy,'output=',status,headers,output)
    # late decoding
    status=status.decode('utf8') # we have bytes and need a string
    headers=atpic.mybytes.headers2string(headers)
    return (status,headers,output)
