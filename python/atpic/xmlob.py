import io
import atpic.log
import atpic.dispatcher
import atpic.worker
import atpic.environment

xx=atpic.log.setmod("INFO","xmlob")




def xmlurl(environ):
    # (hxplo,pxplo,actions,autor)=atpic.dispatcher.dispatcher(environ)
    # this stores the request url in a XML
    output=[]
    tags=[]
    (method,url)=methodurl(environ)
    output.append(b'<request>')
    output.append(b'<method>'+method+b'</method>')
    output.append(b'<url>'+url+b'</url>')
    output.append(b'<scheme>'+environ[b'wsgi.url_scheme']+b'</scheme>')
    output.append(b'<host>'+environ[b'HTTP_HOST']+b'</host>')
    output.append(b'<pathinfo>'+environ[b'PATH_INFO']+b'</pathinfo>')
    output.append(b'<querystring>')
    alist=atpic.environment.get_qs_list(environ)
    for (key,value) in alist:
        output.append(b'<'+key+b'>'+value+b'</'+key+b'>')
    output.append(b'</querystring>')
    output.append(b'</request>')
    return b''.join(output)

def methodurl(environ):
    """
    extracts the HTTP verb and URL from the environ
    """

    # ruri=environ[b'REQUEST_URI']
    # ruri=ruri.replace(b'&',b'&amp;')
    # urlok=environ[b'REQUEST_METHOD']+b'" url="'+environ[b'wsgi.url_scheme']+b'://'+environ[b'HTTP_HOST']+ruri


    url=environ[b'wsgi.url_scheme']+b'://'+environ[b"HTTP_HOST"]+environ[b"PATH_INFO"]
    if environ[b"QUERY_STRING"]:
        qs=environ[b"QUERY_STRING"]
        qs=qs.replace(b'&',b'&amp;')
        url=url+b"?"+qs
    method=environ[b"REQUEST_METHOD"]
    return (method,url)




# ====================================
#        an elementary class
# ====================================

class Xmle():
    # elementary
    def __init__(self):
        self.stack=list() # stores the XML tags, in case of error pop everything
        self.content=list() # io.StringIO() # or io.BytesIO?


    # content append
    # modifies the content only
    def append(self,*args, sep=" ", end=""):
        for arg in args:
            self.content.append(arg)

    # stack append
    # modifies the tag stack and the content
    def push(self,tag,adic={}):
        """
        adic is a dictionnary of attribute of element "tag"
        """
        yy=atpic.log.setname(xx,"stack_append")
        atpic.log.debug(yy,tag,adic)
        self.stack.append(tag)
        self.content.append(b"<" + tag)
        for key in adic.keys():
            self.content.append(b" "+key+b'="'+adic[key]+b'"')
        self.content.append(b">")
        atpic.log.debug(yy,"PPPUS",len(self.stack),tag)
        atpic.log.debug(yy,"PPPus",self.stack)

    # stack pop
    # modifies the tag stack and the content
    def pop(self):
        tag=self.stack.pop()
        self.content.append(b"</"+tag+b">")
        return tag

class Xmlo():
    """
    This is a XML Object
    with a head (authenticated, errors)
    a data
    """
    def __init__(self):
        self.data=Xmle()
        self.composite=Xmle()
        # general head:
        self.head=Xmle()
        # specialized head:
        self.error=Xmle()
        self.headauthentication=Xmle() # we use a special field as we can write to it 
        # at beginning or end
        self.headauthorization=Xmle()

    def data_flush(self):
        """Used to reset the data in case of error"""
        self.data=Xmle()
        pass

    # content append
    def head_append(self,*args, sep=" ", end=""):
        self.head.append(*args)

    def data_append(self,*args, sep=" ", end=""):
        self.data.append(*args)

    def error_append(self,*args, sep=" ", end=""):
        self.error.append(*args)
        
    # stack append
    def datastack_append(self,tag,adic={}):
        """
        adic is a dictionnary of attribute of element "tag"
        """
        yy=atpic.log.setname(xx,"datastack_append")
        atpic.log.debug(yy,tag,adic)
        self.data.push(tag,adic)

    def errorstack_append(self,tag):
        self.error.push(tag)

    def headstack_append(self,tag):
        self.head.push(tag)
        
    # stack pops
    def datastack_pop(self):
        self.data.pop()

    def errorstack_pop(self):
        self.error.pop()

    def headstack_pop(self):
        self.head.pop()


    # def getvalue(self,thefunction,key,adic,olist,atype,actions,autor,environ):
    def getvalue(self,hxplo,pxplo,actions,autor,environ):
        yy=atpic.log.setname(xx,"getvalue")
        atpic.log.debug(yy,'input=',hxplo,pxplo,actions,autor,environ)
        atpic.log.debug(yy,'out_error',self.error.content)
        atpic.log.debug(yy,'out_data',self.data.content)
        atpic.log.debug(yy,'out_head',self.head.content)
        output=[]
        extra=b""
        action0=actions[0]
        action1=actions[-1]

        headstring=b''.join(self.head.content)
        errorstring=b''.join(self.error.content)
        headauthenticationstring=b''.join(self.headauthentication.content)
        headauthorizationstring=b''.join(self.headauthorization.content)
        datastring=b''.join(self.data.content)

        xmlurla=xmlurl(environ)
        output.append(xmlurla)
        if errorstring:
            output.append(b'<error>'+errorstring+b'</error>')
        if headauthenticationstring:
            output.append(headauthenticationstring)
        if headauthorizationstring:
            output.append(b'<authorization>'+headauthorizationstring+b'</authorization>')
        output.append(headstring)

        datawrap=atpic.environment.get_qs_key(environ,b'w',b'') # wrap
        if datastring: # is null on error, but not null if input error
            output.append(b'<'+action0+b'>')
            output.append(b'<'+action1+b'>')
            if datawrap!=b'':
                output.append(b'<'+datawrap+b'>')  
            output.append(b''.join(self.data.content)) # then get the ouput
            if datawrap!=b'':
                output.append(b'</'+datawrap+b'>')
            output.append(b'</'+action1+b'>')
            output.append(b'</'+action0+b'>')
        output.append(b''.join(self.composite.content))
        output=b''.join(output)
        atpic.log.debug(yy,'endtype',type(output))
    
        return output
