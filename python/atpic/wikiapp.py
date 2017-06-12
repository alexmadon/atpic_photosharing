import atpic.wiki

def application(environ, start_response):
    (status,response_headers,output)=atpic.wiki.wsgi(environ)
    # status="200 Ok"
    # response_headers=[('Content-type', 'text/plain')]
    # output=b'hello'
    start_response(status, response_headers)
    return [output]
