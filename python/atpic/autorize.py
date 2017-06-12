#!/usr/bin/python3
# import logging
import atpic.log

import atpic.libpqalex
import atpic.environment

"""
This is different from authentication.
Authenticate answers the question:
who is accessing the page?
Autorization answers the question:
Does the user have the permission to access the URL?

Autorization is based on the HTTP verb and URI.

It can be unit tested.

Expensive authenticate (HTTP Basic which requires a SQL lookup at each request)
may not be necessary (e.g. for the public parts of the site).

Generic (set by dispatcher): 

BETTER: two layers:
 <mode>anonymous,authenticated,author,owner,admin
+<limit>protect,sell,private,friend,public (mode)
+<useris>authenticated,owner,author,friend,admin,inthesecret
=> <result>authorized,notauthorized,watermarked

calculate the user power: <clientprops>
-------------------------
userisauthenticated
userisowner
userisauthor
userisfriend
userisadmin
secretsent ot userisinthesecret
<useris>
to be matched against
1) the gallery modes (private,protect,friend,sell,public)
2) the dispatcher modes (anonymous, admin, user, authenticated, author)

result:
yes, no, partial (only watermark)
"""


# mode photograph client:
# a username/key is sent unencrypted, just to view watermarked pictures
# then stored as a cookie gi_123 (gallery invite) or gs_123 (gallery secret)
xx=atpic.log.setmod("INFO","autorize")

def get_gallery_mode_sql_wrap(galleryid,db):
    try:
        (mode,secret)=get_gallery_mode_sql(galleryid,db)
    except:
        raise atpic.errors.Error404(b"gallery",galleryid,b"not found")
    return (mode,secret)

def get_gallery_mode_sql(galleryid,db):
    yy=atpic.log.setname(xx,'get_gallery_mode_sql')
    atpic.log.debug(yy,'entering get_gallery_mode_sql(',galleryid,db,')')
    if galleryid:
        query=b"select _mode,_secret from _user_gallery where id=$1"
        ps=atpic.libpqalex.pq_prepare(db,b'',query)
        result=atpic.libpqalex.pq_exec_prepared(db,b'',(galleryid,))
        result=atpic.libpqalex.process_result(result)
        (mode,secret)=(result[0][b'_mode'],result[0][b'_secret'])
    else:
        (mode,secret)=(b'',b'')
    atpic.log.debug(yy,'will return',(mode,secret))
    return (mode,secret)


def check_authenticated_isfriend(authenticated_userid,userid,galleryid,db):
    # user id can be empty b'' (if not in the /user virtual tree)
    # galleryid can be empty b'' (if above a particular gallery)
    yy=atpic.log.setname(xx,'check_authenticated_isfriend')
    atpic.log.debug(yy,'input=',(authenticated_userid,userid,galleryid,db))
    if userid and authenticated_userid:
        if galleryid:
            query=b"select id from _user_friend where _user=$1 and id=$2 UNION SELECT id FROM _user_gallery_friend where _user=$3 AND id=$4 AND _gallery=$5"
            parameters=(userid,authenticated_userid,userid,authenticated_userid,galleryid,)
        else:
            query=b"select id from _user_friend where _user=$1 and id=$2"
            parameters=(userid,authenticated_userid,)
        atpic.log.debug(yy,'query=',query)
        atpic.log.debug(yy,'parameters=',parameters)
        ps=atpic.libpqalex.pq_prepare(db,b'',query)
        result=atpic.libpqalex.pq_exec_prepared(db,b'',parameters)    
        result=atpic.libpqalex.process_result(result)
    else:
        result=None

    if result:
        out=True
    else:
        out=False
    atpic.log.debug(yy,'will return',out)

    return out

def authorization(mode,gallerymode,isauthenticated,isfriend,isowner,isauthor,isadmin,isinsecret):
    """
    This can be unit tested as no SQL
    """
    yy=atpic.log.setname(xx,'authorization')

    result=b'notauthorized'
    atpic.log.debug(yy,'input=',(mode,gallerymode,isauthenticated,isfriend,isowner,isauthor,isadmin,isinsecret))

    # the generic modes
    if mode==b'anonymous':
        atpic.log.debug(yy,'1 anonymous we pass')
        result=b'authorized'
    elif mode==b'owner':
        atpic.log.debug(yy,'2 mode is owner')
        if isowner:
            result=b'authorized'
    elif mode==b'author':
        atpic.log.debug(yy,'3 mode is author') # used for tags, phrases, votes
        if isauthor:
            result=b'authorized'
    elif mode==b'admin':
        atpic.log.debug(yy,'4 mode is admin')
        if isadmin:
            result=b'authorized'
            
    atpic.log.debug(yy,'result5=',result)

    # now gallery specific mode
    if gallerymode==b'v': # private
        atpic.log.debug(yy,'')
        if isowner or isinsecret:
            result=b'authorized'
        else:
            result=b'notauthorized'
        atpic.log.debug(yy,'result=6',result)
    elif gallerymode==b'f': # friend
        atpic.log.debug(yy,'mode friend')
        if isowner or isfriend:
            result=b'authorized'
        else:
            result=b'notauthorized'
    
        atpic.log.debug(yy,'result7=',result)
    elif gallerymode==b't': # protect
        atpic.log.debug(yy,'mode friend')
        if isowner or isfriend:
            result=b'authorized'
        else:
            result=b'watermarked'
    
        atpic.log.debug(yy,'result8=',result)
    elif gallerymode==b's': # sell
        atpic.log.debug(yy,'mode sell')
        if isowner:
            result=b'authorized'
        else:
            result=b'watermarked'
        atpic.log.debug(yy,'result9=',result)

    if isadmin:
        result=b'authorized'
        atpic.log.debug(yy,'result10=',result)
    atpic.log.debug(yy,'return=',result)
    return result

def authorization_elasticsearch(mode,uid,aid):
    # we need a special function for search (elasticsearch)
    # as we do not have the 'mode' (anonymous, etc...) or if we have it
    # it does not mean anything
    # This is to decide between b'authorized' and b'watermarked'
    # see elasticsearch_queries.permission_filter
    result=b'notauthorized'
    if mode==b'b': # public
            result=b'authorized'
    elif mode==b's': # sell
        if aid!=b'' and uid==aid:
            result=b'authorized'
        else:
            result=b'watermarked'
    elif mode==b't': # protect
        # should we see the watermarked in protected mode?????
        if aid!=b'' and uid==aid:
            result=b'authorized'
        else:
            result=b'watermarked'
    elif mode==b'v': # private and owner (from search query)
            result=b'authorized'
    elif mode==b'f': # friends and infriends  (from search query)
            result=b'authorized'
    return result



def get_galleryid(pxplo):
    # return b'' or galleryid
    galleryid=b''
    if pxplo.getmatrix(1,0)==b'gallery' and pxplo.getmatrix(1,1): # a gallery entry
        owner_userid=pxplo.getmatrix(0,1)
        galleryid=pxplo.getmatrix(1,1)
    # to be used later with: (gallerymode,secret)=get_gallery_mode_sql(galleryid,db)
    return galleryid

def get_ownerid(pxplo):
    ownerid=b''
    if pxplo.getmatrix(0,0)==b'user' and pxplo.getmatrix(0,1):
        ownerid=pxplo.getmatrix(0,1)
    return ownerid

def get_authenticatedid(authenticated,details):
    authenticatedid=b''
    if authenticated:
        authenticatedid=details[0]
    return authenticatedid

def get_authorid(pxplo):
    lastobjecttype=pxplo.getmatrix(len(pxplo)-1,1)
    if lastobjecttype in (b'tag',b'phrase',b'vote'): 
        # do not do it on b'comment' as too difficult
        # as not in url
        lastobjectid=pxplo.getmatrix(len(pxplo)-1,1)
    else:
        lastobjectid=b''
    return lastobjectid


def check_authenticated_isowner(authenticatedid,ownerid):
    if authenticatedid!=b'' and authenticatedid==ownerid:
        return True
    else:
        return False

def check_authenticated_isauthor(authenticatedid,authorid):
    if authenticatedid!=b'' and authenticatedid==authorid:
        return True
    else:
        return False

def check_authenticated_isadmin(authenticatedid):
    if authenticatedid in [b'1',]:
        return True
    else:
        return False

def check_goodsecret(secret,secret_sent):
    if secret !=b'' and secret==secret_sent:
        return True
    else:
        return False

def autorize(pxplo,actions,autor,environ,authenticated,details,db):
    """
    two layers:
    <mode>anonymous,authenticated,author,owner,admin
    +<limit>protect,sell,private,friend
    +<useris>authenticated,owner,author,friend,admin,inthesecret
    => <result>authorized,notauthorized,watermarked
    """
    yy=atpic.log.setname(xx,'autorize')
    atpic.log.debug(yy,'input=',(pxplo.list(),actions,autor,environ,authenticated,details,db))

    galleryid=get_galleryid(pxplo)
    (gallerymode,secret)=get_gallery_mode_sql_wrap(galleryid,db)
    secret_sent=atpic.environment.get_qs_key(environ,b'secret',b'')

    # all user ID necessary; rule: if empty (b'') then not set:
    authenticatedid=get_authenticatedid(authenticated,details)
    atpic.log.debug(yy,'authenticatedid',authenticatedid)
    ownerid=get_ownerid(pxplo)
    atpic.log.debug(yy,'ownerid',ownerid)
    authorid=get_authorid(pxplo)
    atpic.log.debug(yy,'authorid',authorid)

    # list of useris:
    isauthenticated=authenticated
    atpic.log.debug(yy,'isauthenticated',isauthenticated)
    isfriend=check_authenticated_isfriend(authenticatedid,ownerid,galleryid,db)
    atpic.log.debug(yy,'isfriend',isfriend)
    isowner=check_authenticated_isowner(authenticatedid,ownerid) # the user/gallery/pic owner
    atpic.log.debug(yy,'isowner',isowner)
    isauthor=check_authenticated_isauthor(authenticatedid,authorid) # the tagger/phraser
    atpic.log.debug(yy,'isauthor',isauthor)
    isadmin=check_authenticated_isadmin(authenticatedid)
    atpic.log.debug(yy,'isadmin',isadmin)
    isinsecret=check_goodsecret(secret,secret_sent)
    atpic.log.debug(yy,'isinsecret',isinsecret)

    autoresult=authorization(autor,gallerymode,isauthenticated,isfriend,isowner,isauthor,isadmin,isinsecret)
    atpic.log.debug(yy,'autoresult',autoresult)
    atpic.log.debug(yy,'output=',(autor,gallerymode,isauthenticated,isfriend,isowner,isauthor,isadmin,isinsecret,autoresult))
    return (autor,gallerymode,isauthenticated,isfriend,isowner,isauthor,isadmin,isinsecret,autoresult)

if __name__ == "__main__":
    db=atpic.libpqalex.db()
    (mode,secret)=get_gallery_mode_sql(b'1',db)
    print(mode,secret)
    isfriend=check_authenticated_isfriend(b'1',b'2',b'1',db)
    print(isfriend)

    pass


