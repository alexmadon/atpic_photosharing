
import atpic.log
import atpic.hashat

xx=atpic.log.setmod("INFO","picurl2file")

def extension2mimetype(extension):
    mimetype=b'octet/stream'
    if extension==b'jpg':
       mimetype=b'image/jpeg'
    return mimetype

def getfilename(environ):
    yy=atpic.log.setname(xx,'getfilename')
    atpic.log.debug(yy,'environ',environ)
    pathinfo=environ['PATH_INFO']
    pathinfo=pathinfo.encode('utf8')
    atpic.log.debug(yy,'pathinfo',pathinfo)
    ahash=pathinfo[2:-4] # eliminate [[/{a,b} at the beginning ]] and .jpg at the end
    etag=ahash
    atpic.log.debug(yy,'ahash',ahash)
    astring_dec=atpic.hashat.undohash(ahash)
    atpic.log.debug(yy,'astring_dec',astring_dec)
    partition=pathinfo[1:2]
    atpic.log.debug(yy,'partition',partition)
    startpath=b'/'+partition+b'/'
    filename=startpath+astring_dec[4:]
    atpic.log.debug(yy,'filename',filename)
    extension=pathinfo[-3:]

    atpic.log.debug(yy,'extension',extension)
    mimetype=extension2mimetype(extension)
    atpic.log.debug(yy,'will return=',(filename,mimetype))
    return (filename,mimetype,etag)
