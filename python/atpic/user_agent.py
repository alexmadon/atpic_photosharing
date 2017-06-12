# py3k version
"""
Tries to identify mobile devices based on user agent

NOT used any more: user wurfl instead
"""

# http://detectmobilebrowsers.mobi/
import re

def parse_header(environ):
    ismobile=False

    if "HTTP_USER_AGENT" in environ:


        p=re.compile(r"""
ipod|iphone
|android
|opera\ mini
|blackberry
|palm os|palm|hiptop|avantgo|plucker|xiino|blazer|elaine
|windows
|windows ce;\ ppc;|windows\ ce;\ smartphone;|windows\ ce;\ iemobile
|up.browser|up.link|mmp|symbian|smartphone|midp|wap|vodafone|o2|pocket|kindle|mobile|pda|psp|treo
""",re.VERBOSE|re.IGNORECASE)

        # p=re.compile("(Windows)",re.IGNORECASE|re.MULTILINE|re.DOTALL,)
        # print environ['HTTP_USER_AGENT']
        m=p.search(environ['HTTP_USER_AGENT'])
        if m:
            print("MATCH")
            ismobile=True
        else:
            print("does not match")

    if not ismobile:
        if "HTTP_ACCEPT" in environ:
            p=re.compile(r"""
text/vnd.wap.wml
|application/vnd.wap.xhtml+xml
""",re.VERBOSE|re.IGNORECASE)
            m=p.search(environ['HTTP_ACCEPT'])
            if m:
                ismobile=True
    if not ismobile:
        if "HTTP_X_WAP_PROFILE" in environ:
            ismobile=True
    if not ismobile:
        if "HTTP_PROFILE" in environ:
            ismobile=True
    return ismobile
