# import logging
import re
import traceback
import socket
import hashlib

import atpic.antidos
import atpic.errors
import atpic.mybytes
import atpic.log
import atpic.worker
import atpic.xplo
import atpic.redis_pie                 
# import atpic.globalcon

# import psyco # package python-psyco 
# psyco.full()
"""
URLs:
1st elelement
http://atpic.com/pic

"""
xx=atpic.log.setmod("INFO","dispatcher")




def is_disktier(thehost): # legacy url tester
    p = re.compile(b"^user[0-9]+\.atpic\.(com|foo|faa)$")
    m = p.match(thehost)
    if m:
        answer=True
    else:
        answer=False
    return answer

def get_udomain(host,hlist):
    # note: direct.atpic.com are served before in apache: not by python
    # direct is a legacy?
    yy=atpic.log.setname(xx,'get_udomain')
    if is_disktier(host):
        hlist.append((b'disktier',None))
    else:
        pattern=re.compile(b'^([^\.]+)\.atpic\.(com|foo|faa)$')
        match=pattern.match(host)
        if match:
            m1=match.group(1)
            if m1 not in [b'www',b'pic',b'gallery',b'faq',b'google',b'maps',b'du',b'pm',b'wiki']:
                replaced=pattern.sub(b':uname.atpic.com',host)
                uname=match.group(1)
                hlist.append((b'uname',uname))
            elif m1 == b'www':
                hlist.append((b'atpiccom',None))
            else:
                hlist.append((b'legacyobject',m1))
        elif host.endswith(b'.atpic.com'):
            hlist.append((b'legacy',None))
        elif  host != b'atpic.com':
            selldns=host
            hlist.append((b'selldns',selldns))
        else:
            hlist.append((b'atpiccom',None))

    return (hlist)



def get_id_legacy(path,plist):
    # we forget about language and resolution in the legacy redirect
    yy=atpic.log.setname(xx,'get_id_legacy')
    pattern=re.compile(b'^\/([a-z]{2})\/([0-9]+)\/([0-9]+)\/([^\.]+)$')
    match=pattern.match(path)
    if match:            
        replaced=pattern.sub(b'/:id/:secret',path)
        id=match.group(2)
        secret=match.group(4)
        path=replaced
        plist.append((b'id',id))
        plist.append((b'secret',secret))

    else:
        pattern=re.compile(b'^\/([0-9]+)\/([0-9]+)\/([^\.]+)$')
        match=pattern.match(path)
        if match:            
            replaced=pattern.sub(b'/:id/:secret',path)
            id=match.group(1)
            secret=match.group(3)
            path=replaced
            plist.append((b'id',id))
            plist.append((b'secret',secret))
        else:
            pattern=re.compile(b'^\/([a-z]{2})\/([0-9]+)\/([0-9]+)$')
            match=pattern.match(path)
            if match:            
                replaced=pattern.sub(b'/:id',path)
                id=match.group(2)
                path=replaced
                plist.append((b'id',id))
            else:
                pattern=re.compile(b'^\/([a-z]{2})\/([0-9]+)$')
                match=pattern.match(path)
                if match:            
                    replaced=pattern.sub(b'/:id',path)
                    id=match.group(2)
                    path=replaced
                    plist.append((b'id',id))
 
                else:
                    pattern=re.compile(b'^\/([0-9]+)\/([0-9]+)$')
                    match=pattern.match(path)
                    if match:            
                        replaced=pattern.sub(b'/:id',path)
                        id=match.group(1)
                        path=replaced
                        plist.append((b'id',id))
 
                    else:
                        pattern=re.compile(b'^\/([0-9]+)$')
                        match=pattern.match(path)
                        if match:            
                            replaced=pattern.sub(b'/:id',path)
                            id=match.group(1)
                            path=replaced
                            plist.append((b'id',id))
 
                        else:
                            pattern=re.compile(b'^\/([a-z]{2})\/([0-9]+)\/(.+)$')
                            match=pattern.match(path)
                            if match:            
                                replaced=pattern.sub(b'/:id/:secret',path)
                                id=match.group(2)
                                secret=match.group(3)
                                path=replaced
                                plist.append((b'id',id))
                                plist.append((b'secret',secret))
                            else:
                                pattern=re.compile(b'^\/([0-9]+)\/(.+)$')
                                match=pattern.match(path)
                                if match:            
                                    replaced=pattern.sub(b'/:id/:secret',path)
                                    id=match.group(1)
                                    secret=match.group(2)
                                    path=replaced
                                    plist.append((b'id',id))
                                    plist.append((b'secret',secret))


    return (plist)


def get_tree(path,plist,subject=b'tree'):
    yy=atpic.log.setname(xx,'get_tree')
    atpic.log.debug(yy,"input",(path,plist,subject))
    pattern=re.compile(b'^\/'+subject+b'(\/.*)$')
    match=pattern.match(path)
    if match:            
        atpic.log.debug(yy,"math")
        replaced=pattern.sub(b'/'+subject+b'/:tree',path)
        tree=match.group(1)
        path=replaced
        # if subject==b'wiki':
        #    path=path.strip(b'/')
    elif path==b'/'+subject or path==b'/'+subject+b'/':
        atpic.log.debug(yy,"no math")
        tree=b'/'

    
        if subject==b'wiki':
            tree=b''
        else:
            tree=b'/'
    plist.append((subject,tree))
    atpic.log.debug(yy,"output",plist)
    return (plist)

def get_faq(path,plist):
    yy=atpic.log.setname(xx,'get_faq')
    pattern=re.compile(b'^\/faq(\/.*)$')
    match=pattern.match(path)
    if match:            
        replaced=pattern.sub(b'/faq/:faq',path)
        faq=match.group(1)
        path=replaced
    elif path==b'/faq' or path==b'/faq/':
        faq=b'/'
    plist.append((b'faq',faq))
    return (plist)

def get_thefunction(key):
    """
    returns a function name from a Key
    e.g.:
    GET :uname.atpic.com/google -> get_uname_atpic_com_google
    """

    p = re.compile(b'[\.\- \:\/]')
    key=p.sub(b'_',key)
    key=key.lower()
    return key

def dispatcher(environ):
    """
    returns 
    an exploded host
    an exploded path
    exploded actions
    autor
    """
    yy=atpic.log.setname(xx,'dispatcher')
    atpic.log.debug(yy,'input=',environ)

    plist=[] # variables stored in path
    hlist=[] # variables stored in host
    actions=[]


    # compile some regex:
    digits_pattern=re.compile(b'^([0-9]+)$')

    host=environ[b'HTTP_HOST']
    path=environ[b'PATH_INFO']
    action=environ[b'REQUEST_METHOD']
    querystring=environ[b'QUERY_STRING']
    atpic.log.debug(yy,'0 (host,path,action)=',(host,path,action))

    actions.append(action.lower())

    if host==b'atpic.faa':
       host=b'atpic.com'
    if host==b'alex.atpic.faa':
        host=b'alex.atpic.com'
    p = re.compile(b'atpic\.faa$')
    host=p.sub(b'atpic.com',host)

    (hlist)=get_udomain(host,hlist)

    # clean trailing slash
    atpic.log.debug(yy,'1 path is', path)
    if path:
        if path[-1:]==b'/':
            path=path[:-1]

    splitted=path.split(b'/')

    atpic.log.debug(yy,"2 splitted path is", splitted)


    if hlist[0][0]==b'legacyobject': # removed has_key use 'in' in py3k, see also get('x',y) with default value y
       # this is legacy host URL e.g pic.atpic.com
        atpic.log.debug(yy,"3 LEGACYY")
        (plist)=get_id_legacy(path,plist)
        atpic.log.debug(yy,"4 LEGACYDIC", plist)
        # action=b"REDIR"
        # if "id" in adic:
        #     pathid=b"?q=id:"+adic["id"]
        #     if "secret" in adic:
        #         pathid=pathid+b"&secret=b"+adic["secret"]
        # else:
        #     pathid=b""
        # path=b"/"+adic["legacyobject"]+pathid


    else:
        if len(splitted)>1:
            # set the actions
            last=splitted.pop()
            if last in (b'get',b'post',b'put',b'delete'):
                actions.append(last)
            else:
                splitted.append(last)


        if len(splitted)>1: # the length may have changed because nof pop()
            pos1=splitted[1]
            atpic.log.debug(yy,"5 pos1 " , pos1)


            if pos1 in (b'wiki',):
                atpic.log.debug(yy,"6 we are in wiki" , pos1)
                last=splitted.pop()
                if last in (b'_get',b'_post',b'_put',b'_delete'):
                    atpic.log.debug(yy,"7 wikilast is underscore")
                    actions.append(last[1:])
                else:
                    atpic.log.debug(yy,"8 wikilast is NOT underscore")
                    splitted.append(last)


            if pos1 in [b'login',b'forgot',b'reset'] and actions[0]==b'get':
                atpic.log.debug(yy,"9 pos1loginnnn", pos1)
                actions.append(b'post')

            if pos1 in (b'tree', b'treenav', b'treesearch', 
                        b'vtree', b'vtreenav', b'vtreesearch', 
                        b'geo', b'geonav', b'geosearch', 
                        b'blog', b'blognav', b'blogsearch',
                        b'journal',): 
                # COMPOSITE, FACET, SEARCH, VARIABLE
                # path, pathnav, pathsearch, path         *****
                # vpath, vpathnav, vpathsearch, vpath     *****
                # geo, geonav, geosearch, geo             *****
                # blog, blognav, blogsearch, blog *****
                # geo, geonav, geosearch, geopath              (alias)
                # blog, blognav, blogsearch, blogpath  (alias)
                # tree, treenav, treesearch, treepath
                # vtree, vtreenav, vtreesearch, vtreepath
                # tree, treenav, treesearch, path
                # vtree, vtreenav, vtreesearch, vpath
                # geopath, geopathnav, geopathsearch
                # blogpath, blognav, blogsearch
                # blogpath, blogpathnav, blogpathsearch
                # path, nav, search NO as collision /search is already used
                atpic.log.debug(yy,"10 pos1 is BLOG")
                (plist)=get_tree(path,plist,subject=pos1)
            elif pos1 in (b'wiki',):
                atpic.log.debug(yy,"11 pos1 is WIKI")
                atpic.log.debug(yy,"12 last:",last)
                if last in (b'_get',b'_post',b'_put',b'_delete'):
                    (plist)=get_tree(b'/'.join(splitted),plist,subject=pos1)
                elif last in (b'_revision',b'_link',b'_deadlink',b'_picture',b'_linktothis'):
                    atpic.log.debug(yy,"13 revision collection")
                    (plist)=get_tree(b'/'.join(splitted[:-1]),plist,subject=pos1)
                    plist.append((last[1:],None))
                elif re.search(b'_revision',path):
                    atpic.log.debug(yy,"14 revision element or diff")
                    (plist)=get_tree(b'/'.join(splitted[:-2]),plist,subject=pos1)
                        
                    plist.append((b'revision',last))
                    atpic.log.debug(yy,"15 wiki diff plist",plist)

                else:
                    (plist)=get_tree(path,plist,subject=pos1)

            elif pos1==b'faq':
                atpic.log.debug(yy,"16 pos1 is FAQ")
                (plist)=get_faq(path,plist)
            elif len(pos1)==2 and pos1!=b'du' and pos1!=b'pm':
                # constraint on uname: NO two chars only
                # possibly a LANG legacy encoding
                atpic.log.debug(yy,"17 LEGACY LANG")
                # eliminate the LANG and redirect
                action=b'REDIR'
                path=b'/'
                if len(splitted)>2:
                    path=path+b'/'.join(splitted[2:])
            elif digits_pattern.match(pos1):
                atpic.log.debug(yy,"18 POS1 is digits ONLY")
                action=b'REDIR'
                host=b'atpic.com'
                path=b'/user?q=id:'+pos1
            
            else:
                atpic.log.debug(yy,"19 SEARCH")
                tlen=len(splitted)
                rest=tlen %2
                nb=int(tlen/2)-1+rest
                if rest==0:
                    atpic.log.debug(yy,"20 collection",rest,nb)
                else:
                    atpic.log.debug(yy,"21 entry",rest,nb)

                for i in range(0,nb):
                    plist.append((splitted[2*i+1],splitted[2*i+2]))
                if rest==0:
                    plist.append((splitted[-1],None)) # this is a collection, no ID




    # autor
    # note: 
    # - owner is the photograph, owner of the pic and galleries
    # - author is the tagger 
    atpic.log.debug(yy,'22 autorization')
    autor=b'anonymous'
    try:
        plist00=plist[0][0]
    except:
        plist00=None
    atpic.log.debug(yy,'23 plist00',plist00)
    if actions[-1]!=b'get' and plist00:
        atpic.log.debug(yy,'24 test1')
        autor=b'admin'
        if hlist[0][0]==b'uname':
            atpic.log.debug(yy,'25 test2 actions',actions)
            autor=b'owner' # user, i.e the user that in the username
            if actions[-1]==b'post':
                atpic.log.debug(yy,'26 test3')
                if plist[-1][0] in (b'tag',b'comment',b'phrase',b'vote'):
                    atpic.log.debug(yy,'27 test4')
                    autor=b'authenticated'
            if actions[-1]==b'put' or actions[-1]==b'delete' :
                atpic.log.debug(yy,'28 test5')
                if plist[-1][0] in (b'tag',b'phrase',b'vote'):
                    atpic.log.debug(yy,'29 test6')
                    autor=b'author' # needs authenticated + (need to be the author of the tag or the owner of the gallery)
        if plist00==b'user':
            atpic.log.debug(yy,'30 test7')
            autor=b'owner'
            if actions[-1]==b'post':
                atpic.log.debug(yy,'31 test8')
                autor=b'anonymous'

        if plist00 in (b'forgot',b'reset'):
            atpic.log.debug(yy,'30 test8')
            autor=b'anonymous'


    if hlist[0][0]==b'uname' and plist00==b'cart':
        atpic.log.debug(yy,'32 test9')
        autor=b'owner'

    if plist00==b'translate':
        atpic.log.debug(yy,'33 test10')
        if actions[-1]==b'post':
            autor=b'authenticated'
    if plist00==b'login' :
        autor=b'anonymous'
    if plist00==b'reset' :
        autor=b'authenticated'
    if plist00==b'pm' and actions[-1]!=b'post':
        autor=b'owner'
    if plist00==b'pm' and actions[-1]==b'post':
        autor=b'authenticated'
    if plist00==b'pmsent':
        autor=b'owner'
    atpic.log.debug(yy,'output=',(hlist,plist,actions,autor))
    return (hlist,plist,actions,autor)


def signature(hxplo,pxplo,actions):
    actions_s=b' '.join(actions)
    sig=actions_s+b' '+hxplo.signature()+b''+pxplo.signature()
    return sig


if __name__ == "__main__":
    pass
