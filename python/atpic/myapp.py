import sys
import uwsgi
import atpic.globalcon
import atpic.wsgiat
# import logging
# see http://code.google.com/p/modwsgi/wiki/DebuggingTechniques
sys.stdout = sys.stderr

# comment or uncomment this line if you want to log in apache error.log file


# uwsgi_python32 --socket :8090  -M -w  atpic.myapp  -p 1 -z 30 -l 500 -L --callable application
# uwsgi_python32 --socket :8091  -M -w  atpic.myapp  -p 1 -z 30 -l 500 -L --callable application

# append to: /etc/nginx/uwsgi_params 
# uwsgi_param  UWSGI_SCHEME   $scheme;

# to TEST with http: http://localhost:8090
# uwsgi_python32 --http-socket :8090  -M -w atpic.myapp  -p 1 -z 30 -l 500 -L --callable application


# logging.basicConfig(file=sys.stdout,level=logging.DEBUG)

uwsgi.post_fork_hook = atpic.globalcon.myconnect

def application(environ, start_response):
    import atpic.dispatcher
    (status,response_headers,output)=atpic.wsgiat.wsgi(environ)
    start_response(status, response_headers)
    return [output]



# apache returns a "Internal Server Error" if environ['CONTENT_LENGTH']
# to run by command line:
if __name__ == '__main__':
    from paste import httpserver
    httpserver.serve(application, host='127.0.0.1', port=8080)
