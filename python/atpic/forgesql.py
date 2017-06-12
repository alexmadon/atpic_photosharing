#!/usr/bin/python3
"""
This creates the automatic SQL queries for the API.

The only function that should be called from outside this module is: forge_query()


"""
# import logging
import traceback
import copy

import atpic.log
import atpic.xplo
import atpic.indatautils
import atpic.dateutils
import atpic.randomalpha
import atpic.wiki_lines
import atpic.wikinormalizer

from atpic.mybytes import *

xx=atpic.log.setmod("INFO","forgesql")

# always avoid OFFSET as this is slow, better use greate than operator id 

def keysort(p):
    return p[0]

def create_tablename(o2list):
    tablename=b"_".join(o2list)
    tablename=b"_"+tablename
    return tablename

def forge_insertpm(pxplo,tablename,indic,authid):
    yy=atpic.log.setname(xx,"forge_insertpm")
    atpic.log.debug(yy,"forge_insertpm(",pxplo,tablename,indic,authid,")")
    """
    WITH
    ins1 AS (INSERT INTO _user_pm (id,_from,_user,_title) VALUES (997,2,1,'hi99') RETURNING *),
    ins2 AS (INSERT INTO _user_pmsent (id,_to,_user,_title) SELECT id, ins1._user, ins1._from, _title FROM ins1 RETURNING *)
    SELECT * FROM ins1;
    """
    infieldslist=[]
    indollarslist=[]

    # convert a dictionary into a list of key-value
    inlist=list(indic.items())
    inlist.sort(key=keysort)

    try:
        (inkeylist,invaluelist)=zip(*inlist)
    except:
        (inkeylist,invaluelist)=([],[])

    for key in inkeylist:
        infieldslist.append(b'_'+key)
        indollarslist.append(b'$')

    infields=b','.join(infieldslist)
    indollars=b','.join(indollarslist)
    if infields:
        infields=b','+infields
    if indollars:
        indollars=b','+indollars

    uid=pxplo.getmatrix(0,1)
    invaluelist2=[]
    for val in invaluelist:
        invaluelist2.append(val) # val is a list!
    query_args=[]
    query_args.append(authid)
    query_args.append(uid)
    query_args=query_args+invaluelist2

    querylist=[]
    querylist.append(b'WITH')
    querylist.append(b'ins1 AS (INSERT INTO _user_pm (_from,_user'+infields+b') VALUES ($,$'+indollars+b') RETURNING *),')
    querylist.append(b'ins2 AS (INSERT INTO _user_pmsent (id,_to,_user'+infields+b') SELECT id, _user, _from'+infields+b' FROM ins1 RETURNING *)')
    querylist.append(b'SELECT * FROM ins1')
    query=b' '.join(querylist)
    (query,query_args)=transform(query,query_args)
    return (query,query_args)

def forge_selectversion(pxplo,actions,depth,lang,start,fromto,perpage,allownull):
    yy=atpic.log.setname(xx,"forge_selectversion_notransform")
    lastone=pxplo.getmatrix(len(pxplo)-1,0)
    lastval=pxplo.getmatrix(len(pxplo)-1,1)
    atpic.log.debug(yy,"lastone",lastone)
    atpic.log.debug(yy,"lastval",lastval)

    if lastone==b'revision' and lastval==None:
        atpic.log.debug(yy,"lastone is revision and there is no lastval: doing two calls")
        atpic.log.debug(yy,"111111: First call")
        (query1,query_args1)=forge_selectversion_notransform(pxplo,actions,depth,lang,start,fromto,perpage,allownull)
        if fromto==b'from':
            newfromto=b'to'
        else:
            newfromto=b'from'
        perpage=b'0'
        atpic.log.debug(yy,"222222: Second call")
        (query2,query_args2)=forge_selectversion_notransform(pxplo,actions,depth,lang,start,newfromto,perpage,allownull)
        query=b'('+query1+b') UNION ('+query2+b') ORDER BY id DESC'
        query_args=query_args1+query_args2
    else:
        atpic.log.debug(yy,"000000: lastone is NOT a revision: doing ONE call")
        (query,query_args)=forge_selectversion_notransform(pxplo,actions,depth,lang,start,fromto,perpage,allownull)

    (query,query_args)=transform(query,query_args)
    atpic.log.debug(yy,"output=", (query,query_args))
    return (query,query_args)

def forge_selectversion_notransform(pxplo,actions,depth,lang,start,fromto,perpage,allownull):
    # used for wikitext
    """
    WITH 
    select1 AS (SELECT * from _wiki WHERE _path='/'),
    one AS (SELECT 1 AS uno)
    SELECT select1.* FROM select1 RIGHT JOIN one ON true;
    """


    """
    WITH select1 AS (select id,_user from _user_gallery where _user=1),
    one AS (SELECT 1 AS uno)
    SELECT select1.* FROM select1 RIGHT JOIN one ON true;
    
    WITH select1 AS (select id,_user from _user_gallery where _user=-99999999),
    one AS (SELECT 1 AS uno)
    SELECT select1.* FROM select1 RIGHT JOIN one ON true;
    """

    yy=atpic.log.setname(xx,"forge_selectversion_notransform")
    atpic.log.debug(yy,"input=", (pxplo.list(),actions,depth,lang,start,fromto,perpage,allownull))
    atpic.log.debug(yy,"1a pxplo.keys()",pxplo.keys())
    query=b''
    query_list=[]
    user=b''
    # deal with user
    first=pxplo.getmatrix(0,0)
    userand=b""
    if first==b"user":
        atpic.log.debug(yy,'0 have a user....')
        user=pxplo.getmatrix(0,1) 
        if user:   
            atpic.log.debug(yy,'1 have a user id')
            userand=b"_user=$ AND"

    lastone=pxplo.getmatrix(len(pxplo)-1,0)
    lastval=pxplo.getmatrix(len(pxplo)-1,1)
    atpic.log.debug(yy,"2 (lastone,lastval)",(lastone,lastval))
    if lastone==b'revision':
        atpic.log.debug(yy,"3 see 'revision' keyword")
        atpic.log.debug(yy,"3a pxplo.keys()",pxplo.keys())
        tablename=create_tablename(pxplo.keys()[:-1])
        atpic.log.debug(yy,"3b tablename",tablename)
        if not lastval:
            atpic.log.debug(yy,"4 this is a collection")
            revand=b'' # this is a collection
        else:
            atpic.log.debug(yy,"5 it's either one revision or a diff of two")
            splitted=lastval.split(b',')
            if len(splitted)>1:
                atpic.log.debug(yy,"6 need two revisions for diffing")
                revand=b'id in ($,$) AND'
            else:
                atpic.log.debug(yy,"7 just one revision")
                revand=b'id=$ AND'
    else:
        atpic.log.debug(yy,"8")
        tablename=create_tablename(pxplo.keys())
        revand=b''
    langand=b'_lang=$ AND'
    query_list.append(b'WITH select1 AS (')
    query_list.append(b'SELECT * FROM '+tablename)
    query_list.append(b'WHERE')
    if userand: query_list.append(userand)
    if revand: query_list.append(revand)
    query_list.append(langand)
    query_list.append(b'_path=$')

    if fromto==b'to':
        desc_asc=b'ASC'
        greater_lower=b'>='
    else:
        desc_asc=b'DESC'
        greater_lower=b'<='


    if start!=b'0':
        query_list.append(b'AND id '+greater_lower+b' $') # start
    query_list.append(b'ORDER BY id '+desc_asc)
    query_list.append(b'LIMIT $') # 1 for entry, 2 for diff, 10 for collection
    query_list.append(b'),')
    query_list.append(b'one AS (SELECT 1 AS uno)')
    query_list.append(b'SELECT select1.* FROM select1')
    if allownull: 
        query_list.append(b'RIGHT JOIN one ON true')

    # EXIST
    atpic.log.debug(yy,"9")

    if first==b'user':
        atpic.log.debug(yy,"10 we see a user")
        path=pxplo.getmatrix(1,1)
    else:
        atpic.log.debug(yy,"11 no user")
        path=pxplo.getmatrix(0,1)

    atpic.log.debug(yy,"11b path=",path)
    path=atpic.wikinormalizer.normalize(path)
    atpic.log.debug(yy,"11bb path normalized=",path)

    # arguments
    query_args=[]
    if user:
        atpic.log.debug(yy,"12 appending user",user)
        query_args.append(user)
    if lastone==b'revision':
        atpic.log.debug(yy,"13 last is a revision")
        if lastval:
            atpic.log.debug(yy,"14 there is a revision string")
            splitted=lastval.split(b',')
            if len(splitted)>1:
                atpic.log.debug(yy,"15 it can be splitted")
                query_args.append(splitted[0])
                query_args.append(splitted[1])
            else:
                atpic.log.debug(yy,"16 it cannot be splitted")
                query_args.append(lastval)

    query_args.append(lang)
    query_args.append(path)
    if start!=b'0':
        query_args.append(start)

    if lastone==b'revision':
        atpic.log.debug(yy,"17 there is a revision keyword in path")
        if lastval:
            atpic.log.debug(yy,"18 there is a revision string value")
            splitted=lastval.split(b',')
            if len(splitted)>1:
                atpic.log.debug(yy,"19 it can be splitted by a coma")
                query_args.append(b'2')
            else:
                atpic.log.debug(yy,"20 it cannot be splitted by a coma")
                query_args.append(b'1')
        else:
            atpic.log.debug(yy,"21 there is no value string: it's a collection")
            query_args.append(atpic.mybytes.int2bytes(atpic.mybytes.bytes2int(perpage)+1)) # 10 by default
    else:
        atpic.log.debug(yy,"22 there is no revision asked, take the last")
        query_args.append(b'1')
    query=b' '.join(query_list)
    atpic.log.debug(yy,"output=", (query,query_args))
    return (query,query_args)





def forge_insertversion(pxplo,tablename,lang,environ,indic,authid):
    # used for wiki like (pages that contain versions) wikitext
    """
WITH  
select1 AS (SELECT * FROM _wiki WHERE _path='/' ORDER BY id DESC LIMIT 1),
select2 AS (SELECT * FROM select1 WHERE _text='new text2'),
select3 AS (INSERT INTO _wiki (_path,_text,_datepublished) SELECT '/','new text2',now() WHERE NOT EXISTS (SELECT 1 FROM select2) 
    RETURNING *)
SELECT * FROM select2 UNION SELECT * FROM select3;
"""
    yy=atpic.log.setname(xx,"forge_insertversion")
    atpic.log.debug(yy,"input",(pxplo.list(),tablename,lang,environ,indic,authid))



    # deal with 'user'
    user=b''
    first=pxplo.getmatrix(0,0)
    userand=b""
    userfield=b''
    uservalue=b''
    if first==b"user":
        atpic.log.debug(yy,'have a user....')
        user=pxplo.getmatrix(0,1) 
        if user:   
            atpic.log.debug(yy,'have a user id')
            # query_args.append(pxplo.getmatrix(0,1))
            userand=b"_user=$ AND "
            userfield=b',_user'
            uservalue=b',$'
    # query
    querylist=[]
    querylist.append(b'WITH')
    querylist.append(b'select1 AS (SELECT * FROM '+tablename+b' WHERE '+userand+b'_path=$ AND _lang=$ ORDER BY id DESC LIMIT 1),')
    querylist.append(b'select2 AS (SELECT * FROM select1 WHERE _wikitext=$ AND _lang=$),')
    querylist.append(b'select3 AS (INSERT INTO '+tablename+b' (_path,_wikitext,_lang,_message,_datepublished'+userfield+b') SELECT $,$,$,$,now()'+uservalue+b' WHERE NOT EXISTS (SELECT 1 FROM select2) ')
    querylist.append(b'    RETURNING *)')
    querylist.append(b'SELECT * FROM select2 UNION SELECT * FROM select3')
    query=b' '.join(querylist)

    if user:
        path=pxplo.getmatrix(1,1)
    else:
        path=pxplo.getmatrix(0,1)

    atpic.log.debug(yy,"path=",path)
    
    path=atpic.wikinormalizer.normalize(path)
    atpic.log.debug(yy,"normalized path=",path)

    lines=atpic.wiki_lines.get_lines(environ)
    if lines:
        wikitext=indic[b'wikitext']
        wikilines=indic[b'wikilines']
        wikitext=atpic.wiki_lines.replace(wikitext,wikilines,lines[0],lines[1])

    else:
        wikitext=indic[b'wikitext']


    atpic.log.debug(yy,"new wikitext=",wikitext)
    message=indic.get(b'message',b'') # may fail

    query_args=[]
    if user: 
        query_args.append(user)
    query_args.append(path)
    query_args.append(lang)
    query_args.append(wikitext)
    query_args.append(lang)
    query_args.append(path)
    query_args.append(wikitext)
    query_args.append(lang)
    query_args.append(message)
    if user: 
        query_args.append(user)

    (query,query_args)=transform(query,query_args)
    atpic.log.debug(yy,"output",(query,query_args))
    return (query,query_args)



def forge_upsert(pxplo,tablename,indic):
    #  for b'tag',b'phrase',b'vote',b'friend'
    yy=atpic.log.setname(xx,"forge_upsert")
    atpic.log.debug(yy,"forge_upsert(",pxplo,tablename,indic,")")
    """
    WITH 
    upsert1 AS (UPDATE actor SET last_update=now() WHERE fname='Alex4' and lname='Madon' returning *),
    upsert2 AS (INSERT INTO actor  (fname, lname,last_update) SELECT 'Alex4','Madon',now() WHERE NOT EXISTS (SELECT 1 FROM upsert) 
    RETURNING *)
    SELECT * FROM UPSERT1 UNION SELECT * FROM UPSERT2;
    """
    # convert a dictionary into a list of key-value
    inlist=list(indic.items())
    inlist.sort(key=keysort)
    try:
        (inkeylist,invaluelist)=zip(*inlist)
    except:
        (inkeylist,invaluelist)=([],[])

    querylist=[]
    querylist.append(b"WITH")

    key2set=[]
    key2insert=[]
    val2set=[]

    for key in inkeylist:
        key2set.append(b'_'+key+b'=$')
        key2insert.append(b'_'+key)
        val2set.append(b'$')
 
    uniquevals=[]
    uniquekeys=[]
    uniquedollars=[]
    if pxplo.getmatrix(0,0)==b"user":
        uniquevals.append(pxplo.getmatrix(0,1))
        uniquekeys.append(b'_user')
        uniquedollars.append(b'$')
    if pxplo.getmatrix(len(pxplo)-1,0) in [b'tag',b'phrase',b'vote',b'friend']: # last object
        uniquevals.append(pxplo.getmatrix(len(pxplo)-1,1))
        uniquekeys.append(b'id')
        uniquedollars.append(b'$')
    if pxplo.getmatrix(len(pxplo)-1,0) in [b'tag',b'phrase',b'vote',b'friend'] and len(pxplo)>2: # last object
        uniquevals.append(pxplo.getmatrix(len(pxplo)-2,1))
        uniquekeys.append(b'_'+pxplo.getmatrix(len(pxplo)-2,0))
        uniquedollars.append(b'$')
        
    uniquekeys2and=[]
    for key in uniquekeys:
        uniquekeys2and.append(key+b'=$')
    query_args=[]
    invaluelist2=[]
    for val in invaluelist:
        invaluelist2.append(val) # val is a list!
    query_args=invaluelist2+uniquevals+uniquevals+invaluelist2

    querylist.append(b"upsert1 AS (UPDATE "+tablename+b" SET "+b', '.join(key2set+[b"_datelast=now()",])+b" WHERE "+b' AND '.join(uniquekeys2and)+b" RETURNING *),")
    querylist.append(b"upsert2 AS (INSERT INTO "+tablename+b" ("+b','.join(uniquekeys+key2insert+[b"_datelast",])+b") SELECT "+b','.join(uniquedollars+val2set+[b"now()",])+b" WHERE NOT EXISTS (SELECT 1 FROM upsert1) RETURNING *)")
    querylist.append(b"SELECT * FROM upsert1 UNION SELECT * FROM upsert2")
    query=b' '.join(querylist)
    
    (query,query_args)=transform(query,query_args)
    return (query,query_args)

def forge_update(pxplo,tablename,indic):
    yy=atpic.log.setname(xx,"forge_update")
    atpic.log.debug(yy,"forge_update(",pxplo,tablename,indic,")")


    # query_args=[]
    lenpm=len(pxplo)-1

    and_deleted_iszero=get_and_deleted_iszero(tablename)


    # convert a dictionary into a list of key-value
    inlist=list(indic.items())
    inlist.sort(key=keysort)
    atpic.log.debug(yy,"inlist=",inlist)

    try:
        (inkeylist,invaluelist)=zip(*inlist)
    except:
        (inkeylist,invaluelist)=([],[])
        inlist=[]
    atpic.log.debug(yy,"(inkeylist,invaluelist)=",(inkeylist,invaluelist))

    invaluelist2=[]
    for val in invaluelist:
        invaluelist2.append(val) # val is a list!
    query_args=invaluelist2

    # deal with the 'SET' string
    keyvs=[]
    for (key,value) in inlist:
        s=b'_'+key+b"=$"
        keyvs.append(s)


    # deal with 'user'
    first=pxplo.getmatrix(0,0)
    userand=b""
    if first==b"user":
        atpic.log.debug(yy,'have a user....')
        user=pxplo.getmatrix(0,1) 
        if pxplo.keys()==[b'user']:
            atpic.log.debug(yy,'we pass as this is the _user table update')    
        elif user:   
            atpic.log.debug(yy,'have a user id')
            query_args.append(pxplo.getmatrix(0,1))
            userand=b"_user=$ AND "


    # deal with the unique ID
    id=pxplo.getmatrix(lenpm,1)    
    query_args.append(id)






    query=b"UPDATE "+tablename+b" SET "+b",".join(keyvs)+b" WHERE "+userand+b"id=$"+and_deleted_iszero+b" RETURNING *"
    atpic.log.debug(yy,'query1',query)

    # query=query+b",".join(keyvs)
    # atpic.log.debug(yy,'query2',query)




    (query,query_args)=transform(query,query_args)
    atpic.log.debug(yy,'output=',query,query_args)




    return (query,query_args)


def forge_delete(tablename,firstobject_id,lastobject_id):

    """
    about deletes:
    could add a flag:deleted to each table
    that could be incremented -1:not deleted, >0 deleted X times
    only on _user, _user_gallery, _user_gallery_pic
    that ison those whohave a unique string in addition to ID
    this allows to delete more than once,and gives to the admin possibility to restore
    need to store timestamp of (first) delete

    we could increment globally all deleted users, or galleries or pics

    this is only for _user, _user_gallery, _user_gallery_pic
    that is those that are name based

    do it is 2 stages:
    first set deleted to 1 on the one to delete + update the last touched
    then update everything in that partition incrementing _deleted by 1
    partition= all users for _user, all users gals or pics for one _user

    """
    yy=atpic.log.setname(xx,"forge_delete")
    if tablename in [b'_user',b'_user_gallery',b'_user_gallery_pic']:
        query=[]
        if tablename==b'_user':
            anduser=b''
            needuser=False
        else:
            anduser=b' AND _user=$'
            needuser=True

        query.append(b"WITH")
        query.append(b"select1 AS (UPDATE "+tablename+b" SET _deleted=_deleted+1 WHERE _deleted>0"+anduser+b"),") # update all deleted in that partition
        query.append(b"select2 AS (UPDATE "+tablename+b" SET _deleted=_deleted+1, _datelast=now() WHERE id=$"+anduser+b" RETURNING *)") # update just that row
        query.append(b"SELECT * FROM select2")
        query=b' '.join(query)
        query_args=[]
        query_args.append(lastobject_id)
        if needuser: 
            query_args.append(firstobject_id)
            query_args.append(firstobject_id)
    else:
        query=b"DELETE FROM "+tablename+b" WHERE id=$1 RETURNING *"
        query_args=[lastobject_id]
    (query,query_args)=transform(query,query_args)
    atpic.log.debug(yy,'output=',query,query_args)
    return (query,query_args)

def forge_insert(pxplo,tablename,indic):
    """
    Input: pxplo=the URLS parameters, indic=the input dictionary in POST data
    """
    yy=atpic.log.setname(xx,"forge_insert")
    atpic.log.debug(yy,"pxplo=%s" % pxplo)
    atpic.log.debug(yy,indic)
    query=b"INSERT INTO "+tablename
    # convert a dictionary into a list of key-value
    inlist=list(indic.items())
    inlist.sort(key=keysort)
    try:
        (inkeylist,invaluelist)=zip(*inlist)
    except:
        (inkeylist,invaluelist)=([],[])

    # we will use those lists:
    inkeylist2=[] 
    invaluelist2=[]
    query_args=[]
    
    # first and penultimo
    lenpm=len(pxplo)-1
    if lenpm>0:
        # first of non single
        akey=pxplo.getmatrix(0,0)
        aval=pxplo.getmatrix(0,1)
        inkeylist2.append(b"_"+akey)
        invaluelist2.append(b"$")
        query_args.append(aval) 
        # penultimo
    if lenpm>1:
        akey=pxplo.getmatrix(lenpm-1,0)
        aval=pxplo.getmatrix(lenpm-1,1)
        inkeylist2.append(b"_"+akey)
        invaluelist2.append(b"$")
        query_args.append(aval) 
            
    # prepend an underscore as all SQL fields (but id) start with _
    for key in inkeylist:
        atpic.log.debug(yy,"key",key)
        inkeylist2.append(b"_"+key)
    atpic.log.debug(yy,"stage2 inkeylist2= ",inkeylist2)
    for val in invaluelist:
        invaluelist2.append(b"$") # val is a list!
        query_args.append(val) # val is a list!

    keystring=b",".join(inkeylist2)
    valstring=b",".join(invaluelist2)

    if keystring:
        what=b"("+keystring+b") VALUES ("+valstring+b")"
    else:
        what=b"DEFAULT VALUES"
    query=query+b" "+what+b" RETURNING *" # postgresql RETURNING feature inserted id


    # special case of _user: we need a root gallery
    if tablename==b'_user':
        query=b'WITH select1 AS ('+query+b"), select2 AS (INSERT INTO _user_gallery (_user,_path) SELECT select1.id,'' FROM select1) SELECT * FROM select1"
    (query,query_args)=transform(query,query_args)

    return (query,query_args)



def transform(query,query_args):
    """
    transforms the $ in $1, $2,... as the index in query_args
    """
    yy=atpic.log.setname(xx,"transform")
    atpic.log.debug(yy,"transform(",query,query_args,")")
    atpic.log.debug(yy,'len1 (dollars nb)=',query.count(b'$'),'len2 (query_args)',len(query_args))
    newquery_args=[]
    i=1
    for aarg in query_args:
        newquery_args.append(i)
        i=i+1
    atpic.log.debug(yy,"newquery_args: ", newquery_args)
    newquery_args=tuple(newquery_args)
    atpic.log.debug(yy,"newquery_args2: ", query,newquery_args)
    query2=query.split(b"$")
    atpic.log.debug(yy,"query2: ", query2)
    new_query=b""
    commandline=b""

    for i in range(0,len(newquery_args)):
        atpic.log.debug(yy,"NEW",query2[i],newquery_args[i])
        new_query=new_query+query2[i]+b"$"+int2bytes(newquery_args[i])
        commandline=commandline+query2[i]+b"'"+query_args[i]+b"'"
    new_query=new_query+query2[-1]
    commandline=commandline+query2[-1]
    # new_query=query % (newquery_args)
    # new_query=query

    atpic.log.debug(yy,"commandline= ", commandline.replace(b'\n',b' ').decode('utf8'),';')

    atpic.log.debug(yy,"new_query ", new_query)

    return (new_query,query_args)




def forge_select_post(pxplo,actions,depth):
    yy=atpic.log.setname(xx,"forge_select_post")

    atpic.log.debug(yy,"forge_select_post(%s, %s, %s)" % (pxplo,actions,depth))
    query_args=[]
    tablename=create_tablename(pxplo.keys()[:depth]) # truncate the object list


    first=pxplo.getmatrix(0,0)
    userand=b""
    if first==b"user":
        atpic.log.debug(yy,'have a user....')
        user=pxplo.getmatrix(0,1) 
        if user:   
            atpic.log.debug(yy,'have a user id')
            query_args.append(pxplo.getmatrix(0,1))
            userand=b"_user<-10 AND "
    # query="" slect 1
    # force return a NULL row with all columns:
    queryl=[]
    queryl.append(b"SELECT original_query.* FROM")
    queryl.append(b"(SELECT * FROM "+tablename+b" WHERE "+userand+b"id<0 LIMIT 1 )")
    queryl.append(b"AS original_query")
    queryl.append(b"RIGHT JOIN (SELECT 1) AS one_row ON true")
    query=b" ".join(queryl)
    if first==b'forgot':
        query=b"WITH myquery AS (SELECT id as fieldname, _email as fieldvalue from _user where id<0) SELECT myquery.* FROM myquery  RIGHT JOIN (SELECT 1) AS one_row ON true"
    query_args=[]
    return (query,query_args)




def forge_select_post_upsert(pxplo,actions,depth,authid):
    yy=atpic.log.setname(xx,"forge_select_post_upsert")

    atpic.log.debug(yy,"forge_select_post_upsert(",pxplo,actions,'depth=',depth,'authid=',authid,')')
    query_args=[]
    tablename=create_tablename(pxplo.keys()[:depth]) # truncate the object list


    first=pxplo.getmatrix(0,0)
    wheres=[]
    if first==b"user":
        atpic.log.debug(yy,'have a user....')
        user=pxplo.getmatrix(0,1) 
        if user:   
            atpic.log.debug(yy,'have a user id')
            query_args.append(pxplo.getmatrix(0,1))
            wheres.append(b"_user=$")
    # last but one
    lastboneid=pxplo.getmatrix(depth-2,1)    
    lastboneat=pxplo.getmatrix(depth-2,0)    
    wheres.append(b'_'+lastboneat+b"=$")
    query_args.append(lastboneid)

    # last
    wheres.append(b"id=$")
    query_args.append(authid)

    """
    WITH select1 AS (select id,_user from _user_gallery where _user=1),
    one AS (SELECT 1 AS uno)
    SELECT select1.* FROM select1 RIGHT JOIN one ON true;
    
    WITH select1 AS (select id,_user from _user_gallery where _user=-99999999),
    one AS (SELECT 1 AS uno)
    SELECT select1.* FROM select1 RIGHT JOIN one ON true;
    """

    queryl=[]
    queryl.append(b"WITH")
    queryl.append(b"row AS (SELECT * FROM "+tablename+b" WHERE "+b' AND '.join(wheres)+b"),")
    queryl.append(b"one AS (SELECT 1 AS uno)")
    queryl.append(b"SELECT row.* FROM row RIGHT JOIN one ON true")
    query=b" ".join(queryl)
    
    (query,query_args)=transform(query,query_args)
    return (query,query_args)


def forge_select_update(pxplo,actions,depth,start):
    yy=atpic.log.setname(xx,"forge_select_update")

    atpic.log.debug(yy,"forge_select_update(%s, %s, %s, %s)" % (pxplo,actions,depth,start))
    query_args=[]
    tablename=create_tablename(pxplo.keys()[:depth]) # truncate the object list
    first=pxplo.getmatrix(0,0)
    userand=b""
    if first==b"user":
        atpic.log.debug(yy,'have a user....')
        user=pxplo.getmatrix(0,1) 
        if user:   
            atpic.log.debug(yy,'have a user id')
            query_args.append(pxplo.getmatrix(0,1))
            userand=b"_user=$ AND "
    query=b"SELECT * FROM "+tablename
    query=query+b" WHERE "+userand+b"id=$"
    id=pxplo.getmatrix(depth-1,1)    
    query_args.append(id)

    (query,query_args)=transform(query,query_args)
    atpic.log.debug(yy,'output=',query,query_args)
    return (query,query_args)


def forge_select(pxplo,actions,depth,start,fromto,perpage):
    yy=atpic.log.setname(xx,"forge_select")
    atpic.log.debug(yy,"input=(pxplo,actions,depth,start,fromto,perpage)=",(pxplo.list(),actions,depth,start,fromto,perpage))
    id=pxplo.getmatrix(depth-1,1)    
    if id: # this is an entry
        (query,query_args)=forge_select_notransform(pxplo,actions,depth,start,fromto,perpage)
    else: # this is a collection
        # a first
        if fromto==b'from':
            newfromto=b'to'
            newstart=int2bytes(bytes2int(start)+1)
        else:
            newfromto=b'from'
            newstart=int2bytes(bytes2int(start)-1)

        newperpage=int2bytes(bytes2int(perpage)+1)
        atpic.log.debug(yy,"newperpage",newperpage)

        (query1,query_args1)=forge_select_notransform(pxplo,actions,depth,newstart,newfromto,b'1')
        (query2,query_args2)=forge_select_notransform(pxplo,actions,depth,start,fromto,newperpage)
        query=b'('+query1+b') UNION ('+query2+b') ORDER BY id ASC'
        query_args=query_args1+query_args2

    (query,query_args)=transform(query,query_args)
    atpic.log.debug(yy,"output=", (query,query_args))
    return (query,query_args)

def get_and_deleted_iszero(tablename):
    if tablename in [b'_user',b'_user_gallery',b'_user_gallery_pic']:
        and_deleted_iszero=b' AND _deleted=0'
    else:
        and_deleted_iszero=b''
    return and_deleted_iszero

def forge_select_notransform(pxplo,actions,depth,start,fromto,perpage):
    yy=atpic.log.setname(xx,"forge_select_notransform")
    atpic.log.debug(yy,"input=",(pxplo.list(),actions,depth,start))
    if fromto==b'from':
        desc_asc=b'ASC'
        greater_lower=b'>'
    else:
        desc_asc=b'DESC'
        greater_lower=b'<'

    query_args=[]
    query=[]
    tablename=create_tablename(pxplo.keys()[:depth]) # truncate the object list

    and_deleted_iszero=get_and_deleted_iszero(tablename)

    first=pxplo.getmatrix(0,0)
    query.append(b'WITH')

    # on for that table: we need storing and artefacts making sure that if no artefact we still see the line (JOIN uno)
    if pxplo.keys()[:3]==[b'user',b'gallery',b'pic'] and depth==3:
        atpic.log.debug(yy,"4a usergallerypic and depth==3")
        uid=pxplo.getmatrix(0,1)
        gid=pxplo.getmatrix(1,1)
        pid=pxplo.getmatrix(2,1)

        query.append(b'select1 AS (SELECT _partition FROM _user WHERE id=$'+and_deleted_iszero+b'),')
        query_args.append(uid)
        if pid: # an entry
            andpic=b' AND _pic=$'
            query_args.append(uid)
            query_args.append(pid)
        else: # collection
            andpic=b' AND _pic IN (SELECT id FROM _user_gallery_pic WHERE _gallery=$ AND id'+greater_lower+b'$'+and_deleted_iszero+b' ORDER BY id '+desc_asc+b' LIMIT '+perpage+b')'
            query_args.append(uid)
            query_args.append(gid)
            query_args.append(start)
        query.append(b"select2 AS (SELECT _pic,string_agg(_code||';'|| _extension||';'|| _pathstore ||';'||_pic::text||';'||_datestore::text ,'|') as _artefact FROM _user_gallery_pic_artefact WHERE _user=$"+andpic+b" GROUP BY _pic),")
        # query.append(b"select3 AS (SELECT 1 AS uno),") # uno




    # on for that table: we need storing and artefacts making sure that if no artefact we still see the line (JOIN uno)
    if pxplo.keys()[:2]==[b'user',b'gallery'] and depth==2:
        atpic.log.debug(yy,"4b usergallery and depth==2")
        uid=pxplo.getmatrix(0,1)
        gid=pxplo.getmatrix(1,1)

        # need the partition
        query.append(b'select1 AS (SELECT _partition FROM _user WHERE id=$ AND _deleted=0),')
        query_args.append(uid)
        # get the list of galleries to display
        if gid: # an entry
            query.append(b'select2 AS (SELECT $::int AS id),')
            query_args.append(gid)
        else: # collection
            query.append(b'select2 AS (SELECT id FROM _user_gallery WHERE _user=$ AND _deleted=0 AND id'+greater_lower+b'$ ORDER BY id '+desc_asc+b' LIMIT '+perpage+b'),')
            query_args.append(uid)
            query_args.append(start)

        # need to choose one pic per gallery, (preferrably one that has artefacts, e.g. the oldest)
        query.append(b'select3 AS (SELECT _gallery,min(id) AS _pic FROM _user_gallery_pic WHERE _user=$ AND _deleted=0 AND _gallery IN (SELECT id FROM select2) GROUP BY _gallery),')
        query_args.append(uid)

        # now get the agregate
        query.append(b"select5 AS (SELECT _pic,string_agg(_code||';'|| _extension||';'|| _pathstore ||';'||_pic::text||';'||_datestore::text ,'|') as _artefact FROM _user_gallery_pic_artefact WHERE _user=$ AND _pic IN (SELECT _pic FROM select3) GROUP BY _pic),")
        query_args.append(uid)
        # now join gallery with aggregate
        query.append(b'select6 AS (SELECT select3._gallery,select5._artefact FROM select3 JOIN select5 ON select5._pic=select3._pic),')
        
        
        
    # restrict on user
    if pxplo.getmatrix(0,0)==b"user" and depth>1:
        atpic.log.debug(yy,"10 partition by user")
        user_and=tablename+b"._user=$ AND "
        query_args.append(pxplo.getmatrix(0,1))
    else:
        user_and=b''

    # restrict on parent
    if len(pxplo) - depth < 1 and depth > 2:
        atpic.log.debug(yy,"10 avantdernier")
        # avantdernier
        avantdernier_and=tablename+b"._"+pxplo.getmatrix(len(pxplo)-2,0)+b"=$ AND "  # BUGGGGGGG
        query_args.append(pxplo.getmatrix(len(pxplo)-2,1))
    else:
        avantdernier_and=b''
        # http://alex.atpic.faa/gallery/38764/pic/2019119


    # main entry/collection query
    id=pxplo.getmatrix(depth-1,1)    
    if id: # this is an entry
        query.append(b"select4 AS (SELECT "+tablename+b".* FROM "+tablename+b" WHERE "+user_and+avantdernier_and+tablename+b".id=$"+and_deleted_iszero+b")")
        query_args.append(id)

    else: # this is a collection
        # we do not use offset as it is memory extensive, we use >
        query.append(b"select4 AS (SELECT "+tablename+b".* FROM "+tablename+b" WHERE "+user_and+avantdernier_and+tablename+b".id"+greater_lower+b'$'+and_deleted_iszero+b" ORDER BY "+tablename+b".id "+desc_asc+b" LIMIT "+perpage+b")")
        query_args.append(start)

    # finally
    if pxplo.keys()[:3]==[b'user',b'gallery',b'pic'] and depth==3:
        query.append(b"SELECT * FROM select4 JOIN select1 ON true LEFT JOIN select2 ON select2._pic=select4.id ORDER BY id ASC") # final order
    elif pxplo.keys()[:2]==[b'user',b'gallery'] and depth==2:
        query.append(b"SELECT * FROM select4 JOIN select1 ON true LEFT JOIN select6 ON select6._gallery=select4.id ORDER BY id ASC") # final order

    else:
        query.append(b"SELECT * FROM select4 ORDER BY id ASC") # final order

    query=b' '.join(query)
    atpic.log.debug(yy,"output=", (query,query_args))
    return (query,query_args)


def forge_selectforgot(indic):
    yy=atpic.log.setname(xx,"forge_selectforgot")
    atpic.log.debug(yy,'input',indic)
    query=b'SELECT id,_email,_name,_servershort FROM _user WHERE '+indic[b'fieldname']+b'=$1'
    query_args=[indic[b'fieldvalue'],]
    atpic.log.debug(yy,'output',(query,query_args))
    return (query,query_args)


def forge_query(pxplo,actions,depth,lang,environ,indata=(),start=b"0",perpage=b'10',fromto=b'from',direction=b'+',authid=b''):
    """
    Returns a SQL query and arguments in a list
    Can be unit tested.

    depth should be >=1
    """

    # pxplo=pxplo.int()
    yy=atpic.log.setname(xx,"forge_query")
    query=b""
    query_args=[]
    query_args=pxplo.values()[0:depth]
    
    atpic.log.debug(yy,"+++++++++++++++++++++++++++++")
    atpic.log.debug(yy,"forge_query(",pxplo.list(),',',actions,',',depth,',',lang,',',indata,',',"start=",start,'perpage=',perpage,'fromto=',fromto,'direction=',direction,'authid=',authid)
    olist_len=len(pxplo)
    indic=atpic.indatautils.setdicfiles(indata)
 
    tablename=create_tablename(pxplo.keys()[:depth]) # truncate the object list
    atpic.log.debug(yy,"tablename",tablename)
    lastobject_id=pxplo.getmatrix(len(pxplo)-1,1)


    keysnorev=copy.deepcopy(pxplo.keys())
    lastrev=keysnorev.pop()
    if lastrev!=b'revision':
        keysnorev.append(lastrev)
    if actions in (
        [b'get'],
        [b'get',b'put'],
        [b'get',b'post']
        ) and depth==len(keysnorev) and (keysnorev in (
            [b'wiki'],
            [b'user',b'wiki'],
            )):

        atpic.log.debug(yy,"this is a SELECT wiki")
        if actions==[b'get']:
            allownull=False
        else:
            allownull=True
        atpic.log.debug(yy,"allownull is",allownull)
        
        (query,query_args)=forge_selectversion(pxplo,actions,depth,lang,start,fromto,perpage,allownull)

    elif actions==[b"get"] or depth<len(pxplo):
        # need a selectversion for wiki
        atpic.log.debug(yy,"this is a SELECT depth=%s, len=%s" % (depth,len(pxplo)))
        (query,query_args)=forge_select(pxplo,actions,depth,start,fromto,perpage)

    elif actions==[b"post"] or actions==[b"post",b"post"]:
        atpic.log.debug(yy,"this is a POST")
        lastone=pxplo.getmatrix(len(pxplo)-1,0)
        if lastone in [b'tag',b'phrase',b'vote',b'friend']: 
            atpic.log.debug(yy,"this is a POST UPSERT")
            if lastone in [b'tag',b'phrase',b'vote']: 
                # modify pxplo putting as 'id' the authenticated user
                # note that for friend this isnot necessary
                plist=pxplo.list()
                (k,v)=plist.pop()
                plist.append((k,authid))
                pxplo_new=atpic.xplo.Xplo(plist)
            elif lastone in [b'friend']:
                # modify pxplo the 'friend' in {'friend':'99} data into a virtual PUT /user/1/friend/99
                friendid=indic[b'friend']
                indic={} # erase the indata
                plist=pxplo.list()
                (k,v)=plist.pop()
                plist.append((k,friendid))
                pxplo_new=atpic.xplo.Xplo(plist)
            (query,query_args)=forge_upsert(pxplo,tablename,indic)
        elif lastone in [b'pm',]:
            atpic.log.debug(yy,"this is a PM POST (double insert CTE)")
            (query,query_args)=forge_insertpm(pxplo,tablename,indic,authid)
        elif lastone in [b'wiki','user_wiki']:
            atpic.log.debug(yy,"this is version insert")
            (query,query_args)=forge_insertversion(pxplo,tablename,lang,environ,indic,authid)
        elif lastone in [b'forgot']:
            atpic.log.debug(yy,"this a forgot pseudo POST, in fact a SELECT")
            (query,query_args)=forge_selectforgot(indic)
        else:    
            atpic.log.debug(yy,"this is a normal POST")
            (query,query_args)=forge_insert(pxplo,tablename,indic)
    elif actions==[b"get",b"post"]:
        # e.g: GET http://alex.atpic.faa/gallery/post
        query=b""
        query_args=[]
        atpic.log.debug(yy,"we need to present a post form")
        lastone=pxplo.getmatrix(len(pxplo)-1,0)
        if lastone in [b'tag',b'phrase',b'vote',b'friend']:     
            atpic.log.debug(yy,"we need to present an upsert post form")
            (query,query_args)=forge_select_post_upsert(pxplo,actions,depth,authid)
        else:  
            # force return a NULL row with all columns:
            # SELECT original_query.* FROM
            # (select * from _user where id<0 limit 1 ) AS original_query
            # RIGHT JOIN (SELECT 1) AS one_row ON true;
            atpic.log.debug(yy,"we need to present a normal post form")
            (query,query_args)=forge_select_post(pxplo,actions,depth)

    elif actions==[b"put"] or actions==[b"post",b"put"]:
        atpic.log.debug(yy,"we need to do a SQL UPDATE")
        if pxplo.keys()==[b"user",b"gallery",b"gallery"]:
            pass # deprecated
        else:
            lastone=pxplo.getmatrix(len(pxplo)-1,0)
            if lastone in [b'tag',b'phrase',b'vote',b'friend']:
                atpic.log.debug(yy,'SQL UPSERT')
                (query,query_args)=forge_upsert(pxplo,tablename,indic)
            elif lastone in [b'wiki','user_wiki']:
                atpic.log.debug(yy,"this is version insert")
                (query,query_args)=forge_insertversion(pxplo,tablename,lang,environ,indic,authid)
            else:
                (query,query_args)=forge_update(pxplo,tablename,indic)
    elif actions==[b"get",b"put"]:
        # e.g: GET http://alex.atpic.faa/gallery/1/put
        atpic.log.debug(yy,"we need to present a PUT form")
        # we just do a regular select
        (query,query_args)=forge_select(pxplo,actions,depth,start,fromto,perpage)
    elif actions==[b"delete"] or actions==[b"post",b"delete"]:
        atpic.log.debug(yy,"we need to do a SQL DELETE")
        firstobject_id=pxplo.getmatrix(0,1)


        (query,query_args)=forge_delete(tablename,firstobject_id,lastobject_id)
    elif actions==[b"get",b"delete"]:
        atpic.log.debug(yy,"we need Do  you confirm DELETE?")
        # we just do a regular select to then confirm the delete
        (query,query_args)=forge_select(pxplo,actions,depth,start,fromto,perpage)
        


    atpic.log.debug(yy,"query %s" % query)
    atpic.log.debug(yy,"query_args %s" % query_args)

    atpic.log.debug(yy,"output=",query,',',query_args)
    # return (b'aaaa'+query,query_args)
    return (query,query_args)




# ===============================================================
#
# fuse FS related:
#
# ===============================================================

# ---------------------------------------
# Utilities
# ---------------------------------------
def get_login_dirpath(path):
    # utility used by dirtype and rename gallery
    yy=atpic.log.setname(xx,"get_login_dirpath")
    atpic.log.debug(yy,"input=",path)
    path=path.strip(b'/')
    splitted=path.split(b'/')
    atpic.log.debug(yy,"splitted=",splitted)
    login=splitted[0]
    atpic.log.debug(yy,"login=",login)
    dirpath=b'/'.join(splitted[1:])
    atpic.log.debug(yy,"dirpath=",dirpath)
    atpic.log.debug(yy,"output=(login,dirpath)",(login,dirpath))
    return (login,dirpath)







def get_login_dirpath_picname(path):
    # utility used by dirtype and rename gallery
    yy=atpic.log.setname(xx,"get_login_dirpath_picname")
    atpic.log.debug(yy,"input=",path)



    path=path.strip(b'/')
    splitted=path.split(b'/')
    atpic.log.debug(yy,"splitted=",splitted)
    # we have three parts
    atpic.log.debug(yy,"splitted=",splitted)
    login=splitted[0]
    atpic.log.debug(yy,"login=",login)
    dirpath=b'/'.join(splitted[1:-1])
    atpic.log.debug(yy,"dirpath=",dirpath)
    picname=splitted[-1]

    return (login,dirpath,picname)




# ================================================================
#
#  FUSE Functions
#
# ================================================================


def forge_dirlist(path):
    # list the directories children of a directory
    # use by filesystem (fuse)
    # path can be
    # alex
    # alex/italia2006
    # alex/italia2006/firenze
    # USER/DIRPATH=PATH
    yy=atpic.log.setname(xx,"forge_dirlist")
    atpic.log.debug(yy,"input=",path)

    (login,dirpath)=get_login_dirpath(path)


    path=path.strip(b'/')
    splitted=path.split(b'/')
    depth=len(splitted)




    query=[]
    query.append(b"WITH")
    query.append(b"select1 AS (SELECT _path FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$1 AND _user._deleted=0 AND _user_gallery._deleted=0 AND _user_gallery._path ~ $2),")
    query.append(b"select2 AS (SELECT string_to_array(_path,'/') as pathar FROM select1),")
    query.append(b'select3 AS (SELECT pathar[$3] as dirname FROM select2)')
    query.append(b'SELECT DISTINCT ON (dirname) dirname FROM select3 ORDER by dirname')
    query=b' '.join(query)
    if dirpath==b'': # root
        # dirpathregex=b'^[^/]+$'
        dirpathregex=b'.+' # list all not null
    else:
        # dirpathregex=b'^'+dirpath+b'/[^/]+$'
        dirpathregex=b'^'+dirpath+b'/.+$'
    query_args=[]
    query_args.append(login)
    query_args.append(dirpathregex)
    query_args.append(int2bytes(depth))
    atpic.log.debug(yy,"output=",(query,query_args))
    return (query,query_args)


def forge_piclist(path):
    # get the list of pics names and their pathstores (used to get stats)
    # that are children of a directory
    # diretcory can be 
    # /alex
    # /alex/italia2006
    yy=atpic.log.setname(xx,"forge_piclist")
    atpic.log.debug(yy,"input=",path)


    (login,dirpath)=get_login_dirpath(path)


    query=[]
    query.append(b"WITH")
    query.append(b"select1 AS (SELECT _user._partition AS partition,_user_gallery.id AS gid, _user_gallery._user AS uid FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$ AND _user._deleted=0 AND _user_gallery._path = $ AND _user_gallery._deleted=0),")
    query.append(b"select2 AS (SELECT _user_gallery_pic._originalname AS originalname, '/' || select1.partition ||'/'||_user_gallery_pic._pathstore as fullpathstore FROM _user_gallery_pic JOIN select1 ON select1.gid=_user_gallery_pic._gallery WHERE _user_gallery_pic._user=select1.uid AND _user_gallery_pic._deleted=0)") # fastdir, partition
    query.append(b'SELECT * FROM select2 ORDER BY originalname')


    query=b' '.join(query)
    
    query_args=[]
    query_args.append(login)
    query_args.append(dirpath)
    (query,query_args)=transform(query,query_args)
    atpic.log.debug(yy,"output=",(query,query_args))
    return (query,query_args)

def forge_createfile(path):
    # used by fuse
    pass


def forge_mkdir(path):
    yy=atpic.log.setname(xx,"forge_mkdir")

    atpic.log.debug(yy,"input=",path)

    (login,dirpath)=get_login_dirpath(path)

    query=[]
    query.append(b"WITH")
    query.append(b"select1 AS (SELECT _user.id AS uid FROM _user WHERE _user._login=$ AND _user._deleted=0)")
    query.append(b"INSERT INTO _user_gallery (_user,_path) (SELECT uid,$ FROM select1) RETURNING *")
    query=b' '.join(query)
    
    query_args=[]
    query_args.append(login)
    query_args.append(dirpath)

    (query,query_args)=transform(query,query_args)
    atpic.log.debug(yy,"output=",(query,query_args))

    return (query,query_args)
    

def forge_rmdir(path):
    yy=atpic.log.setname(xx,"forge_rmdir")

    atpic.log.debug(yy,"input=",path)

    (login,dirpath)=get_login_dirpath(path)


    query=[]

    query.append(b"WITH")
    query.append(b"select1 AS (SELECT _user.id AS uid FROM _user WHERE _user._login=$ AND _user._deleted=0),")
    query.append(b"select2 AS (UPDATE _user_gallery SET _deleted=_deleted+1 WHERE _deleted>0 AND _user=(SELECT uid FROM select1)),") # update all deleted in that partition
    query.append(b"select3 AS (UPDATE _user_gallery SET _deleted=_deleted+1, _datelast=now() WHERE _path=$ AND _user=(SELECT uid FROM select1) AND _deleted=0 RETURNING *)") # update just that row
    query.append(b"SELECT * FROM select3")
    query=b' '.join(query)

    query_args=[]
    query_args.append(login)
    query_args.append(dirpath)

    (query,query_args)=transform(query,query_args)
    atpic.log.debug(yy,"output=",(query,query_args))

    return (query,query_args)
    








def forge_unlink(path):
    """
    Unlinks a picture
    """
    yy=atpic.log.setname(xx,"forge_unlink")
    atpic.log.debug(yy,"input=",path)

    (login,dirpath,picname)=get_login_dirpath_picname(path)

    query=[]

    # http://stackoverflow.com/questions/4005969/increment-field-with-not-null-and-unique-constraint-in-postgresql-8-3
    # http://www.postgresql.org/docs/9.1/static/sql-set-constraints.html
    # DEFERRED constraint
    # SET CONSTRAINTS ALL DEFERRED;
    # -- Uniqueness and exclusion constraints that have not been declared DEFERRABLE are also checked immediately.
    query.append(b"WITH")
    query.append(b"select1 AS (SELECT _user.id AS uid FROM _user WHERE _user._login=$ AND _user._deleted=0),")
    query.append(b"select2 AS (SELECT id AS gid FROM _user_gallery WHERE _path=$ AND _user=(SELECT uid FROM select1) AND _deleted=0),")
    query.append(b"select3 AS (UPDATE _user_gallery_pic SET _deleted=_deleted+1 WHERE _deleted>0 AND _user=(SELECT uid FROM select1) AND _gallery=(SELECT gid FROM select2)),") # update all deleted in that partition
    query.append(b"select4 AS (UPDATE _user_gallery_pic SET _deleted=_deleted+1,_datelast=now() WHERE _originalname=$ AND _user=(SELECT uid FROM select1) AND _gallery=(SELECT gid FROM select2) AND _deleted=0 RETURNING *)") # update just that row
    query.append(b"SELECT * FROM select4")
    query=b' '.join(query)

    query_args=[]
    query_args.append(login)
    query_args.append(dirpath)
    query_args.append(picname)

    (query,query_args)=transform(query,query_args)
    atpic.log.debug(yy,"output=",(query,query_args))

    return (query,query_args)
    



def forge_dirtype(path):
    # tells if a gallery
    # ismissing
    # isreal
    # isvirtual
    yy=atpic.log.setname(xx,"forge_dirtype")
    atpic.log.debug(yy,"input=",path)

    (login,dirpath)=get_login_dirpath(path)
    query=[]
    query.append(b"WITH")
    query.append(b"select1 AS (SELECT _user.id AS uid FROM _user WHERE _user._login=$ AND _user._deleted=0),")
    # first try exact path, special case of root gallery
    query.append(b"select2 AS (SELECT 'isreal'::text AS res FROM _user_gallery WHERE _user=(SELECT uid FROM select1) AND _path=$ AND _deleted=0),")
    query.append(b"select3 AS (SELECT 'isvirtual'::text AS res FROM _user_gallery WHERE NOT EXISTS (SELECT 1 FROM select2) AND _deleted=0 AND _path ~ $ AND _user=(SELECT uid FROM select1)),") 
    query.append(b"select4 AS (SELECT 'ismissing'::text AS res WHERE NOT EXISTS (SELECT 1 FROM select2) AND NOT EXISTS (SELECT 1 FROM select3) AND ''!=$),") 
    query.append(b"select5 AS (SELECT 'missingroot'::text AS res WHERE NOT EXISTS (SELECT 1 FROM select2) AND NOT EXISTS (SELECT 1 FROM select3) AND ''=$)") 
    query.append(b"SELECT * FROM select2 UNION SELECT * FROM select3 UNION SELECT * FROM select4 UNION SELECT * FROM select5")
    query=b' '.join(query)
    
    query_args=[]
    query_args.append(login)
    query_args.append(dirpath)
    query_args.append(b'^'+dirpath+b'/.*')
    query_args.append(dirpath)
    query_args.append(dirpath)

    (query,query_args)=transform(query,query_args)
    atpic.log.debug(yy,"output=",(query,query_args))

    return (query,query_args)
    


def forge_rename_gallery(path_old,path_new):
    yy=atpic.log.setname(xx,"forge_rename_gallery")
    atpic.log.debug(yy,"input=",path_old,path_new)
    query=[]
    # can rename a gallery only if old is a real gallery and new does not exist (virtual?)

    (login_old,dirpath_old)=get_login_dirpath(path_old)
    (login_new,dirpath_new)=get_login_dirpath(path_new)

    if login_old!=login_new:
        atpic.log.debug(yy,"error! cannot move galleries across users")
        raise()
    else:
        login=login_old

    query.append(b"WITH")
    query.append(b"select1 AS (SELECT _user.id AS uid FROM _user WHERE _user._login=$ AND _user._deleted=0)")
    query.append(b"UPDATE _user_gallery SET _path=$ WHERE _user=(SELECT uid FROM select1) AND _path=$ AND _deleted=0 RETURNING *")
    query=b' '.join(query)



    query_args=[]
    query_args.append(login)
    query_args.append(dirpath_new)
    query_args.append(dirpath_old)

    (query,query_args)=transform(query,query_args)
    atpic.log.debug(yy,"output=",(query,query_args))

    return (query,query_args)












def forge_rename_picture(path_old,path_new):
    yy=atpic.log.setname(xx,"forge_rename_picture")
    atpic.log.debug(yy,"input=",path_old,path_new)
    query=[]
    # can rename a gallery only if old is a real gallery and new does not exist (virtual?)


    (login_old,dirpath_old,picname_old)=get_login_dirpath_picname(path_old)
    (login_new,dirpath_new,picname_new)=get_login_dirpath_picname(path_new)

    if login_old!=login_new:
        atpic.log.debug(yy,"error! cannot move pictures across users")
        raise()
    else:
        login=login_old

    query.append(b"WITH")
    query.append(b"select1 AS (SELECT _user.id AS uid FROM _user WHERE _user._login=$ AND _user._deleted=0),")
    query.append(b"select2 AS (SELECT _user_gallery.id AS gid_old FROM _user_gallery WHERE _user=(SELECT uid FROM select1) AND _path=$ AND _deleted=0),")
    query.append(b"select3 AS (SELECT _user_gallery.id AS gid_new FROM _user_gallery WHERE _user=(SELECT uid FROM select1) AND _path=$ AND _deleted=0)")
    query.append(b"UPDATE _user_gallery_pic SET _originalname=$,_gallery=(SELECT gid_new FROM select3) WHERE _user=(SELECT uid FROM select1) AND _gallery=(SELECT gid_old FROM select2) AND _originalname=$ AND _deleted=0 AND EXISTS (SELECT 1 FROM select2) AND EXISTS (SELECT 1 FROM select3) RETURNING *")

    query=b' '.join(query)


    query_args=[]
    query_args.append(login)
    query_args.append(dirpath_old)
    query_args.append(dirpath_new)
    query_args.append(picname_new)
    query_args.append(picname_old)

    (query,query_args)=transform(query,query_args)
    atpic.log.debug(yy,"output=",(query,query_args))

    return (query,query_args)





def forge_picpathstore(path):
    # from a pic path like
    # alex/italia2006/firenze/immagine_292.jpg 
    # outputs: 
    # /a/o/1/7701/0/291571/0.jpg
    yy=atpic.log.setname(xx,"forge_picpathstore")
    atpic.log.debug(yy,"input=",path)



    (login,dirpath,picname)=get_login_dirpath_picname(path)




    query=[]
    query.append(b"WITH")
    query.append(b"select1 AS (SELECT _user._partition AS partition,_user_gallery.id AS gid, _user_gallery._user AS uid FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$ AND _user._deleted=0 AND _user_gallery._path = $ AND _user_gallery._deleted=0),")
    query.append(b"select2 AS (SELECT '/' || select1.partition ||'/'||_user_gallery_pic._pathstore as _fullpathstore,_user_gallery_pic.*,select1.partition as _partition FROM _user_gallery_pic JOIN select1 ON select1.gid=_user_gallery_pic._gallery WHERE _user_gallery_pic._user=select1.uid AND _user_gallery_pic._originalname=$ AND _user_gallery_pic._deleted=0)")
    query.append(b'SELECT * FROM select2')
    query=b' '.join(query)
    
    query_args=[]
    query_args.append(login)
    query_args.append(dirpath)
    query_args.append(picname)
    (query,query_args)=transform(query,query_args)
    atpic.log.debug(yy,"output=",(query,query_args))

    return (query,query_args)
    
def forge_fuseupsert(path):
    # from a pic path like
    # alex/italia2006/firenze/immagine_292.jpg 
    yy=atpic.log.setname(xx,"forge_fuseupsert")
    atpic.log.debug(yy,"input=",path)



    (login,dirpath,picname)=get_login_dirpath_picname(path)

 
    query=[]
    query.append(b'WITH')
    query.append(b'select1 AS (SELECT _user._partition AS _partition,_user_gallery.id AS gid, _user_gallery._user AS uid FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user._login=$ AND _user_gallery._path = $ AND _user._deleted=0 AND _user_gallery._deleted=0),')
    query.append(b'select2 AS (SELECT _user_gallery_pic.* FROM _user_gallery_pic JOIN select1 ON _user_gallery_pic._user=select1.uid AND _user_gallery_pic._gallery=select1.gid WHERE _originalname=$ AND _user_gallery_pic._deleted=0),')
    query.append(b'select3 AS (INSERT INTO _user_gallery_pic (_user,_gallery,_originalname,_pathstore) (SELECT uid,gid,$,$ FROM select1 WHERE NOT EXISTS (SELECT 1 FROM select2)) RETURNING *),')
    query.append(b"select4 AS (SELECT 'update' AS _upsert,* FROM select2 UNION SELECT 'insert' AS _upsert,* FROM select3)")
    query.append(b"SELECT select4.*,select1._partition FROM select4 JOIN select1 ON select1.uid=select4._user")


    query_args=[]
    query_args.append(login)
    query_args.append(dirpath)
    query_args.append(picname)
    query_args.append(picname)
    query_args.append(atpic.randomalpha.myrandomfile())

    query=b' '.join(query)
    (query,query_args)=transform(query,query_args)
    atpic.log.debug(yy,"output=",(query,query_args))

    return (query,query_args)


def asyncpro(message):
    # this is a zmq process message to insert into artefacts or update pic metadata
    yy=atpic.log.setname(xx,"select_asyncpro")
    atpic.log.debug(yy,"input=",message)
    query=[]

    splitted=message.split(b'|')
    query_args=[]
    atpic.log.debug(yy,'splitted',splitted)
    if splitted[0]==b'A': # A like Artefact
        atpic.log.debug(yy,'need insert into artefact')
        query.append(b'INSERT INTO _user_gallery_pic_artefact (_user,_pic,_sizeb,_code,_extension,_pathstore) VALUES ($,$,$,$,$,$)')
        query_args=splitted[1:]
    elif splitted[0]==b'U': # U like Update an existing pic
        atpic.log.debug(yy,'need update pic metadata')
        # look at asyncpro 'U'
        (uid,pid,mime_exiftool,width,height,duration,make,model,aperture,exposuretime,focallength,flash,whitebalance,exposuremode,datetimeoriginal,gpslat,gpslon)=splitted[1:]

        query.append(b'UPDATE _user_gallery_pic SET')
        squery=[]

        if width!=b'':
            squery.append(b'_width=$')
            query_args.append(width)

        if height!=b'':
            squery.append(b'_height=$')
            query_args.append(height)

        if duration!=b'':
            squery.append(b'_duration=$')
            query_args.append(duration)

        squery.append(b'_exifmake=$')
        query_args.append(make)
        squery.append(b'_exifmodel=$')
        query_args.append(model)
        squery.append(b'_exifaperture=$')
        query_args.append(aperture)
        squery.append(b'_exifexposuretime=$')
        query_args.append(exposuretime)
        squery.append(b'_exiffocallength=$')
        query_args.append(focallength)
        squery.append(b'_exifflash=$')
        query_args.append(flash)
        squery.append(b'_exifwhitebalance=$')
        query_args.append(whitebalance)
        squery.append(b'_exifexposuremode=$')
        query_args.append(exposuremode)
        squery.append(b'_exifdatetimeoriginal=$')
        query_args.append(datetimeoriginal)
        # need sql
        sqldate=atpic.dateutils.date_exif2sql(datetimeoriginal)
        if sqldate!=b'':
            squery.append(b'_datetimeoriginalsql=$')
            query_args.append(sqldate)
        if gpslat!=b'':
            squery.append(b'_exifgpslat=$')
            query_args.append(gpslat)
        if gpslon!=b'':
            squery.append(b'_exifgpslon=$')
            query_args.append(gpslon)

        # 
        (mimetype,mimesubtype)=mime_exiftool.split(b'/')
        squery.append(b'_mimetype_exiftool=$')
        query_args.append(mimetype)
        squery.append(b'_mimesubtype_exiftool=$')
        query_args.append(mimesubtype)
        # squery.append(b'=$')
        # query_args.append()
 
        query.append(b', '.join(squery))

        query.append(b'WHERE _user=$ AND id=$')
        query_args.append(uid)
        query_args.append(pid)
    query=b' '.join(query)
    (query,query_args)=transform(query,query_args)
    atpic.log.debug(yy,"output=",(query,query_args))

    return (query,query_args)



def forge_wikiimage(uid,pid,code):
    yy=atpic.log.setname(xx,"forge_wikiimage")
    query=[]
    query.append(b'WITH')
    query.append(b'select1 AS (SELECT _user_gallery_pic_artefact.* FROM _user_gallery_pic_artefact WHERE _user=$ AND _pic=$ AND _code=$),')
    query.append(b'select2 AS (SELECT _user_gallery_pic.id,_user_gallery_pic._gallery FROM _user_gallery_pic WHERE _user=$ AND id=$ AND _deleted=0)')
    query.append(b'SELECT * FROM select1 JOIN select2 ON select1._pic=select2.id')
    # do not take into account deleted yet
    # _user._partition AS _partition FROM _user JOIN _user_gallery ON _user_gallery._user=_user.id WHERE _user.id=$ AND _user._deleted=0 AND _user_gallery._deleted=0')
    query=b' '.join(query)
    query_args=[]
    query_args.append(uid)
    query_args.append(pid)
    query_args.append(code)
    query_args.append(uid)
    query_args.append(pid)
    (query,query_args)=transform(query,query_args)
    atpic.log.debug(yy,"output=",(query,query_args))

    return (query,query_args)



if __name__ == "__main__":
    print('hi')
    pxplo=atpic.xplo.Xplo([(b"user",b"1"),(b"gallery",b"2"),(b"pic",b"3")])
    # forge_query(pxplo,actions,environ,depth)

# needs postgresql 9.1
# needs a UNIQUE to make prevent duplicates in race conditions
"""
CREATE TABLE actor (fname text,lname text, last_update timestamp);

WITH upsert AS (UPDATE actor SET last_update=now() WHERE fname='Alex' and lname='Madon' returning *)
INSERT INTO actor (fname, lname,last_update) 
SELECT 'Alex','Madon',now() WHERE NOT EXISTS (SELECT 1 FROM upsert) 
RETURNING *;


WITH 
upsert1 AS (UPDATE actor SET last_update=now() WHERE fname='Alex4' and lname='Madon' returning *),
upsert2 AS (INSERT INTO actor  (fname, lname,last_update) SELECT 'Alex4','Madon',now() WHERE NOT EXISTS (SELECT 1 FROM upsert) 
RETURNING *)
SELECT * FROM UPSERT1 UNION SELECT * FROM UPSERT2;


WITH 
upsert AS (UPDATE actor SET last_update=now() WHERE fname='Alex' and lname='Madon' returning *),
upsert2 AS (UPDATE actor SET last_update=now() WHERE fname='Alex' and lname='Madon' returning *)
SELECT * FROM UPSERT;




select * from actor;




WITH upsert AS (UPDATE _user_gallery_pic_tag SET _text='paris france',_datelast=now() WHERE id=1 AND _pic=24 returning *)
INSERT INTO _user_gallery_pic_tag (id,_pic,_text,_datelast) 
SELECT 1,24,'paris france',now() WHERE NOT EXISTS (SELECT 1 FROM upsert) RETURNING *;

SELECT * FROM _user_gallery_pic_tag WHERE id=1;

NEED a UNIQUE on id,_pic
"""
