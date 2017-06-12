#!/usr/bin/python3
"""
journal is an interceptor that is called each time there is a PUT, POST, DELETE.
data is stored in elasticsearch with permissions to query.
elasticsearch databases are small, routing by user and split by date
YYY-MM-DD
not sure about the resolution of the tables?

internally, we use elasticsearch templates:
you do NOT need to create an index, the first write request to an index that matches the template pattern (here log*) will create the index.

for search, search against a non existing index will fail.

query language:
default: () and (uid:1 or aid:1)
admin: whatewever
+uid:1 +path:/user/1/gallery/2 +datepath:/2013/06

do we really need a full blown queryparser???

atpic.com/journal/user/2/gallery/23
atpic.com/journal/wiki
atpic.com/journal?aid=1
or
atpic.com/journal?q=-aid:2
atpic.com/journal?q=-aid:2 +uid:2
atpic.com/journal?q=+aid:2 -uid:2
atpic.com/journal/user?q=+method:post
atpic.com/journal?q=path:/user/1/gallery/23/*
atpic.com/journal/user/2/gallery/23?q=date:201306
atpic.com/journal/2013/user/2/gallery/23
atpic.com/journal/201306/user/2/gallery/23

easy navigation criteria:

atpic.com/journal/user/1
has links to:
atpic.com/journal/user/1/gallery/23
atpic.com/journal/user/1/gallery/24
atpic.com/journal/user/1/[gallery]



security is more basic that for search:
if admin: can see everytghing
else: can view only with same uid or aid than the authenticated user


curl -v -X PUT -d 'text=some more tags put' "http://username:passwd@alex.atpic.faa/gallery/1/tag/1?f=xml"
"""


# what do we use as input?
# python array?
# xml? json?

# what are the fields?
# what is the size of the table?

# similar to stats
# this is a auditing-like capability
"""
journal:
date
table
permission

(do not show passwords)

do we do a SQL component for each row??
slow....
get the unique ID

in elasticsearch can store:
pxplo0_name,
pxplo0_value,
etc..

or
name: value
but then can not allow twice the same name in path pxplo
/user/1/gallery/22/pic/33
can do a XPATH:/*
GOOD!!!!

store in elasticesearch
servershort
or as it is mutable, you could look it up in RAM
and store only the UID


curl -XGET 'http://localhost:9200/log2013/journal/_search'
curl -XGET 'http://localhost:9200/log2013/journal/_search?pretty=1'
curl -XGET 'http://localhost:9200/log2013/journal/_search?q=aid:1&pretty=1'
curl -XGET 'http://localhost:9200/log2013/journal/973838e5-909c-408a-bcec-d4a9dd6d6785?pretty=1'

"""
import time
import uuid

import atpic.log
import atpic.mybytes
import atpic.xplo
import atpic.zmq_elastic_client

xx=atpic.log.setmod("INFO","journal")

def unquote(ss): # escape the double quotes
    return ss.replace(b'"',b'\\"')

def forge_json(hxplo,pxplo,actions,indata,environ,uid,aid,axml):
    """
    This is the json to PUT new data into the journal in elasticsearch
    """
    yy=atpic.log.setname(xx,'forge_json')
    atpic.log.debug(yy,'input=',(hxplo.list(),pxplo.list(),indata,environ,actions,axml))
    ajson=[]
    lastaction=actions[-1]
    ajson.append(b'{')
    ajson.append(b'"action" : "'+lastaction+b'",')

    

    ajson.append(b'"datestore" : "'+atpic.dateutils.elastic_now()+b'",')


    path=environ[b'PATH_INFO']
    if uid!=b'':
        path=b'/user/'+uid+path
        ajson.append(b'"uid" : "'+uid+b'",')
    # need to remove ending /put /post /delete
    ajson.append(b'"path" : "'+path.rstrip(b'/')+b'",')

    path_dirs=path.strip(b'/').split(b'/')
    fpath=b''
    depth=0
    last=path_dirs[-1]
    if last in (b'get',b'post',b'put',b'delete'):
        path_dirs.pop()

    for adir in path_dirs:
        fpath=fpath+b'/'+adir
        ajson.append(b'"dir_'+atpic.mybytes.int2bytes(depth)+b'" : "'+unquote(fpath)+b'",')
        depth=depth+1

    for (key,isfile,value) in indata:
        if not isfile:
            ajson.append(b'"'+key+b'" : "'+unquote(value)+b'",') # NEED TO ESCAPE DOUBLE QUOTE, TODO
        else:
            ajson.append(b'"onefile": true,')
    ajson.append(b'"aid" : "'+aid+b'"')
    # indata is a list, difficult to store in a dictionary
    # could store anyway in a dict, taking only the first value
    # could store in a dict, storing all values
    # could store in field_1, value_1
    ajson.append(b'}')

    ajsons=b''.join(ajson)
    atpic.log.debug(yy,'ouput=',ajsons)
    return ajsons


def update_journal(essock,hxplo,pxplo,actions,indata,environ,uid,aid,axml):
    yy=atpic.log.setname(xx,'update_journal')
    atpic.log.debug(yy,'input=',(hxplo.list(),pxplo.list(),indata,environ,actions,axml))
    firstaction=actions[0]
    lastaction=actions[-1]
    if firstaction not in [b'put',b'delete',b'post',]:
        atpic.log.debug(yy,'nothing to do for firstaction:',firstaction)
    else:
        atpic.log.debug(yy,'need a journal entry for firstaction:',firstaction)
        # forge the json
        ajson=forge_json(hxplo,pxplo,actions,indata,environ,uid,aid,axml)
        atpic.log.debug(yy,'ajson',ajson)
        auuid=str(uuid.uuid4()).encode('utf8')
        # http://www.elasticsearch.org/tutorials/using-elasticsearch-for-logs/
        # we need to create a rotate on journals
        # http://www.elasticsearch.org/guide/reference/api/multi-index/
        # Using the APIs against all indices is simple by usually either using the _all index, or simply omitting the index.
        # curl -XDELETE 'http://localhost:9200/old-index-name/'
        # http://www.elasticsearch.org/guide/reference/api/search/indices-types/
        # http://www.elasticsearch.org/guide/reference/api/multi-index/
        # Using the APIs against all indices is simple by usually either using the _all index, or simply omitting the index.
        # For multi index APIs (like search), there is also support for using wildcards (since 0.19.8) in order to resolve indices and aliases. For example, if we have an indices test1, test2 and test3, we can simply specify test* and automatically operate on all of them. The syntax also support the ability to add (+) and remove (-), for example: +test*,-test3.

        # uri=/INDEX/TYPE
        uri=b'/log2013/journal/'+auuid+b'?routing='+uid
        content=atpic.zmq_elastic_client.http_general(essock,b'PUT',uri,ajson)
        atpic.log.debug(yy,content)



    pass


if __name__ == "__main__":
    print('hi')
    environ={}
    uid=b'1'
    aid=b'8'
    actions=[b'put',]
    hxplo=atpic.xplo.Xplo([])
    pxplo=atpic.xplo.Xplo([])
    axml=b''
    environ[b'PATH_INFO']=b'/user/1/gallery/22/pic/33/put'
    environ[b'PATH_INFO']=b'/gallery/22/pic/33/put'
    indata=[(b'somekey',False,b'somevalue'),(b'somekey2',False,b'somevalue2'),]
    ajson=forge_json(hxplo,pxplo,actions,indata,environ,uid,aid,axml)
    print(ajson)
    print(ajson.decode('utf8'))
