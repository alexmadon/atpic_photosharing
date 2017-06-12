# to TEST with http: http://localhost:8090
# uwsgi_python32 --http-socket :8090  -M -w atpic.myapp_test  -p 1 -z 30 -l 500 -L --callable application


def application(environ, start_response):
    # start_response("200 OK", [('Content-Type','text/html')])
    start_response("200 OK", [])
    # return b"Hello, uwsgi works!<br>"+environ.__str__().encode('utf8')

    out=[]
    #for i in range(0,100000):
    #    out.append(b'hellllo 11111111111111111111111111111111111111111111111')
    out.append(b'Hello')
    return b'\n'.join(out)
