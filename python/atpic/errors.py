#!/usr/bin/python3
import atpic.log

xx=atpic.log.setmod("INFO","errors")



# =======================
#     various errors
# =======================

class AnticsrfError(Exception):
    pass    

class AntidosError(Exception):
    pass    

class DataError(Exception):
    pass

class ElasticsearchError(Exception):
    pass

# =======================
#     HTTP errors
# =======================

class Error401(Exception):
    pass

class Error404(Exception):
    pass


class Error413(Exception):
    # should return "413 Request Entity Too Large"
    # error too big
    pass

class Error501(Exception):
    pass

class Error5XX(Exception):
    pass

class Error302(Exception):
    def __init__(self,url,headers):
        # a redirect is basically a Location: header
        # passed as the 'url' parameter
        # plus some other headers (can set a cookie for instance)
        yy=atpic.log.setname(xx,'Error302')
        atpic.log.debug(yy,'redirecting:', url, headers)
        self.url=url
        self.headers=headers

