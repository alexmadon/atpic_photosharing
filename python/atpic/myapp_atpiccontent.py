# to TEST with http: http://localhost:8090
# uwsgi_python32 --http-socket :8090  -M -w atpic.myapp_test  -p 1 -z 30 -l 500 -L --callable application
# import uwsgi
import traceback
import atpic.log
import atpic.picur2file

xx=atpic.log.setmod("INFO","appcontent")
# http://stackoverflow.com/questions/11811404/wsgi-file-streaming-with-a-generator
# os.sendfile(out, in, offset, nbytes)
# wsgi.file_wrapper': <built-in function uwsgi_sendfile>
# http://blog.dscpl.com.au/2011/01/testing-wsgifilewrapper-implementation.html
# Graham Dumpleton
# http://projects.unbit.it/uwsgi/wiki/CustomRouting


def fbuffer(f, chunk_size):
    '''Generator to buffer file chunks'''  
    while True:
        chunk = f.read(chunk_size)      
        if not chunk:
            f.close()
            break
        yield chunk

# http://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html
# The primary mechanism for avoiding requests is for an origin server to provide an explicit expiration time in the future, indicating that a response MAY be used to satisfy subsequent requests. In other words, a cache can return a fresh response without first contacting the server. 
# http://stackoverflow.com/questions/13343263/http-cache-headers-cdn-serving-content-that-never-changes
# http://nginx.org/en/docs/http/ngx_http_headers_module.html#expires
# The max parameter sets 'Expires' to the value 'Thu, 31 Dec 2037 23:55:55 GMT', and 'Cache-Control' to 10 years.
# http://stackoverflow.com/questions/3284341/for-cache-control-to-expire-in-10-years-is-using-doc-cssv-128-exactly-the-same
# http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.21
# Expires: Thu, 01 Dec 1994 16:00:00 GMT
# Expires: Thu, 31 Dec 2037 23:55:55 GMT
# Cache-Control: max-age=315360000
def application(environ, start_response):
    yy=atpic.log.setname(xx,'application')
    atpic.log.debug(yy,environ)
    # start_response("200 OK", [('Content-Type','text/html')])
    # server sends a ETag
    # next time client will send:
    # If-None-Match: "686897696a7c876b7e"
    # server responds with 304 Not Modified
    try:
        path='/etc/init.d/rcS'
        (filename,mimetype,etag)=atpic.picur2file.getfilename(environ)
        etag_from_client=environ.get('HTTP_IF_NONE_MATCH','')
        atpic.log.debug(yy,'etag_from_client',etag_from_client)
        if etag.decode('utf8')==etag_from_client:
            atpic.log.info(yy,'304 Not Modified',etag_from_client)
            headers=[]
            start_response("304 Not Modified", headers)
            return b''
        else:
            atpic.log.info(yy,'sending the file: Etag expected:',etag.decode('utf8'),'Etag sent:',etag_from_client)
            fh = open(filename,'rb')
            headers=[]
            headers.append(('Content-Type',mimetype.decode('utf8')))
            headers.append(('ETag',etag.decode('utf8')))
            # headers.append(('Cache-Control','no-transform,public'))
            headers.append(('Cache-Control','no-transform,public,max-age=315360000'))
            headers.append(('Expires','Thu, 31 Dec 2037 23:55:55 GMT'))
            start_response("200 OK", headers)
            return fbuffer(fh,10000)
    except IOError as e:
        atpic.log.error(yy,'error1',e)
        start_response("404 Not Found", [('Content-Type','text/plain')])
        return b'File not found'
    except:
        atpic.log.error(yy,'error decoding',environ['PATH_INFO'])
        atpic.log.debug(yy,'error2',traceback.format_exc())

        start_response("404 Not Found", [('Content-Type','text/plain')])
        return b'File not found'
