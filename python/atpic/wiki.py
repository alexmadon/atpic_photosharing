import atpic.environment
import atpic.log
import atpic.mybytes
import atpic.wikipandoc
import atpic.wikigit
import atpic.xsllib
import atpic.worker

xx=atpic.log.setmod("INFO","wiki")


def wsgi(environ):
    """
    WSGI wrapper and dispatcher
    sets: status,headers,output
    """
    yy=atpic.log.setname(xx,'wsgi')
    # convert early to bytes
    environ=atpic.mybytes.env2bytes(environ)

    (status,headers,output)=wsgi_bytes(environ)

    # now transforms:
    status=status.decode('utf8') # we have bytes and need a string
    headers=atpic.mybytes.headers2string(headers)
    atpic.log.debug(yy,'')
    return (status,headers,output)


def xsl_transform(xml):
    # used for Log formatting to HTML
    xsl=atpic.xsllib.declare(b'xhtml')
    xsl+=b"""
<xsl:template match="Log">
<div>
<xsl:apply-templates/>
</div>
</xsl:template>

<xsl:template match="log">
<div>
Author: <xsl:value-of select="author_name"/><br/>
Date <xsl:value-of select="date"/><br/>
Message: <xsl:value-of select="message"/><br/>
ID: <xsl:value-of select="id"/><br/>
</div>
</xsl:template>

</xsl:stylesheet>
"""
    output=atpic.worker.xslt_apply_dyna(xsl,xml)
    return output

def do_get(afile,aformat,arev):
    yy=atpic.log.setname(xx,'do_get')
    status=b'200 Ok'
    headers=[(b'Content-type', b'text/html')]
    (output,err)=atpic.wikigit.send_git([b'git',b'show',b'HEAD:'+afile])
    if err:
        output=err
    if aformat==b'html':
        headers=[(b'Content-type', b'text/html')]
        (output,err)=atpic.wikipandoc.convert(output)
        if err:
            output=err
    else:
        headers=[(b'Content-type', b'text/plain')]

    atpic.log.debug(yy,'will return',(status,headers,output))
    return (status,headers,output)


def do_diff(afile,aformat,arev):
    yy=atpic.log.setname(xx,'do_diff')
    status=b'200 Ok'
    headers=[(b'Content-type', b'text/html')]
    output=b'no DIFF!!!'
    atpic.log.debug(yy,'')
    return (status,headers,output)



def do_log(afile,aformat,arev):
    yy=atpic.log.setname(xx,'do_log')
    out=[]
    status=b'200 Ok'
    headers=[(b'Content-type', b'text/html')]

    (log,err)=atpic.wikigit.git_log([afile,])
    out.append(b'<Log>')
    for ele in log:
        out.append(b'<log>')
        for key in ele.keys():
            out.append(b'<'+key+b'>'+ele[key]+b'</'+key+b'>')
        out.append(b'</log>')
    out.append(b'</Log>')
    print(log)    
    output=b''.join(out)
    if aformat==b'html':
        headers=[(b'Content-type', b'application/xhtml+xml; charset=utf-8')]
        output=xsl_transform(output)
    elif aformat==b'xml':
        headers=[(b'Content-type', b'text/xml')]


    atpic.log.debug(yy,'')
    return (status,headers,output)


def dispatcher(environ):
    """
    Easy to unit test.
    """
    yy=atpic.log.setname(xx,'dispatcher')
    # get the GIT file name
    action=b'get'
    aformat=b'html'
    afile=b''
    path_info=environ.get(b'PATH_INFO',b'')
    base=b'/wiki' # this is set in nginx
    npath=path_info[len(base):]
    npath=npath.strip(b'/')
    afile=npath.lower()
    if afile==b'':
        afile=b'index'

    # get the action
    action=atpic.environment.get_qs_key(environ,b'a',b'get')

    # get the format
    aformat=atpic.environment.get_qs_key(environ,b'f',b'html')

    # get the revision
    # this is used for 
    # a) get: (get that revision)
    # b) diff: (get the diff between HEAD and that revision 
    #          cf man git-diff
    #          if format XXXX..YYYY: diff between the two
    #          if blank: between HEAD and previous
    #          if a number:
    # c) log: as the revision so start from downwards
    arev=atpic.environment.get_qs_key(environ,b'r',b'')

    atpic.log.debug(yy,'will return', (action,afile,aformat,arev))
    return (action,afile,aformat,arev)



def wsgi_bytes(environ):
    yy=atpic.log.setname(xx,'wsgi_bytes')
    status=b'200 Ok'
    headers=[(b'Content-type', b'text/html')]
    output=b''
    out=[]

    (action,afile,aformat,arev)=dispatcher(environ)
    if action==b'get':
        (status,headers,output)=do_get(afile,aformat,arev)
    elif action==b'log':
        (status,headers,output)=do_log(afile,aformat,arev)
    elif action==b'diff':
        (status,headers,output)=do_diff(afile,aformat,arev)
        
    
    atpic.log.debug(yy,'')
    return (status,headers,output)


