import traceback
import atpic.log
xx=atpic.log.setmod("INFO","appcss")

# This is a small application that creates the variable part of the CSS
# mainly colors
# the PATH_INFO should avoid the question mark '?' 
def application(environ, start_response):
    yy=atpic.log.setname(xx,'application')
    start_response("200 Ok", [('Content-Type','text/css')])
    return b'/* some style'
